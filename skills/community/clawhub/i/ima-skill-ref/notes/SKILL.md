# Notes

笔记管理模块：搜索、浏览、读取、新建、追加。

## 脚本调用（推荐）

前置：`IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` 或 `~/.config/ima/{client_id,api_key}`

### search - 搜索笔记
```
node notes/scripts/notes-ops.cjs search --query <关键词> [--type title|content] [--start 0] [--end 20] [--json]
```
| 参数 | 必填 | 说明 |
|------|------|------|
| `--query` | ✅ | 搜索关键词 |
| `--type` | ❌ | `title`(默认) 或 `content` |
| `--start` | ❌ | 起始位置，默认0 |
| `--end` | ❌ | 结束位置，默认20 |

### list-folders - 列出笔记本
```
node notes/scripts/notes-ops.cjs list-folders [--cursor "0"] [--limit 20] [--json]
```

### list-notes - 浏览笔记本内的笔记
```
node notes/scripts/notes-ops.cjs list-notes [--folder-id <id>] [--cursor ""] [--limit 20] [--json]
```
| 参数 | 必填 | 说明 |
|------|------|------|
| `--folder-id` | ❌ | 空=全部笔记 |

### read - 读取笔记正文
```
node notes/scripts/notes-ops.cjs read --doc-id <id> [--format 0] [--json]
```

### create - 新建笔记
```
node notes/scripts/notes-ops.cjs create --content <markdown> [--title <标题>] [--json]
```
| 参数 | 必填 | 说明 |
|------|------|------|
| `--content` | ✅ | Markdown正文 |
| `--title` | ❌ | 标题（会自动加#前缀） |

### append - 追加到已有笔记
```
node notes/scripts/notes-ops.cjs append --doc-id <id> --content <追加内容> [--json]
```
⚠️ 追加会不可撤销修改用户笔记，**必须先确认目标笔记**。

## 手动API调用

API路径：`openapi/note/v1`

凭证处理已封装在脚本中，手动调用时需自行处理：
```bash
# Bash
curl -X POST "https://ima.qq.com/openapi/note/v1/<endpoint>" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" -d '<body>'
```

### 关键参数
| 字段 | 值 | 说明 |
|------|-----|------|
| content_format | 1 | Markdown格式（写入必须用1） |
| search_type | 0 | 按标题搜索 |
| search_type | 1 | 按正文搜索 |
| query_info.title | 字符串 | 标题搜索词（**不可为空**） |

### 响应格式
```json
{ "code": 0, "msg": "...", "data": {...} }
```
- code=0：成功，从 `data` 提取字段
- code≠0：失败，展示 `msg`

### 核心字段路径
| 数据 | 路径 |
|------|------|
| 搜索结果docid | data.docs[].doc.basic_info.docid |
| 笔记标题 | data.docs[].doc.basic_info.title |
| 笔记本folder_id | note_book_folders[].folder.basic_info.folder_id |

## 注意事项

- `folder_id` 不可为"0"，根目录ID格式 `user_list_{userid}`
- 笔记有大小上限(100009)，超限需拆分多次append
- 本地图片不支持(`file:///...`)，过滤并告知用户
