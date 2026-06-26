# PDF 导入 GetNotes 完整 SOP（2026-04-01 实测版）

## 目标

用户发送 PDF → 生成一条 GetNotes 笔记，包含：
1. AI 生成的 Markdown 摘要
2. PDF 所有页面以图片形式内嵌在同一笔记中

## 技术限制

| 限制项 | 说明 |
|--------|------|
| img_text 多图 | API 为每张图创建独立笔记，不支持多图合并 |
| img_text content | content 字段被 OCR 结果覆盖，不保留 |
| PDF 附件上传 | API 只接受 jpg/png/gif/webp，不支持 PDF |
| plain_text 图片 | 图片以 `![](url)` Markdown 形式内嵌 |

**结论：唯一可行方案 = plain_text + Markdown 内嵌图片**

---

## 完整流程

### Step 1：PDF → PNG 逐页转换

```python
import fitz, os

def pdf_to_images(pdf_path, output_dir, zoom=2.0):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(zoom, zoom)
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

- 输出目录：`/tmp/pdf_pages/{pdf_name}/`
- 放大倍数：2.0x（A4 → 2160×1856px PNG，每页约 3-6MB）
- 成功率：100%

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
```

- 扫描版 PDF（无文字层）：`page.get_text()` 返回空字符串，跳过此步
- 非扫描版：提取文字用于 AI 摘要生成

### Step 3：AI 摘要生成

使用 MiniMax-M2 模型，Prompt 模板：

```markdown
你是一位专业的知识提炼师。请仔细阅读以下 PDF 文稿内容，并按以下格式生成精炼摘要：

## 📄 文档信息
- 来源：[文件名]
- 总页数：[X] 页

## 📝 内容摘要
[请用 3-5 个要点概括文档核心内容，每个要点一句话，优先使用主动句式]

## 💡 关键洞察
[提炼 1-3 条最有价值的 insight，用 bullet list]

## 🔗 适用场景
[这段内容适用于什么场景？适合谁阅读？]

---
以下是 PDF 文稿内容：
{extracted_text}
```

### Step 4：上传图片到 OSS（逐张）

**每次只返回 1 个 token**，每张图单独获取+上传：

```python
import subprocess, json, urllib.request

API_KEY = "..."
CLIENT_ID = "..."

def get_token():
    req = urllib.request.Request(
        "https://openapi.biji.com/open/api/v1/resource/image/upload_token?mime_type=png&count=1",
        headers={"Authorization": f"Bearer {API_KEY}", "X-Client-ID": CLIENT_ID}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def upload(page_path, token_data):
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
    r = subprocess.run(cmd, capture_output=True, text=True)
    return d["access_url"]
```

- 字段顺序必须严格：key → OSSAccessKeyId → policy → signature → callback → Content-Type → file
- 两次调用间隔建议 >0.3 秒，避免限流

### Step 5：创建 plain_text 笔记

```python
content = f"""## 📄 文档信息
- **文件名：** {pdf_name}
- **总页数：** {N}页（PDF扫描版）

## 📝 AI摘要
{AI_SUMMARY}

---

## 📑 PDF原件（共{N}页）

"""

for page_num, url in enumerate(page_urls):
    content += f"### 第{page_num+1}页\n![]({url})\n\n"

payload = {
    "note_type": "plain_text",
    "title": f"{pdf_name} - 完整摘要 + 全{N}页",
    "content": content,
    "tags": ["PDF导入"]
}

# POST /open/api/v1/resource/note/save
# 同步返回 note_id
```

### Step 6：加入知识库（如需要）

```python
# POST /open/api/v1/resource/knowledge/note/batch-add
{
    "topic_id": "知识库ID",
    "note_ids": [note_id]
}
```

- 每批最多 20 条
- 同步返回

---

## 错误处理

| 错误码 | 说明 | 处理 |
|--------|------|------|
| 10004 | 未授权 | 重新 OAuth 授权 |
| 10000 | 不支持的图片类型 | 检查 mime_type 是否为 png/jpg/jpeg/gif/webp |
| 42900 | 限流 | 降低上传频率，重试 |

---

## API 凭证

- Base URL: `https://openapi.biji.com`
- API Key: `gk_live_84d5a871fbae9ad7.473f6246fc533a91f0c6ae1187c79e26a2a16fe050dcde53`
- Client ID: `cli_a1b2c3d4e5f6789012345678abcdef90`

凭证存储在 `~/.openclaw/openclaw.json` → `skills.entries.getnote`
