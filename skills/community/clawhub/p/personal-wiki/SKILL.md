---
name: personal-wiki
description: |
  个人知识库（LLM Wiki）操作 skill。
  当用户提到以下意图时触发：
  - Ingest：处理新内容、更新知识库、"处理IMA新内容"、"处理印象笔记"、"处理raw里的文件"、"帮我ingest"
  - Query：查 wiki、"wiki里有没有关于XX"、"从知识库里找XX"
  - Lint：整理wiki、"检查知识库"、"清理一下wiki"
  - Visualize：可视化知识图谱、"看看wiki长什么样"、"生成关系图"、"知识库图谱"
  - Demo生成：基于 Demo Script 生成定制版本、"帮我做一个XX客户的demo"
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env: ["EVERNOTE_TOKEN"]
      files:
        - "~/.config/ima/client_id"
        - "~/.config/ima/api_key"
---

# personal-wiki

基于 Karpathy LLM Wiki 范式构建的个人知识库操作 skill。
Wiki 存放于本地 `~/wiki/`，内容来自三个来源：IMA 笔记、印象笔记、本地文件。

## 系统路径

```
~/wiki/
├── raw/          ← 用户放置待处理文件（PDF/PPT/Word）
├── schema.md     ← 分类和格式规则
├── index.md      ← 总目录（自动维护）
├── log.md        ← 已处理记录（去重依据）
└── pages/        ← Wiki 知识页面
    └── [主题].md
```

## 凭证加载

每次操作前，先加载凭证：

```bash
# IMA 凭证
IMA_CLIENT_ID="$(cat ~/.config/ima/client_id 2>/dev/null)"
IMA_API_KEY="$(cat ~/.config/ima/api_key 2>/dev/null)"
if [ -z "$IMA_CLIENT_ID" ] || [ -z "$IMA_API_KEY" ]; then
  echo "缺少 IMA 凭证，请检查 ~/.config/ima/"
  exit 1
fi

# Evernote 凭证
if [ -z "$EVERNOTE_TOKEN" ]; then
  echo "缺少 EVERNOTE_TOKEN，请配置环境变量"
  exit 1
fi
EVERNOTE_HOST="${EVERNOTE_HOST:-app.yinxiang.com}"
```

## 操作决策表

| 用户意图 | 操作 | 读取章节 |
|---|---|---|
| 处理 IMA / 腾讯笔记新内容 | Ingest — IMA | `## Ingest：IMA 笔记` |
| 处理印象笔记指定笔记 | Ingest — Evernote | `## Ingest：印象笔记` |
| 回写/更新已有印象笔记（插内容到顶部等） | Evernote 回写 | `### 回写印象笔记` |
| 处理 raw/ 里的文件 | Ingest — 本地文件 | `## Ingest：本地文件` |
| 处理所有新内容 | 三路并行 Ingest | 以上三个章节 |
| 查询 wiki 内容 | Query | `## Query` |
| 整理/检查 wiki | Lint | `## Lint` |
| 可视化 wiki 图谱 / "看看知识库长什么样" / "生成关系图" | Visualize | `## Visualize` |
| 生成 Demo 定制版本 | Demo 生成 | `## Demo 生成` |

---

## Ingest：IMA 笔记

### 目标

读取 IMA 中的笔记，对比 `log.md` 中已处理记录，Ingest 新增或更新过的笔记。

### 步骤 1 — 拉取笔记列表

```bash
curl -s --max-time 15 \
  -X POST "https://ima.qq.com/openapi/note/v1/list_note_by_folder_id" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"cursor": "", "limit": 50}'
```

从返回结果 `data.note_book_list[].basic_info.basic_info` 取：
- `docid`：笔记 ID
- `title`：标题
- `modify_time`：最后修改时间（毫秒时间戳，字符串格式）

### 步骤 2 — 对比 log.md 找出新内容

读取 `~/wiki/log.md` 中"IMA 笔记"表格，跳过已记录的 `doc_id`。
如果 `modify_time` 比 log 中记录的更新，视为有更新，重新 Ingest。

### 步骤 3 — 读取笔记全文

```bash
curl -s --max-time 15 \
  -X POST "https://ima.qq.com/openapi/note/v1/get_doc_content" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"doc_id\": \"$DOC_ID\", \"target_content_format\": 0}"
```

返回 `data.content` 为纯文本正文。

### 步骤 4 — 分析并写入 Wiki

读取 `~/wiki/schema.md` 了解规则，然后：

1. 分析内容：主题、关键概念、类型（知识/Demo脚本/其他）
2. 判断归入哪些现有 page，或是否需要新建
3. 写入 / 更新 `~/wiki/pages/[主题].md`（格式见 `## Wiki 页面格式`）
4. 更新 `~/wiki/index.md`
5. 在 `~/wiki/log.md` 的"IMA 笔记"表格追加一行：

```
| {doc_id} | {标题} | {modify_time} | {今日日期} |
```

### 特殊类型路由

| 内容特征 | 建议分类 | 处理方式 |
|---|---|---|
| 销售演示脚本、Demo 流程 | `Demo Script` | 创建带替换占位符的模板页 |
| 产品/技术知识 | 对应产品分类 | 创建知识页 |
| 行业分析、市场资讯 | 对应行业分类 | 创建知识页 |
| 个人笔记/随想 | 自动聚类 | 按内容决定 |

---

## Ingest：印象笔记

### 目标

读取用户指定的印象笔记笔记，Ingest 进 Wiki。

> **注意**：印象笔记有 220+ 笔记本，不做全量扫描。用户明确指定笔记标题或笔记本时才处理。

### Python 环境说明

> **重要**：evernote2 需要 `python3.12`（不兼容 Python 3.14+，因 `distutils` 已移除）。
> 所有印象笔记相关脚本必须用 `python3.12` 执行。
> 依赖已安装：`python3.12 -m pip install evernote2 oauth2 setuptools --break-system-packages`
> evernote2 库需 patch：`/opt/homebrew/lib/python3.12/site-packages/evernote2/api/client.py` 第145行 `getargspec` → `getfullargspec`（已完成）

### Python 初始化

```python3.12
import os, re
from evernote2.api.client import EvernoteClient
import evernote2.edam.notestore.ttypes as NoteStoreTypes

token = os.environ.get('EVERNOTE_TOKEN')
host = os.environ.get('EVERNOTE_HOST', 'app.yinxiang.com')
client = EvernoteClient(token=token, service_host=host)
note_store = client.get_note_store()

def enml_to_text(enml):
    text = re.sub(r'<[^>]+>', '\n', enml)
    return re.sub(r'\n+', '\n', text).strip()
```

### 按标题搜索

```python
f = NoteStoreTypes.NoteFilter()
f.words = 'intitle:"笔记标题"'
spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True, includeUpdated=True)
result = note_store.findNotesMetadata(token, f, 0, 10, spec)

for note in result.notes:
    content = note_store.getNoteContent(token, note.guid)
    text = enml_to_text(content)
    # → 进入 Ingest 分析流程
```

### 对比 log.md

对比 `~/wiki/log.md` 中"印象笔记"表格，跳过 `guid` 已记录且 `updated` 未变化的笔记。

处理完成后在 log.md 中追加：

```
| {guid} | {标题} | {updated_ms} | {今日日期} |
```

### Token 有效期提醒

印象笔记开发者 Token 有效期约 2 周。若遇到 `EDAMUserException errorCode=9`（AUTH_EXPIRED），提示用户去 https://app.yinxiang.com/api/DeveloperToken.action 重新生成，并更新 `~/.zshrc` 中的 `EVERNOTE_TOKEN`。

> 🔴 **安全**：token 若被贴进对话（HAI 环境会进内网日志），提醒用户下次直接在 Terminal `export` 或写 `~/.zshrc`。刷新后主动帮用户把新 token 覆盖进 `~/.zshrc`（Edit 替换旧行），省得每次过期重贴。

### 回写印象笔记（更新已有笔记内容）

当用户要求"把内容整理进某篇印象笔记 / 插到笔记顶部"时，用 `updateNote` 回写。**三个必踩的坑**：

1. **ENML 是严格 XML，`&` 必须转义成 `&amp;`**
   - 内容里的 "SAP&盖雅"、"目标&继任"、"A&B" 都会导致 `EDAMUserException errorCode=11`（`reference to entity must end with ';'`）
   - 其他要转义：`<` → `&lt;`、`>` → `&gt;`；`"` 在正文里 OK 不用转
   - 保险做法：构造 new_block 后先 `content.replace('&','&amp;')`（但注意别把已有的 `&amp;`/`<br />` 二次转义——若手写 div 就手动只转正文里的裸 `&`）

2. **`note.resources = None` 再 updateNote**
   - `getNote` 带回的 resources（附件）在 update 时可能触发校验问题；纯文本笔记回写前置 `note.resources = None` 最稳

3. **顶部插入 pattern**（保留原有内容，新块插最前）
   ```python
   marker = '<en-note>'
   idx = content.find(marker) + len(marker)
   new_content = content[:idx] + new_block + content[idx:]
   note.content = new_content
   note.resources = None
   ns.updateNote(token, note)
   ```
   - new_block 用 `<div>...</div>` 逐行，空行用 `<div><br /></div>`
   - 与原内容间空开 3-4 行 = 追加 3-4 个 `<div><br /></div>`

完整回写脚本：

```python3.12
import os
from evernote2.api.client import EvernoteClient
token = os.environ['EVERNOTE_TOKEN']
client = EvernoteClient(token=token, service_host='app.yinxiang.com')
ns = client.get_note_store()
note = ns.getNote(token, GUID, True, False, False, False)
new_block = '<div>标题</div><div>正文里的 &amp; 已转义</div><div><br /></div>'
idx = note.content.find('<en-note>') + len('<en-note>')
note.content = note.content[:idx] + new_block + note.content[idx:]
note.resources = None
ns.updateNote(token, note)
```

### Token 更新到 zshrc（刷新后主动做）

```bash
# 用 Edit 工具替换 ~/.zshrc 里的旧 EVERNOTE_TOKEN 行，不要 append 造成重复
grep -n "EVERNOTE_TOKEN" ~/.zshrc   # 先定位旧行
```

---

## Ingest：本地文件

### 目标

处理用户放入 `~/wiki/raw/` 的文件，提取文字内容后 Ingest 进 Wiki。

### 步骤 1 — 扫描新文件

```bash
ls -la ~/wiki/raw/
```

对比 `~/wiki/log.md` 中"本地文件"表格，找出未处理的文件。

### 步骤 2 — 内容提取

根据扩展名选择提取方式：

```python
import os
from pathlib import Path

file_path = os.path.expanduser("~/wiki/raw/文件名")
ext = Path(file_path).suffix.lower()

if ext == '.pptx':
    from pptx import Presentation
    prs = Presentation(file_path)
    slides = []
    for i, slide in enumerate(prs.slides):
        texts = [s.text.strip() for s in slide.shapes if hasattr(s, "text") and s.text.strip()]
        if texts:
            slides.append(f"Slide {i+1}: {' | '.join(texts)}")
    content = '\n'.join(slides)

elif ext == '.pdf':
    import subprocess
    result = subprocess.run(['pdftotext', file_path, '-'], capture_output=True, text=True)
    content = result.stdout

elif ext in ['.docx']:
    from docx import Document
    doc = Document(file_path)
    content = '\n'.join(p.text for p in doc.paragraphs if p.text.strip())

elif ext in ['.md', '.txt']:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
```

**依赖检查**：
- `python-pptx`：`pip3 install python-pptx`（已安装 1.0.2）
- `pdftotext`：macOS 系统自带
- `python-docx`：`pip3 install python-docx`

### 步骤 3 — 分析并写入 Wiki

同 IMA Ingest 步骤 4，分析内容后写入 pages/，更新 index.md。

处理完成后在 log.md 追加：

```
| {文件名} | {mtime} | {今日日期} |
```

---

## Query

### 目标

从 Wiki 中检索信息，综合多个 page 回答用户问题。

### 步骤

1. 读取 `~/wiki/index.md` 了解现有分类和页面列表
2. 根据问题，确定相关分类和 page
3. 读取相关 `~/wiki/pages/[主题].md` 文件
4. 综合多个 page 内容，给出综合回答
5. 如果回答本身有知识价值，询问用户是否写回 Wiki

### 注意

- 优先搜索 `pages/` 目录，不要重复 Ingest 已处理过的内容
- 答案要注明来自哪些 page（便于追溯来源）

---

## Lint

### 目标

定期检查 Wiki 质量，发现问题并修复。

### 检查项

1. **孤立页面**：没有任何其他 page 在 `关联主题` 中链接它
2. **内容矛盾**：两个 page 对同一概念有不一致的描述
3. **过时内容**：log.md 中某来源有更新记录，但对应 page 的 `last_updated` 未跟进
4. **细碎分类**：某分类只有 1 个 page，且可归入其他分类
5. **缺失关联**：两个明显相关的 page 没有互相在 `关联主题` 中链接

### 输出

列出发现的问题，询问用户是否逐项修复。修复后更新相关 page 和 index.md。

---

## Visualize

### 目标

把 `~/wiki/pages/` 转成**单文件交互式知识图谱 HTML**（cytoscape 力导向图 + 节点详情面板），数据不出本地。这是 personal-wiki 的 **Obsidian 平替**——不用装 Obsidian、不改 wiki 结构。

### 一键生成

```bash
# 需要能 import yaml 的 python（3.11/3.12/3 均可，仅依赖 pyyaml）
python3 ~/.claude/skills/personal-wiki/scripts/viz/visualize.py
open ~/wiki/wiki-graph.html
```

参数（可选）：`visualize.py [WIKI_PAGES_DIR] [OUT_HTML] [BUNDLE_NAME]`
默认 `~/wiki/pages` → `~/wiki/wiki-graph.html`，名称 "My Wiki"。

输出示例：`[ok] 65 concepts / 371 edges / 1356 KB -> ...`

### 关键实现（来源 + 双链补丁）

- **来源**：vendored 自 Google Open Knowledge Format (OKF) viewer（Apache-2.0，`github.com/GoogleCloudPlatform/knowledge-catalog`）。LICENSE 在 `scripts/viz/OKF-LICENSE.md`。
- **只依赖 pyyaml**——刻意剥掉 OKF repo 的 `google-adk` / `google-cloud-bigquery`（几百 MB，只给它的 enrich agent 用）。
- **`[[双链]]` 补丁（必须）**：OKF 原版只认 `[text](path.md)` 标准链接，我的 wiki 用 `[[双链]]`。`generator.py` 已 patch：两遍扫描先建 alias_map（文件名 stem + frontmatter title + 首个 H1 → concept_id），`_norm_alias()` 做模糊匹配（lower + 空格↔下划线 + 破折号归一），支持 `[[name]]` 和 `[[name|alias]]` 两种写法。没这个补丁边会几乎全丢。

### 兼顾 Lint

生成后看孤立节点（图上没有任何连线的点）= Lint 检查项 1 的可视化版。跑一遍图谱能直观发现"孤立页面 / 稀疏聚类"，比逐页读 `关联主题` 快。

---

## Demo 生成

### 目标

基于 `~/wiki/pages/Demo_Script_*.md` 中的模板，替换客户和行业信息，生成定制版 Demo 脚本。

### 步骤

1. 读取对应的 Demo Script 模板页面
2. 查看顶部"替换清单"表格，获取所有占位符
3. 根据用户提供的客户名和行业信息，替换所有占位符
4. 根据行业，调整"行业定制要点"中指出的特定段落
5. 输出完整定制版脚本（可选：保存为新文件）

### 现有 Demo Script 模板

| 文件 | 行业 | 适用场景 |
|---|---|---|
| `Demo_Script_ECP_HK_零售.md` | 零售/高端零售 | SAP EC Payroll HK，MPF/ORSO/PCC/回溯计算 |

---

## Wiki 页面格式

每个 `~/wiki/pages/[主题].md` 的标准格式：

```markdown
---
category: [分类名]
tags: [标签1, 标签2]
sources:
  - type: evernote | ima_note | local_file
    id: [guid / doc_id / 文件名]
    title: [原始标题]
last_updated: YYYY-MM-DD
---

# [主题名]

## 核心摘要
（3-5 句话）

## 详细内容
（要点、关键概念、数据、背景）

## 关联主题
- [[相关主题1]]
- [[相关主题2]]

## 来源记录
- [原始标题](来源类型) — YYYY-MM-DD
```

**Demo Script 页面**在标准格式基础上，顶部额外包含：
- 替换清单表格（占位符 → 示例值 → 替换为）
- 行业定制要点（当前行业 + 其他行业调整建议）

---

## log.md 格式参考

```markdown
## 印象笔记
| guid | 标题 | updated (ms) | ingest 时间 |
|------|------|-------------|------------|
| abc123 | 笔记标题 | 1743868000000 | 2026-04-06 |

## IMA 笔记
| doc_id | 标题 | modify_time (ms) | ingest 时间 |
|--------|------|-----------------|------------|
| 7379871906939637 | SAP主权云 | 1759497600000 | 2026-04-05 |

## 本地文件
| 文件名 | mtime | ingest 时间 |
|--------|-------|------------|
| report.pptx | 2026-04-03T11:13:00 | 2026-04-05 |
```
