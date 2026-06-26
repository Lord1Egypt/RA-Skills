---
name: ima-skill
description: |
  统一IMA OpenAPI技能，支持笔记管理和知识库操作。
  触发：知识库、资料库、笔记、上传文件、添加网页、搜索内容。
homepage: https://ima.qq.com
metadata:
  openclaw:
    emoji: '🔧'
    requires: { env: ['IMA_OPENAPI_CLIENTID', 'IMA_OPENAPI_APIKEY'] }
    primaryEnv: 'IMA_OPENAPI_CLIENTID'
  security:
    credentials_usage: 凭证仅发往ima.qq.com
    allowed_domains: [ima.qq.com, '*.myqcloud.com']
    config_paths: ['~/.config/ima/client_id', '~/.config/ima/api_key']
---

# ima-skill

IMA笔记和知识库管理技能。

## 所需配置路径

- `~/.config/ima/client_id` (可选，IMA API 客户端 ID)
- `~/.config/ima/api_key` (可选，IMA API 密钥)

## 网络访问域名

- `ima.qq.com` (主要 API 服务)
- `*.myqcloud.com` (腾讯云 COS 文件上传服务)

## 安全说明

详细权限说明请参阅 [PERMISSIONS.md](PERMISSIONS.md)，包括：
- 配置文件访问说明
- 网络访问域名说明
- 凭证安全存储建议
- COS服务安全措施

## 模块路由

| 用户意图 | 模块 | 脚本 |
|----------|------|------|
| 搜索/浏览/读取笔记、追加到笔记 | notes | notes/scripts/notes-ops.cjs |
| 上传文件、添加网页、搜索/管理知识库 | knowledge-base | knowledge-base/scripts/kb-ops.cjs |

## 意图判断

| 用户说的 | 实际意图 | 路由 |
|----------|----------|------|
| "搜索我的笔记" | 搜索笔记 | notes → search |
| "新建一篇笔记" | 创建笔记 | notes → create |
| "追加到XX笔记" | 追加内容 | notes → append |
| "上传文件到知识库" | 上传文件 | kb (多步骤) |
| "添加到知识库" | 添加网页/笔记 | kb → add-urls/add-note |
| "搜索知识库内容" | 知识库搜索 | kb → search |

## 易混淆场景

| 用户说的 | 实际意图 | 路由 |
|----------|----------|------|
| "添加到知识库XX的笔记YY" | 追加到笔记 | notes → append |
| "把这篇笔记添加到知识库" | 关联笔记到知识库 | kb → add-note |
| "帮我记一下" | 需确认 | notes → 先询问 |

## 多语言调用方式

| 语言/环境 | 脚本 |
|-----------|------|
| Node.js | scripts/ima-api.cjs |
| Python | scripts/ima-api.py |

## 快速调用

### 笔记操作
```bash
node notes/scripts/notes-ops.cjs search --query "关键词"
node notes/scripts/notes-ops.cjs search --query "关键词" --type content
node notes/scripts/notes-ops.cjs list-folders
node notes/scripts/notes-ops.cjs list-notes --folder-id <id>
node notes/scripts/notes-ops.cjs read --doc-id <id>
node notes/scripts/notes-ops.cjs create --content "# 标题\n\n正文"
node notes/scripts/notes-ops.cjs append --doc-id <id> --content "\n\n补充内容"
```

### 知识库操作
```bash
node knowledge-base/scripts/kb-ops.cjs list-kbs
node knowledge-base/scripts/kb-ops.cjs list --kb-id <id>
node knowledge-base/scripts/kb-ops.cjs search --kb-id <id> --query "关键词"
node knowledge-base/scripts/kb-ops.cjs add-urls --kb-id <id> --urls "https://..."
node knowledge-base/scripts/kb-ops.cjs add-note --kb-id <id> --doc-id <笔记ID> --title "标题"
```

### 文件上传（完整5步）
```bash
node knowledge-base/scripts/preflight-check.cjs --file "/path/report.pdf"
node knowledge-base/scripts/check-repeated-names.cjs --kb-id "kb_xxx" --names "report.pdf:1"
node knowledge-base/scripts/create-media.cjs --kb-id "kb_xxx" --file-name "report.pdf" --file-size 1048576 --content-type "application/pdf" --file-ext "pdf"
node knowledge-base/scripts/cos-upload.cjs --file "/path/report.pdf" ...
node knowledge-base/scripts/add-knowledge.cjs --kb-id "kb_xxx" --media-type 1 --title "报告" --media-id "media_xxx" --cos-key "xxx" --file-size 1048576 --file-name "report.pdf"
```

## 凭证配置

获取：https://ima.qq.com/agent-interface

配置（二选一）：
```bash
# 环境变量
export IMA_OPENAPI_CLIENTID="id"
export IMA_OPENAPI_APIKEY="key"

# 配置文件（自动加载）
mkdir -p ~/.config/ima
echo "id" > ~/.config/ima/client_id
echo "key" > ~/.config/ima/api_key
```

## 通用错误码

| 码 | 含义 | 处理 |
|----|------|------|
| 0 | 成功 | — |
| 110001 | 参数非法 | 检查参数 |
| 110010 | 网络错误 | 可重试 |
| 110011 | 逻辑错误 | 不可重试 |
| 110021 | 频控 | 降低频率 |
| 110030 | 无权限 | 确认权限 |

> 响应字段为 `code`/`msg`，不是 `retcode`/`errmsg`

## 通用脚本参数

| 参数 | 说明 |
|------|------|
| `--json` | 输出完整JSON响应 |
| `--help` | 显示帮助信息 |

## 游标分页

适用于：list、search等接口
1. 首次：`cursor: ""`
2. 检查 `is_end`：`false`=还有更多
3. 用 `next_cursor` 继续
4. `is_end=true` 停止

## 实测经验

| 问题 | 解决方案 |
|------|----------|
| search_note_book空标题报错 | query_info.title不可为空 |
| import_urls根目录处理 | folder_id省略，不要传kb_id |
| 笔记搜索必须带关键词 | query_info至少一个非空字段 |

## 脚本列表

```
scripts/
  ima-api.cjs, ima-api.py

notes/scripts/
  notes-ops.cjs, notes-ops.py

knowledge-base/scripts/
  kb-ops.cjs, kb-ops.py
  preflight-check.cjs, check-repeated-names.cjs
  create-media.cjs, cos-upload.cjs, add-knowledge.cjs
```

## Python接口详细文档

### 环境准备
```bash
# 设置环境变量
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"

# 或创建配置文件
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```

---

### 一、笔记操作接口 (notes-ops.py)

#### 1. search - 搜索笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--query` | 是 | string | 搜索关键词 |
| `--type` | 否 | string | 搜索类型：`title`(标题) 或 `content`(内容)，默认 `title` |
| `--start` | 否 | int | 起始位置，默认 0 |
| `--end` | 否 | int | 结束位置，默认 20 |
| `--json` | 否 | flag | 输出完整JSON响应 |

**出参（JSON结构）：**
```json
{
  "is_end": true,           // 是否最后一页
  "total_hit_num": "6",     // 总命中数
  "docs": [                 // 笔记列表
    {
      "doc": {
        "basic_info": {
          "docid": "7439576008228970",
          "title": "笔记标题",
          "summary": "笔记摘要",
          "create_time": "1773733141678",
          "modify_time": "1773758324793",
          "status": 0,
          "folder_id": "",
          "folder_name": "",
          "summary_style": {}
        }
      }
    }
  ]
}
```

**示例：**
```bash
# 搜索标题包含"工作"的笔记
python3 notes/scripts/notes-ops.py search --query "工作"

# 搜索内容包含"会议"的笔记，输出JSON
python3 notes/scripts/notes-ops.py search --query "会议" --type content --json

# 分页搜索
python3 notes/scripts/notes-ops.py search --query "项目" --start 0 --end 10
```

#### 2. list-folders - 列出文件夹
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--cursor` | 否 | string | 分页游标，默认 "0" |
| `--limit` | 否 | int | 返回数量，默认 20 |
| `--json` | 否 | flag | 输出完整JSON响应 |

**出参（JSON结构）：**
```json
{
  "cursor": "next_cursor",
  "has_more": false,
  "folder_list": [
    {
      "folder_id": "folder_xxx",
      "folder_name": "文件夹名称",
      "create_time": "1773733141678",
      "modify_time": "1773758324793"
    }
  ]
}
```

#### 3. list-notes - 列出笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--folder-id` | 否 | string | 文件夹ID，不指定则列出所有笔记 |
| `--cursor` | 否 | string | 分页游标，默认 "" |
| `--limit` | 否 | int | 返回数量，默认 20 |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 4. read - 读取笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--doc-id` | 是 | string | 笔记文档ID |
| `--format` | 否 | int | 格式：0=文本(默认)，1=HTML |
| `--json` | 否 | flag | 输出完整JSON响应 |

**出参（JSON结构）：**
```json
{
  "doc": {
    "basic_info": {
      "docid": "7439576008228970",
      "title": "笔记标题",
      "summary": "摘要",
      "create_time": "1773733141678",
      "modify_time": "1773758324793"
    },
    "content": "笔记完整内容"
  }
}
```

#### 5. create - 创建笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--title` | 是 | string | 笔记标题 |
| `--body` | 是 | string | 笔记内容 |
| `--folder-id` | 否 | string | 目标文件夹ID |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 6. append - 追加到笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--doc-id` | 是 | string | 笔记文档ID |
| `--body` | 是 | string | 要追加的内容 |
| `--json` | 否 | flag | 输出完整JSON响应 |

---

### 二、知识库操作接口 (kb-ops.py)

#### 1. list-kbs - 列出所有知识库
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--query` | 否 | string | 搜索关键词 |
| `--json` | 否 | flag | 输出完整JSON响应 |

**出参（JSON结构）：**
```json
{
  "info_list": [
    {
      "id": "64VbjCXIm3XittrNBDZxkwI5I4KV9suC5LQYa6wGuDY=",
      "name": "知识库名称",
      "cover_url": "https://ima-media-pub-prod.image.myqcloud.com/..."
    }
  ]
}
```

#### 2. get-kb - 获取知识库信息
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 3. list - 列出知识库内容
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--query` | 否 | string | 搜索关键词 |
| `--cursor` | 否 | string | 分页游标，默认 "" |
| `--limit` | 否 | int | 返回数量，默认 50 |
| `--json` | 否 | flag | 输出完整JSON响应 |

**出参（JSON结构）：**
```json
{
  "is_end": true,
  "next_cursor": "",
  "doc_list": [
    {
      "doc_id": "doc_xxx",
      "title": "文档标题",
      "summary": "文档摘要",
      "create_time": "1773733141678",
      "modify_time": "1773758324793",
      "media_type": "document"
    }
  ]
}
```

#### 4. search - 搜索知识库
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--query` | 是 | string | 搜索关键词 |
| `--cursor` | 否 | string | 分页游标，默认 "" |
| `--limit` | 否 | int | 返回数量，默认 20 |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 5. create-kb - 创建知识库
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--name` | 是 | string | 知识库名称 |
| `--desc` | 否 | string | 知识库描述 |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 6. delete-kb - 删除知识库
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 7. create-note - 创建知识库笔记
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--title` | 是 | string | 笔记标题 |
| `--body` | 是 | string | 笔记内容 |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 8. add-urls - 添加网页到知识库
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--kb-id` | 是 | string | 知识库ID |
| `--urls` | 是 | string | 网页URL，多个用逗号分隔 |
| `--json` | 否 | flag | 输出完整JSON响应 |

#### 9. import-urls - 导入网页
**入参：**
| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `--urls` | 是 | string | 网页URL，多个用逗号分隔 |
| `--folder-id` | 否 | string | 目标文件夹ID，不指定则导入到根目录 |
| `--json` | 否 | flag | 输出完整JSON响应 |

---

### 三、通用API调用 (ima-api.py)

#### 用法：
```bash
python3 scripts/ima-api.py --path <API路径> --body <JSON字符串> [--json]
```

#### 常用API路径：
| 接口 | 路径 | 说明 |
|------|------|------|
| 搜索笔记 | `openapi/note/v1/search_note_book` | 搜索笔记 |
| 列出知识库 | `openapi/wiki/v1/search_knowledge_base` | 获取知识库列表 |
| 获取知识库内容 | `openapi/wiki/v1/search_knowledge` | 搜索知识库内容 |

#### 示例：
```bash
# 搜索笔记
python3 scripts/ima-api.py --path openapi/note/v1/search_note_book \
  --body '{"search_type":0,"query_info":{"title":"工作"},"start":0,"end":20}'

# 列出知识库
python3 scripts/ima-api.py --path openapi/wiki/v1/search_knowledge_base \
  --body '{"limit":50}'
```

---

### 四、错误码说明

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| 110001 | 参数非法 | 检查参数格式 |
| 110010 | 网络错误 | 可重试 |
| 110011 | 逻辑错误 | 检查业务逻辑 |
| 110021 | 频控 | 降低调用频率 |
| 110030 | 无权限 | 确认权限设置 |

---

### 五、调用技巧

1. **环境检查**：调用前检查环境变量或配置文件
2. **参数验证**：使用 `--help` 查看参数格式
3. **分页处理**：大数据量使用游标分页
4. **JSON解析**：添加 `--json` 参数获取完整响应
5. **错误处理**：网络错误可重试，参数错误需检查

---

### 六、快速调用示例

#### 笔记操作：
```bash
# 搜索笔记
python3 notes/scripts/notes-ops.py search --query "关键词" --json

# 读取笔记
python3 notes/scripts/notes-ops.py read --doc-id "doc_xxx" --json

# 创建笔记
python3 notes/scripts/notes-ops.py create --title "标题" --body "内容"
```

#### 知识库操作：
```bash
# 列出知识库
python3 knowledge-base/scripts/kb-ops.py list-kbs --json

# 搜索知识库
python3 knowledge-base/scripts/kb-ops.py search --kb-id "kb_xxx" --query "关键词" --json

# 创建知识库笔记
python3 knowledge-base/scripts/kb-ops.py create-note --kb-id "kb_xxx" --title "标题" --body "内容"
```
