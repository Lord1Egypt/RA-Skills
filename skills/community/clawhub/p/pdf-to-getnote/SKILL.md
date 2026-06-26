---
name: pdf-to-getnote
description: 当用户发送 PDF 文件并要求存入 GetNotes 时触发。执行完整流程：PDF 转图片 → AI 摘要生成 → 创建含摘要和全图片的单一笔记。触发词包括「PDF存到GetNotes」「PDF导入GetNotes」「把这个PDF存笔记里」。
---

# PDF 转 GetNotes 笔记

将 PDF 文件存入 GetNotes，生成一条包含 AI 摘要和全部 PDF 页面的单一笔记。

## 核心限制（必须先知道）

**GetNotes API 关键限制：**
- `img_text` 类型传多张图片时，每张图会创建独立笔记（不支持多图合并）
- `img_text` 的 `content` 字段会被 OCR 结果覆盖，不保留传入的摘要
- `plain_text` 可以保留 `content`，图片只能以 Markdown `![](url)` 内嵌显示
- 图片上传只支持 jpg/png/gif/webp，不支持 PDF 原文件作为附件

**结论：最优方案是 `plain_text + Markdown 内嵌图片`**

---

## 执行流程

### Step 1：PDF → 高清 PNG（PyMuPDF 2x 放大）

```python
import fitz, os

def pdf_to_images(pdf_path, output_dir, zoom=2.0):
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(zoom, zoom)
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=mat)
        out = f"{output_dir}/page_{i+1:02d}.png"
        pix.save(out)
        paths.append(out)
    doc.close()
    return paths
```

输出路径：`/tmp/pdf_pages/{pdf_name}/`

### Step 2：提取 PDF 文字（如有文字层）

```python
import fitz
doc = fitz.open(pdf_path)
texts = []
for page in doc:
    t = page.get_text("text")
    if t.strip():
        texts.append(f"[Page {page.number+1}]\n{t.strip()}")
full_text = "\n\n".join(texts)
# 扫描版返回空，跳过此步，直接进入 Step 3
```

### Step 3：生成 AI 摘要（MiniMax-M2）

使用内置模型调用（蓝莓默认模型），Prompt 模板：

```
你是一位专业的知识提炼师。请仔细阅读以下内容，生成精炼摘要：

## 📄 文档信息
- 来源：[文件名]
- 总页数：[X] 页

## 📝 内容摘要
[3-5个要点，概括核心内容]

## 💡 关键洞察
[1-3条最有价值的 insight]

## 🔗 适用场景
[适用人群和使用场景]

---
以下是内容：
{extracted_text}
```

**调用方式**：在 agent 内直接调用 MiniMax-M2 模型（已配置为默认模型，无需额外 API Key）。

如需直接调用 MiniMax API：
```python
import urllib.request, json

API_KEY = os.environ.get("MINIMAX_API_KEY")
resp = urllib.request.Post(
    "https://api.minimax.io/v1/text/chatcompletion_pro?GroupId=...",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"model": "MiniMax-M2", "messages": [...]}
)
```

### Step 4：上传图片到 OSS（逐张）

凭证从 `~/.openclaw/openclaw.json` → `skills.entries.getnote` 读取：
```python
import os, json, urllib.request, subprocess

with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
    cfg = json.load(f)["skills"]["entries"]["getnote"]

API_KEY = cfg["apiKey"]
CLIENT_ID = cfg["env"]["GETNOTE_CLIENT_ID"]
```

获取 token → 上传 OSS（字段顺序严格）：
```python
def get_token():
    req = urllib.request.Request(
        "https://openapi.biji.com/open/api/v1/resource/image/upload_token?mime_type=png&count=1",
        headers={"Authorization": f"Bearer {API_KEY}", "X-Client-ID": CLIENT_ID}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def upload_to_oss(page_path, token_data):
    d = token_data["data"]
    cmd = [
        "curl", "-s", "-X", "POST", d["host"],
        "-F", f"key={d['object_key']}",
        "-F", f"OSSAccessKeyId={d['accessid']}",
        "-F", f"policy={d['policy']}",
        "-F", f"signature={d['signature']}",
        "-F", f"callback={d['callback']}",
        "-F", f"Content-Type=image/png",
        "-F", f"file=@{page_path}"
    ]
    subprocess.run(cmd, capture_output=True)
    return d["access_url"]
```

### Step 5：创建 plain_text 笔记

```python
content = f"## 📄 文档信息\n- **文件名：** {pdf_name}\n- **总页数：** {N}页\n\n## 📝 AI摘要\n{ai_summary}\n\n---\n\n## 📑 PDF原件\n\n"
for i, url in enumerate(page_urls):
    content += f"### 第{i+1}页\n![]({url})\n\n"

payload = {
    "note_type": "plain_text",
    "title": f"{pdf_name} - 完整摘要 + 全{N}页",
    "content": content,
    "tags": ["PDF导入"]
}

# POST /open/api/v1/resource/note/save（同步返回 note_id）
```

### Step 6：加入知识库（如需要）

```python
urllib.request.Request(
    "https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add",
    data=json.dumps({"topic_id": topic_id, "note_ids": [note_id]}).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "X-Client-ID": CLIENT_ID, "Content-Type": "application/json"},
    method="POST"
)
```

---

## 推荐快捷脚本

```bash
python3 skills/pdf-to-getnote/scripts/run_pdf_to_getnote.py \
  /path/to/file.pdf \
  "知识库ID(可选)" \
  "自定义标题(可选)"
```

凭证自动从 `~/.openclaw/openclaw.json` 读取，无需手动传入。

---

## 凭证配置（不硬编码）

凭证从 `~/.openclaw/openclaw.json` 自动读取，不再写在文件里：

```json
{
  "skills": {
    "entries": {
      "getnote": {
        "apiKey": "gk_live_xxx",
        "env": {
          "GETNOTE_CLIENT_ID": "cli_xxx"
        }
      }
    }
  }
}
```

如需更新凭证，修改 `~/.openclaw/openclaw.json` 即可。

---

## 详细 SOP 和 API 行为说明

完整流程、API 限制说明、错误处理详见：
- `references/full_sop.md` — 完整执行SOP
- `references/api_behavior.md` — API 关键行为发现（2026-04-01实测）
