---
name: personal-wiki
version: 1.0.0
description: |
  个人知识库（LLM Wiki）操作 skill。
  当用户提到以下意图时触发：
  - Ingest：处理新内容、更新知识库、"处理IMA新内容"、"处理印象笔记"、"处理raw里的文件"、"帮我ingest"
  - Query：查 wiki、"wiki里有没有关于XX"、"从知识库里找XX"
  - Lint：整理wiki、"检查知识库"、"清理一下wiki"
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

> **配置项**：Wiki 默认位于 `~/wiki/`。如需自定义路径，在 shell 环境中设置 `WIKI_DIR` 环境变量。

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
# Wiki 路径
WIKI_DIR="${WIKI_DIR:-$HOME/wiki}"

# IMA 凭证
IMA_CLIENT_ID="$(cat ~/.config/ima/client_id 2>/dev/null)"
IMA_API_KEY="$(cat ~/.config/ima/api_key 2>/dev/null)"
if [ -z "$IMA_CLIENT_ID" ] || [ -z "$IMA_API_KEY" ]; then
  echo "缺少 IMA 凭证，请检查 ~/.config/ima/"
  echo "获取方式：https://ima.qq.com/agent-interface"
  exit 1
fi

# Evernote 凭证
if [ -z "$EVERNOTE_TOKEN" ]; then
  echo "缺少 EVERNOTE_TOKEN，请配置环境变量"
  echo "获取方式：https://app.yinxiang.com/api/DeveloperToken.action"
  exit 1
fi
EVERNOTE_HOST="${EVERNOTE_HOST:-app.yinxiang.com}"
```

## 操作决策表

| 用户意图 | 操作 | 读取章节 |
|---|---|---|
| 处理 IMA / 腾讯笔记新内容 | Ingest — IMA | `## Ingest：IMA 笔记` |
| 处理印象笔记指定笔记 | Ingest — Evernote | `## Ingest：印象笔记` |
| 处理 raw/ 里的文件 | Ingest — 本地文件 | `## Ingest：本地文件` |
| 处理所有新内容 | 三路并行 Ingest | 以上三个章节 |
| 查询 wiki 内容 | Query | `## Query` |
| 整理/检查 wiki | Lint | `## Lint` |
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

读取 `$WIKI_DIR/log.md` 中"IMA 笔记"表格，跳过已记录的 `doc_id`。
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

读取 `$WIKI_DIR/schema.md` 了解规则，然后：

1. 分析内容：主题、关键概念、类型（知识/Demo脚本/其他）
2. 判断归入哪些现有 page，或是否需要新建
3. 写入 / 更新 `$WIKI_DIR/pages/[主题].md`（格式见 `## Wiki 页面格式`）
4. 更新 `$WIKI_DIR/index.md`
5. 在 `$WIKI_DIR/log.md` 的"IMA 笔记"表格追加一行：

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

> **注意**：印象笔记笔记本数量可能很多，不做全量扫描。用户明确指定笔记标题或笔记本时才处理。

### Python 初始化

```python
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

对比 `$WIKI_DIR/log.md` 中"印象笔记"表格，跳过 `guid` 已记录且 `updated` 未变化的笔记。

处理完成后在 log.md 中追加：

```
| {guid} | {标题} | {updated_ms} | {今日日期} |
```

### Token 有效期提醒

印象笔记开发者 Token 有效期约 2 周。若遇到 `EDAMUserException errorCode=9`（AUTH_EXPIRED），提示用户去 https://app.yinxiang.com/api/DeveloperToken.action 重新生成，并更新 `~/.zshrc` 中的 `EVERNOTE_TOKEN`。

---

## Ingest：本地文件

### 目标

处理用户放入 `$WIKI_DIR/raw/` 的文件，提取文字内容后 Ingest 进 Wiki。

### 步骤 1 — 扫描新文件

```bash
ls -la "$WIKI_DIR/raw/"
```

对比 `$WIKI_DIR/log.md` 中"本地文件"表格，找出未处理的文件。

### 步骤 2 — 内容提取

根据扩展名选择提取方式：

```python
import os
from pathlib import Path

wiki_dir = os.environ.get('WIKI_DIR', os.path.expanduser('~/wiki'))
file_path = os.path.join(wiki_dir, 'raw', '文件名')
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

**依赖安装**：
- `python-pptx`：`pip3 install python-pptx`
- `pdftotext`：macOS 系统自带；Linux 需安装 `poppler-utils`
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

1. 读取 `$WIKI_DIR/index.md` 了解现有分类和页面列表
2. 根据问题，确定相关分类和 page
3. 读取相关 `$WIKI_DIR/pages/[主题].md` 文件
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

## Demo 生成

### 目标

基于 `$WIKI_DIR/pages/Demo_Script_*.md` 中的模板，替换客户和行业信息，生成定制版 Demo 脚本。

### 步骤

1. 读取对应的 Demo Script 模板页面
2. 查看顶部"替换清单"表格，获取所有占位符
3. 根据用户提供的客户名和行业信息，替换所有占位符
4. 根据行业，调整"行业定制要点"中指出的特定段落
5. 输出完整定制版脚本（可选：保存为新文件）

---

## Wiki 页面格式

每个 `$WIKI_DIR/pages/[主题].md` 的标准格式：

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
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | 笔记标题示例 | 1743868000000 | 2026-01-01 |

## IMA 笔记
| doc_id | 标题 | modify_time (ms) | ingest 时间 |
|--------|------|-----------------|------------|
| 1234567890123456 | 笔记标题示例 | 1742601600000 | 2026-01-01 |

## 本地文件
| 文件名 | mtime | ingest 时间 |
|--------|-------|------------|
| example.pptx | 2026-01-01T10:00:00 | 2026-01-01 |
```
