---
name: IMA 笔记模块
description: IMA 笔记管理模块。负责搜索、浏览、创建、编辑（追加）用户个人笔记。
allowed-tools: Bash,Read
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["node"]}}}
---

# Notes (笔记)

> ⛔ Before ANY write (`import_doc`/`append_doc`): validate ALL string fields (`content`, `title`) are legal UTF-8.
> Non-UTF-8 content causes irreversible garbled text in IMA. See root SKILL.md § MANDATORY RULES for platform-specific validation methods.

API base path: `openapi/note/v1`

通过 IMA OpenAPI 管理用户个人笔记，支持读取（搜索、列表、获取内容）和写入（新建、追加）。

完整的数据结构和接口参数详见 `references/api.md`。

> **隐私规则：** 笔记内容属于用户隐私，在群聊场景中只展示标题和摘要，禁止展示笔记正文。

## 接口决策表

| 用户意图                                                                          | 调用接口          | 关键参数                                                                  |
| --------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------- |
| 搜索/查找笔记                                                                     | `search_note`     | `query_info`（QueryInfo 对象）                                            |
| 查看笔记本列表 / 列出笔记本                                                       | `list_notebook`   | `cursor`(必填，首页传`"0"`) + `limit`(必填)                               |
| 列出笔记/获取多篇笔记信息                                                         | `list_note`       | `folder_id`(选填,空为全部) + `sort_type` + `cursor`(首次传`""`) + `limit` |
| 读取笔记正文                                                                      | `get_doc_content` | `note_id` + `target_content_format`(必填，推荐`0`纯文本)                  |
| 新建一篇笔记（用户明确说"新建/创建笔记"时走此接口）                               | `import_doc`      | `content` + `content_format`(必填，固定`1`) + 可选 `folder_id`            |
| 往已有笔记追加内容（⚠️ **敏感操作**：用户必须明确指定目标笔记，否则先确认再操作） | `append_doc`      | `note_id` + `content` + `content_format`(必填，固定`1`)                   |
| 往笔记插入含图片的内容（本地/远程图片）                                           | `note-images.cjs` | `--note-id` + `--file`/`--content`；图片 < 3MiB，仅 PNG/JPEG/WebP         |
| 编辑笔记前获取块结构（update_note 前置）                                          | `export_note_blocks` | `note_id` |
| 按 block 精细编辑笔记（改/删/插某段）                                             | `update_note`     | `note_id` + `user_request_id`(UUIDv4) + `updates[]`(block_id/action/new_content) |
| 重命名笔记本                                                                       | `rename_notebook` | `folder_id` + `new_folder_name` |
| 导出整篇笔记（Markdown/纯文本/JSON）                                            | `export_note`     | `note_id` + `target_content_format`(推荐`1`) |
| 智能推送：不存在则新建、存在则追加                                              | `push_note`       | `content`(可选)+`note_id`(可选)+`content_cos_key`(可选) |
| 重命名单篇笔记标题                                                               | `rename_note`     | `note_id` + `title` |
| 批量移动笔记到其他笔记本                                                         | `move_notes`      | `note_ids[]` + `target_folder_id` |

## ⚠️ 新建 vs. 追加 — 行为规则

**新建笔记（`import_doc`）** 和 **追加内容到已有笔记（`append_doc`）** 是两个完全不同的操作，务必正确区分：

### 明确走新建的信号词

用户说以下任一表述时，**直接调用 `import_doc` 创建新笔记**：

- "**新建**笔记"、"**创建**笔记"、"**写一篇**笔记"
- "**新建**一篇笔记记录这些内容"

### 明确走追加的信号词

用户说以下任一表述时，**调用 `append_doc` 追加到已有笔记**（但仍需确认目标笔记，见下方规则）：

- "把这段话**追加到**《XX》笔记里"
- "在那篇笔记**末尾加上**这段内容"

### 模糊场景 — 必须先询问用户

以下表述**既可能是新建、也可能是追加**，agent **不得自行假设**，必须先向用户确认：

- "帮我记一下"、"记录一下"、"保存为笔记"、"存成笔记"
- "把这段内容记到笔记里"
- "添加到笔记里"
- 任何其他未明确表达"新建"或"追加"意图的表述

询问示例：

> "您是想**创建一篇新笔记**，还是**追加到某篇已有笔记**？"

### 追加到已有笔记是敏感操作

`append_doc` 会**不可撤销地修改**用户的现有笔记，因此必须谨慎处理：

1. **用户明确指定了目标笔记** — 可以直接追加。例如：

   - "把这段话追加到《会议纪要》笔记里"
   - "在那篇笔记末尾加上这段内容"（上下文中已有明确的笔记对象）

2. **用户没有明确指定目标笔记** — **必须先向用户确认**，不要自行猜测。例如：
   - 用户说"添加到笔记里" → 询问："您想追加到哪篇已有笔记？请提供笔记标题或让我帮您搜索。"
   - 用户说"把这个加到之前那篇笔记" → 如果上下文中有多篇笔记或不确定是哪篇 → 列出候选笔记让用户选择

> **原则**：不确定时，先问。宁可多问一句，也不要误改用户的已有笔记或自作主张创建新笔记。

### 🖼️ 图片写入（支持本地图片）

**含图片的 Markdown 一律用 `notes/scripts/note-images.cjs` 写入**：它把内容按原顺序分批——连续文本合并为一批、每张图片单独一批，逐批 `append_doc`。图片会被规范化为 data URL，**无需先上传到网络**。

- **支持来源**：本地路径 / `file://` URI / `http(s)` 远程图片 / base64 data URL
- **支持格式**：PNG / JPEG / WebP，单张原始文件必须 **< 3 MiB**（不得压缩、转码规避）
- **原始预检**：大小 + MIME + 真实文件签名一致性，任一不符立即拒绝

```bash
# 写入到已有笔记（--file 与 --content 二选一；建议先 --dry-run 预演）
node notes/scripts/note-images.cjs --note-id "<笔记ID>" --file "/path/to/content.md" --dry-run
node notes/scripts/note-images.cjs --note-id "<笔记ID>" --file "/path/to/content.md"

# 仅把本地图片转成临时 download_url（此模式不接受远程 URL）
node notes/scripts/note-images.cjs --url "/path/to/img.png"
```

⚠️ **它是「追加」接口，不负责新建**：

- 新建含图片的笔记 → 先用 `notes_create.cjs` 建好笔记（拿到 `note_id`），再用 `note-images.cjs` 追加含图片的正文
- 同一段文本不要两边都传，否则会重复写入
- 任一批次失败立即停止，已成功批次不回滚

**降级规则（不走脚本时）**：直接调 `import_doc` / `append_doc` 时 `content` 仅支持 Markdown，**本地图片引用会被过滤**，只保留 `http(s)` 网络图片——`notes_create.cjs` / `notes_append.cjs` 也保留此过滤行为并会提示。需要插入本地图片时，请改用 `note-images.cjs`。

## 跨平台调用说明（Windows / Linux）

单一 Node.js 实现，命令跨平台一致（需 Node 18+）；**优先用封装脚本**（`notes_create.cjs` / `notes_append.cjs` / `note-images.cjs` / `resolve_notebook.cjs`），其余接口走 `ima_api.cjs`。下文 `ima_api "<path>" '<json>'` 即：

- **Linux / macOS**：`node "$SKILL_DIR/ima_api.cjs" "$1" "$2"`
- **Windows PowerShell**：`& node "$env:SKILL_DIR/ima_api.cjs" '<path>' '<json>'`
- **Windows cmd**：先 `chcp 65001 >nul`，再 `node "%SKILL_DIR%\ima_api.cjs" "<path>" "<json>"`

中文编码：Linux/macOS 默认 UTF-8；PowerShell 5.1 须用 UTF-8 字节数组模式（Body 会被静默转 GBK）。完整写法、`ima_api` 包装函数与两层错误处理 → 见父级 `SKILL.md` 与 `references/api-call-templates.md`。

## 🌐 笔记本名解析（统一入口，优先使用）

**所有需要笔记本（folder_id）的操作，优先用笔记本名称，不要让用户提供 folder_id。**

统一解析器 `notes/scripts/resolve_notebook.cjs`：

```bash
# 按名称解析笔记本
node notes/scripts/resolve_notebook.cjs --path "学习笔记"
# → { "note_folder_id": "...", "note_folder_name": "学习笔记" }

# 列出所有笔记本
node notes/scripts/resolve_notebook.cjs --list
```

**使用规则**：

1. 用户说了笔记本名称（如"存到学习笔记里"）→ 先调 `resolve_notebook.cjs --path <名称>` 拿到 `note_folder_id`，再用于 `list_note` / `import_doc` / `move_notes` 等接口
2. 解析不到时列出当前笔记本让用户确认，禁止猜测
3. **面向用户永远只展示笔记本名称**，禁止暴露 folder_id

## 常用工作流

### 查找并阅读笔记

先搜索获取 `note_id`，再用 `get_doc_content` 读取正文：

```bash
# 1. 按标题搜索
ima_api "openapi/note/v1/search_note" '{"search_type": 0, "query_info": {"title": "会议纪要"}, "start": 0, "end": 20}'
# 从返回的 search_note_infos[].note_book_info.note_id 中取目标笔记 ID

# 2. 读取正文（纯文本格式，Markdown 格式目前不支持）
ima_api "openapi/note/v1/get_doc_content" '{"note_id": "目标note_id", "target_content_format": 0}'
```

### 列出自己有哪些笔记

直接使用`list_note`，拉取全部笔记列表，直到符合用户要求（如：用户要求全部笔记，则到 `is_end=true` 时停止；用户要求近30天的笔记，则根据`modify_time`与当前时间判断停止）

```bash
# 1. 拉取全部笔记的列表（首页 cursor 传 ""）
ima_api "openapi/note/v1/list_note" '{"folder_id":"", "sort_type":0, "cursor": "", "limit": 20}'
# 获取全部笔记中前20篇笔记的信息

```

### 浏览笔记本里的笔记

**首选：笔记本名 → folder_id 一步解析**（见上方「笔记本名解析」章节）：

```bash
# 0. 按名称解析笔记本 folder_id
node notes/scripts/resolve_notebook.cjs --path "学习笔记"
# → { "note_folder_id": "...", "note_folder_name": "学习笔记" }

# 1. 拉取该笔记本的笔记（首页 cursor 传 ""）
ima_api "openapi/note/v1/list_note" '{"folder_id": "<解析出的note_folder_id>", "cursor": "", "limit": 20}'
```

仅当需要手动探索时：

```bash
# 1. 列出笔记本（首页 cursor 传 "0"）
ima_api "openapi/note/v1/list_notebook" '{"cursor": "0", "limit": 20}'

# 2. 拉取指定笔记本的笔记（首页 cursor 传 ""）
ima_api "openapi/note/v1/list_note" '{"folder_id": "目标folder_id", "cursor": "", "limit": 20}'
```

### 新建笔记

**首选脚本**（自动 UTF-8 校验；本地图片会被过滤，含图片请改用 `note-images.cjs`）：

```bash
# 新建到默认位置
node notes/scripts/notes_create.cjs --content "# 标题

正文内容"

# 新建到指定笔记本（--path 自动解析 folder_id，带缓存）
node notes/scripts/notes_create.cjs --content "# 标题

正文内容" --path "学习笔记"

# 从文件新建
node notes/scripts/notes_create.cjs --file /tmp/note.md --path "学习笔记"
# 返回 note_id，后续可用于 append_doc
```

也可以直接调接口（灵活场景）：

```bash
ima_api "openapi/note/v1/import_doc" '{"content_format": 1, "content": "# 标题\n\n正文内容", "folder_id": "<解析出的note_folder_id>"}'
```

### 追加内容到已有笔记

**首选脚本**（⚠️ 敏感操作，AI 必须确认目标笔记明确后再调用）：

```bash
node notes/scripts/notes_append.cjs --note-id <笔记ID> --content "
## 补充内容

追加的文本"
node notes/scripts/notes_append.cjs --note-id <笔记ID> --file /tmp/extra.md
```

也可以直接调接口：

```bash
ima_api "openapi/note/v1/append_doc" '{"note_id": "笔记ID", "content_format": 1, "content": "\n## 补充内容\n\n追加的文本"}'
```

### 编辑笔记（块级精细）

编辑已有笔记中的某一段/某一块，需要两步：先用 `export_note_blocks` 获取块结构，再用 `update_note` 按 `block_id` 修改。

```bash
# 1. 获取块结构
ima_api "openapi/note/v1/export_note_blocks" '{"note_id": "笔记ID"}'
# 从返回的 data.blocks[] 中取目标 block_id 和 editable 字段

# 2. 按 block 修改：action 1=EDIT替换 / 2=DELETE删除 / 3=APPEND在该块后插入
ima_api "openapi/note/v1/update_note" '{"note_id": "笔记ID", "user_request_id": "本轮UUIDv4", "updates": [{"block_id": "目标block_id", "action": 1, "new_content": "新的Markdown内容"}]}'
```

**`user_request_id` 复用规则**：同一用户消息内的多次 `update_note` 调用必须复用同一个 UUID v4；收到新的用户消息时重新生成。未传或为空会返回 `210001`。

**注意事项**：
- `editable=false` 的块（图片/录音/附件/链接卡片/AI 生成块）只能作为 APPEND 锚点，对其下发 EDIT/DELETE 会返回 `210039`
- `block_id` 必须来自 `export_note_blocks`，不可凭空构造
- 虚拟锚点 `_begin_`（最前插入）/ `_end_`（末尾追加）配合 `action=3` 使用
- 列表整体（`id1..idN`）作为一个逻辑块：EDIT 替换整个列表，DELETE 删除整个列表

### 笔记本管理

| 用户意图 | 调用接口 | 关键参数 |
| -------- | -------- | -------- |
| 列出笔记本 | `list_notebook` | `cursor`(首页`"0"`)+`limit` |
| 创建笔记本 | `add_notebook` | `folder_name` |
| 重命名笔记本 | `rename_notebook` | `folder_id`+`new_folder_name` |

```bash
# 重命名笔记本
ima_api "openapi/note/v1/rename_notebook" '{"folder_id": "笔记本ID", "new_folder_name": "新名称"}'
```

### 导出笔记（export_note）

导出整篇笔记为文件，支持 Markdown / 纯文本 / JSON 三种格式。

```bash
ima_api "openapi/note/v1/export_note" '{"note_id": "笔记ID", "target_content_format": 1}'
```

- 返回 `data.content_url` 为带签名的 COS 下载链接（时效约 3 小时），需二次 `curl` 该链接获取实际内容
- `target_content_format`：`0`=纯文本 `.txt`，`1`=Markdown `.md`（推荐），`2`=JSON（Slate 编辑器 AST）`.json`
- 需要作者权限

### 智能推送（push_note）

不确定笔记是否已存在时使用：note_id 为空则新建，不为空则追加到该笔记。

```bash
ima_api "openapi/note/v1/push_note" '{"content": "标题：项目排期。正文内容..."}'
```

- `note_id` 可选（为空新建，不为空追加）；`content` 与 `content_cos_key` 不能同时为空
- 长内容可先 `ima_cos_util -f <文件>` 上传拿 cosKey，再传 `content_cos_key`
- 返回 `data.note_id`

### 重命名笔记（rename_note）

```bash
ima_api "openapi/note/v1/rename_note" '{"note_id": "笔记ID", "title": "新标题"}'
```

- 需要作者权限，返回空消息体

### 移动笔记（move_notes）

```bash
ima_api "openapi/note/v1/move_notes" '{"note_ids": ["笔记ID1", "笔记ID2"], "target_folder_id": "目标笔记本ID"}'
```

- `note_ids` 最多 100 条，`target_folder_name` 可选
- 返回 `data.result` map（key=note_id, value=true/false），可能部分成功，需逐条检查

### 按正文搜索

```bash
ima_api "openapi/note/v1/search_note" '{"search_type": 1, "query_info": {"content": "项目排期"}, "start": 0, "end": 20}'
```

## 核心响应字段

**搜索结果**（`SearchNoteInfo`）：笔记信息路径为 `search_note_infos` 包含 `NoteBookInfo`，关键字段：`note_id`、`title`、`summary`、`create_time`、`modify_time`、`note_ext_info.folder_id`、`note_ext_info.folder_name`。额外包含 `highlightInfo`（高亮匹配，key 为 `doc_title`，value 含 `<em>高亮词</em>`）。

**笔记列表条目**（`list_note` 响应数组字段是 `data.note_book_list`）：`NoteBookInfo` 关键字段：`note_id`、`title`、`summary`、`create_time`、`modify_time`、`cover_image`、`note_ext_info`（含 `folder_id`、`folder_name`）。

**读取正文**（`get_doc_content`）：正文在 `data.content`（纯文本/Markdown 由 `target_content_format` 决定）。

**笔记本条目**（`NoteFolderInfo`）：关键字段：`folder_id`、`name`、`note_number`、`create_time`、`modify_time`、`parent_folder_id`、`folder_type`（`0`=用户自建，`1`=全部笔记，`2`=未分类）。

**写入结果**（`import_doc`/`append_doc`）：返回 `note_id`（新建或目标笔记的唯一 ID）。

完整字段定义见 `references/api.md`。

## 分页

- **游标分页 — 笔记本列表**（`list_notebook`）：首次 `cursor: "0"`，后续用 `next_cursor`，`is_end=true` 时停止。
- **游标分页 — 笔记列表**（`list_note`）：首次 `cursor: ""`，`is_end=true` 时停止。
- **偏移量分页**（`search_note`）：首次 `start: 0, end: 20`，翻页时递增，`is_end=true` 时停止。

## 枚举值

- **`content_format`：** `0`=纯文本，`1`=Markdown，`2`=JSON。写入（`import_doc`/`append_doc`）目前仅支持 `1`（Markdown）。读取（`get_doc_content`）推荐 `0`（纯文本），Markdown 格式不支持。
- **`search_type`：** `0`=标题检索（默认），`1`=正文检索
- **`sort_type`：** `0`=更新时间（默认），`1`=创建时间，`2`=标题，`3`=大小（仅 `search_note_book` 使用）
- **`folder_type`：** `0`=用户自建，`1`=全部笔记（根目录），`2`=未分类

## 注意事项

- `folder_id` 不可为 `"0"`，根目录 ID 格式为 `user_list_{userid}`（从 `folder_type=1` 的笔记本条目获取）
- 笔记内容有大小上限，超过时返回 `100009`，可拆分为多次 `append_doc` 写入
- 直接调 `import_doc` / `append_doc` 不支持本地图片；需插入本地/远程图片时用 `notes/scripts/note-images.cjs`（详见上方「🖼️ 图片写入」章节）
- 展示笔记列表时只展示标题、摘要和修改时间，不要主动展示正文
- 时间字段是 Unix 毫秒时间戳，展示时转为可读格式
- 返回数据为嵌套结构：搜索结果取 `SearchNoteInfo[].note_book_info.note_id`，笔记本列表取 `NoteFolderInfo[].folder_id`，笔记列表取 `NoteBookInfo[].note_id`，注意按层级解析

## 错误处理

| 错误码 | 含义                   | 建议处理                     |
| ------ | ---------------------- | ---------------------------- |
| 100001 | 参数错误               | 检查请求参数格式和必填字段   |
| 100002 | 无效 ID                | 检查凭证配置                 |
| 100003 | 服务器内部错误         | 等待后重试                   |
| 100004 | size 不合法 / 空间不够 | 检查参数范围                 |
| 100005 | 无权限                 | 确认操作的是用户自己的笔记   |
| 100006 | 笔记已删除             | 告知用户该笔记不存在         |
| 100008 | 版本冲突               | 重新获取内容后再操作         |
| 100009 | 超过大小限制           | 拆分为多次 `append_doc` 写入 |
| 310001 | 笔记本不存在           | 检查 `folder_id` 是否正确    |
| 20002  | apiKey超过最大限频     |
| 20004  | apikey 鉴权失败        | 检查凭证配置是否正确         |

> 遇到笔记接口错误码（210039 / 100009 / 100005 等）或异常现象，先读 `references/troubleshooting.md` 对照定位；UTF-8 强制校验与跨模块规则见父级 SKILL.md。
