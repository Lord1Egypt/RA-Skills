# Knowledge Base

知识库管理模块：浏览、搜索、上传文件、添加网页/笔记。

## 脚本调用（推荐）

前置：`IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` 或 `~/.config/ima/{client_id,api_key}`

### list - 浏览知识库内容
```
node knowledge-base/scripts/kb-ops.cjs list --kb-id <知识库ID> [--query <搜索词>] [--cursor ""] [--limit 50] [--json]
```

### search - 在知识库中搜索
```
node knowledge-base/scripts/kb-ops.cjs search --kb-id <知识库ID> --query <搜索词> [--cursor ""] [--limit 20] [--json]
```

### list-kbs - 列出所有知识库
```
node knowledge-base/scripts/kb-ops.cjs list-kbs [--query <搜索词>] [--json]
```

### get-kb - 获取知识库信息
```
node knowledge-base/scripts/kb-ops.cjs get-kb --kb-id <知识库ID> [--json]
```

### add-urls - 添加网页/微信文章
```
node knowledge-base/scripts/kb-ops.cjs add-urls --kb-id <知识库ID> --urls <url1,url2> [--folder-id <folderID>] [--json]
```

### add-note - 将笔记关联到知识库
```
node knowledge-base/scripts/kb-ops.cjs add-note --kb-id <知识库ID> --doc-id <笔记ID> --title <标题> [--folder-id <folderID>] [--json]
```

## 文件上传（完整流程）

文件上传需按以下顺序执行脚本，不可跳过：

```
1. preflight-check.cjs        → 文件检测（类型/大小）
2. check-repeated-names.cjs    → 重名检查
3. create-media.cjs            → 创建媒体+获取COS凭证
4. cos-upload.cjs               → 上传到COS
5. add-knowledge.cjs           → 添加到知识库
```

### 完整示例

```bash
# 1. 文件检测
PREFLIGHT=$(node knowledge-base/scripts/preflight-check.cjs --file "/path/report.pdf")
# 解析结果提取 file_name, file_size, media_type, content_type

# 2. 重名检查
node knowledge-base/scripts/check-repeated-names.cjs \
  --kb-id "kb_xxx" \
  --names "report.pdf:1"

# 3. 创建媒体
CREATE_MEDIA=$(node knowledge-base/scripts/create-media.cjs \
  --kb-id "kb_xxx" \
  --file-name "report.pdf" \
  --file-size 1048576 \
  --content-type "application/pdf" \
  --file-ext "pdf" \
  --json)
# 解析结果提取 media_id 和 cos_credential

# 4. COS上传（使用create-media返回的凭证）
node knowledge-base/scripts/cos-upload.cjs \
  --file "/path/report.pdf" \
  --secret-id "xxx" \
  --secret-key "xxx" \
  --token "xxx" \
  --bucket "bucket-xxx" \
  --region "ap-guangzhou" \
  --cos-key "xxx" \
  --content-type "application/pdf"

# 5. 添加到知识库
node knowledge-base/scripts/add-knowledge.cjs \
  --kb-id "kb_xxx" \
  --media-type 1 \
  --title "产品报告" \
  --media-id "media_xxx" \
  --cos-key "xxx" \
  --file-size 1048576 \
  --file-name "report.pdf"
```

详见各脚本的 `--help` 查看详细用法。

## 手动API调用

API路径：`openapi/wiki/v1`

凭证处理已封装在脚本中，手动调用时需自行处理：
```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/<endpoint>" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" -d '<body>'
```

### 关键参数
| 字段 | 值 | 说明 |
|------|-----|------|
| media_type | 1 | PDF |
| media_type | 3 | Word |
| media_type | 4 | PPT |
| media_type | 5 | Excel |
| media_type | 7 | Markdown |
| media_type | 9 | 图片 |
| media_type | 11 | 笔记 |
| media_type | 13 | TXT |
| media_type | 14 | Xmind |
| media_type | 15 | 音频 |
| folder_id | folder_xxx | 文件夹ID（根目录省略此字段） |

### 响应格式
```json
{ "code": 0, "msg": "...", "data": {...} }
```
- code=0：成功，从 `data` 提取字段
- code≠0：失败，展示 `msg`

### 核心字段路径
| 数据 | 路径 |
|------|------|
| 知识库列表 | data.list[].id/name/description |
| 知识条目 | data.list[].media_id/title |
| 搜索高亮 | data.results[].highlight_content |
| COS凭证 | data.cos_info.secret_id/secret_key/token/bucket/region |

## 文件夹操作

| 场景 | 方法 |
|------|------|
| 用户给了文件夹ID | 直接用 |
| 用户只给文件夹名 | search_knowledge 搜名称，找folder_xxx |

**规则：**
- 根目录时：**省略folder_id字段**
- folder_id以`folder_`开头
- 不要将knowledge_base_id作为folder_id传入

## URL类型判断

| URL模式 | 类型 | 处理 |
|---------|------|------|
| mp.weixin.qq.com/s/ | 微信公众号 | add-urls |
| bilibili.com/video/ | 视频 | 不支持 |
| youtube.com/watch | 视频 | 不支持 |
| 含文件扩展名(.pdf/.docx) | 文件型 | 走上传流程 |
| 其他 | 普通网页 | add-urls |

## 注意事项

- 视频文件(.mp4等)仅桌面端支持
- 文件大小限制：Excel/TXT/Xmind/MD 10MB，图片 30MB，其他 200MB
- 重名时需询问用户处理方式
