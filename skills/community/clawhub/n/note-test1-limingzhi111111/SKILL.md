---
name: ima-note
description: |
  IMA 个人笔记服务 API skill，用于管理用户的 IMA 笔记。支持搜索笔记、浏览笔记本、获取笔记内容、新建笔记和追加内容。
  当用户提到笔记、备忘录、记事、知识库，或者想要查找、阅读、创建、编辑笔记内容时，使用此 skill。
  即使用户没有明确说"笔记"，只要意图涉及个人文档的存取（如"帮我记一下"、"我之前写过一个关于XX的东西"、"把这段内容保存下来"），也应触发此 skill。
homepage: https://ima.qq.com
metadata:
  {
    "openclaw":
      { "emoji": "📝", "requires": { "env": ["IMA_OPENAPI_CLIENTID", "IMA_OPENAPI_APIKEY"] }, "primaryEnv": "IMA_OPENAPI_CLIENTID" },
  }
---

# ima-note

通过 IMA OpenAPI 管理用户个人笔记，支持读取（搜索、列表、获取内容）和写入（新建、追加）。

完整的数据结构和接口参数详见 `references/api.md`。

## Setup

1. 请打开 https://ima.qq.com/agent-interface 获取 **Client ID** 和 **App Key**
2. 存储凭证：

```bash
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```

也可以通过环境变量配置（agent 会按优先级依次尝试：环境变量 → 配置文件）：

```bash
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"
```

## 凭证预检

每次调用 API 前，先确认凭证可用。如果两个值都为空，停止操作并提示用户按 Setup 步骤配置。

```bash
IMA_CLIENT_ID="${IMA_OPENAPI_CLIENTID:-$(cat ~/.config/ima/client_id 2>/dev/null)}"
IMA_API_KEY="${IMA_OPENAPI_APIKEY:-$(cat ~/.config/ima/api_key 2>/dev/null)}"
if [ -z "$IMA_CLIENT_ID" ] || [ -z "$IMA_API_KEY" ]; then
  echo "缺少 IMA 凭证，请按 Setup 步骤配置 Client ID 和 App Key"
  exit 1
fi
```

## API 调用模板

所有请求统一为 **HTTP POST + JSON Body**，Base URL 为 `https://ima.qq.com/openapi/note/v1`。

定义辅助函数避免重复 header：

```bash
ima_api() {
  local endpoint="$1" body="$2"
  curl -s -X POST "https://ima.qq.com/openapi/note/v1/$endpoint" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$body"
}
```

> **隐私规则：** 笔记内容属于用户隐私，在群聊场景中只展示标题和摘要，禁止展示笔记正文。

## 接口决策表

| 用户意图 | 调用接口 | 关键参数 |
|---------|---------|---------|
| 搜索/查找笔记 | `search_note_book` | `query_info`（QueryInfo 对象）+ `start`(必填) + `end`(必填) |
| 查看笔记本列表 | `list_note_folder_by_cursor` | `cursor`(必填，首页传`"0"`) + `limit`(必填) |
| 浏览某笔记本里的笔记 | `list_note_by_folder_id` | `folder_id`(必填) + `cursor`(必填，首次传`""`) + `limit`(必填) |
| 读取笔记正文 | `get_doc_content` | `doc_id` + `target_content_format`(必填，推荐`0`纯文本) |
| 新建一篇笔记 | `import_doc` | `content` + `content_format`(必填，固定`1`) + 可选 `folder_id` |
| 往已有笔记追加内容 | `append_doc` | `doc_id` + `content` + `content_format`(必填，固定`1`) |

## 常用工作流

### 查找并阅读笔记

先搜索获取 `docid`，再用 `get_doc_content` 读取正文：

```bash
# 1. 按标题搜索
ima_api "search_note_book" '{"search_type": 0, "query_info": {"title": "会议纪要"}, "start": 0, "end": 20}'
# 从返回的 docs[].doc.basic_info.basic_info.docid 中取目标笔记 ID

# 2. 读取正文（纯文本格式，Markdown 格式目前不支持）
ima_api "get_doc_content" '{"doc_id": "目标docid", "target_content_format": 0}'
```

### 浏览笔记本里的笔记

先拉笔记本列表获取 `folder_id`，再拉该笔记本下的笔记：

```bash
# 1. 列出笔记本（首页 cursor 传 "0"）
ima_api "list_note_folder_by_cursor" '{"cursor": "0", "limit": 20}'

# 2. 拉取指定笔记本的笔记（首页 cursor 传 ""）
ima_api "list_note_by_folder_id" '{"folder_id": "user_list_xxx", "cursor": "", "limit": 20}'
```

### 新建笔记

```bash
# 新建到默认位置
ima_api "import_doc" '{"content_format": 1, "content": "# 标题\n\n正文内容"}'

# 新建到指定笔记本
ima_api "import_doc" '{"content_format": 1, "content": "# 标题\n\n正文内容", "folder_id": "笔记本ID"}'
# 返回 doc_id 和 doc_info，后续可用于 append_doc
```

### 追加内容到已有笔记

```bash
ima_api "append_doc" '{"doc_id": "笔记ID", "content_format": 1, "content": "\n## 补充内容\n\n追加的文本"}'
```

### 按正文搜索

```bash
ima_api "search_note_book" '{"search_type": 1, "query_info": {"content": "项目排期"}, "start": 0, "end": 20}'
```

## 核心响应字段

**搜索结果**（`SearchedDoc`）：笔记信息在 `doc.basic_info.basic_info` 下，关键字段：`docid`、`title`、`summary`、`tags`、`folder_name`、`create_time`（Unix 毫秒）、`modify_time`。额外包含 `highlight_info`（高亮匹配）和 `share_flag`。

**笔记本条目**（`NoteBookFolder`）：信息在 `folder.basic_info.basic_info` 下，关键字段：`folder_id`、`name`、`note_number`、`folder_type`（`0`=用户自建，`1`=全部笔记根目录，`2`=未分类）。

**笔记列表条目**（`NoteBookInfo`）：信息在 `basic_info.basic_info` 下，额外包含 `knowledge_exist_info`（知识库状态）和 `security_status`（安审状态）。

**写入结果**（`import_doc`/`append_doc`）：返回 `doc_id` 和完整的 `doc_info`（DocInfo 对象）。

完整字段定义见 `references/api.md`。

## 分页

- **游标分页 — 笔记本列表**（`list_note_folder_by_cursor`）：首次 `cursor: "0"`，后续用 `next_cursor`，`is_end=true` 时停止。支持 `version`/`next_version` 增量同步，`need_update` 判断是否有变化。
- **游标分页 — 笔记列表**（`list_note_by_folder_id`）：首次 `cursor: ""`，后续用 `next_cursor`，`is_end=true` 时停止。同样支持 `version` 增量同步。
- **偏移量分页**（`search_note_book`）：首次 `start: 0, end: 20`，翻页时递增，`query_id` 原样透传，`is_end=true` 时停止。

## 枚举值

- **`content_format`：** `0`=纯文本，`1`=Markdown，`2`=JSON。写入（`import_doc`/`append_doc`）目前仅支持 `1`（Markdown）。读取（`get_doc_content`）推荐 `0`（纯文本），Markdown 格式不支持。
- **`search_type`：** `0`=标题检索（默认），`1`=正文检索
- **`sort_type`：** `0`=更新时间（默认），`1`=创建时间，`2`=标题，`3`=大小（仅 `search_note_book` 使用）
- **`folder_type`：** `0`=用户自建，`1`=全部笔记（根目录），`2`=未分类

## 注意事项

- `folder_id` 不可为 `"0"`，根目录 ID 格式为 `user_list_{userid}`（从 `folder_type=1` 的笔记本条目获取）
- 笔记内容有大小上限，超过时返回 `100009`，可拆分为多次 `append_doc` 写入
- 展示笔记列表时只展示标题、摘要和修改时间，不要主动展示正文
- 时间字段是 Unix 毫秒时间戳，展示时转为可读格式
- 新协议返回的数据是嵌套结构（如 `doc.basic_info.basic_info.docid`），注意按层级解析

## 错误处理

| 错误码 | 含义 | 建议处理 |
|--------|------|---------|
| 0 | 成功 | — |
| 100001 | 参数错误 | 检查请求参数格式和必填字段 |
| 100002 | 无效 QBID | 检查凭证配置 |
| 100003 | 服务器内部错误 | 等待后重试 |
| 100004 | size 不合法 / 空间不够 | 检查参数范围 |
| 100005 | 无权限 | 确认操作的是用户自己的笔记 |
| 100006 | 笔记已删除 | 告知用户该笔记不存在 |
| 100008 | 版本冲突 | 重新获取内容后再操作 |
| 100009 | 超过大小限制 | 拆分为多次 `append_doc` 写入 |
| 310001 | 笔记本不存在 | 检查 `folder_id` 是否正确 |
| 20004 | appkey 鉴权失败 | 检查凭证配置是否正确 |
