# 灏天文库 Skill 客户端

客户端用于调用服务端 API，供 OpenClaw 使用。所有脚本通过 `lib/api_client.py` 发送请求，自动附带 Token（`Authorization: Bearer <token>` 或配置在 `config.json`）。

## 这个技能能做什么

- 新建文集、新建文档
- 查询文集/文档列表与详情
- 更新文集/文档内容
- 设置文档父级（管理文档层级）
- 移动文档到其他文集
- 图片分组、上传图片到 COS、查询图片列表/详情与图片额度

## 配置

- 默认服务地址：`https://zzht.tech`
- `config.json`：只需配置 `token`（`server_base_url` 默认使用 `https://zzht.tech`）
- 或环境变量：只需配置 `HT_SKILL_TOKEN`（`HT_SKILL_SERVER_URL` 默认使用 `https://zzht.tech`）

环境变量示例（可替代 `config.json`）：

```bash
# Windows PowerShell
$env:HT_SKILL_TOKEN="你的个人Token"

# macOS / Linux
export HT_SKILL_TOKEN="你的个人Token"
```

---

## 个人 Token 获取方式

1. 登录灏天文库官网：[www.aiknowledge.cn](https://www.aiknowledge.cn)
2. 点击右上角头像，进入「个人中心」
3. 在 Token 信息区域查看并复制 `apiToken`
4. 将 Token 填入 `config.json` 的 `token` 字段

> 安全提醒：Token 等同于你的接口访问凭证，请勿泄露。若怀疑泄露，请在个人中心刷新 Token。

## 脚本与 API 对应关系

| 脚本 | HTTP 方法 | 路由地址 | 说明 |
|------|----------|----------|------|
| `create_collection.py` | POST | `/api/collections` | 新建文集 |
| `list_collections.py` | GET | `/api/collections` | 查询文集列表 |
| `get_collection.py` | GET | `/api/collections/{id}` | 查询文集详情 |
| `update_collection.py` | PATCH | `/api/collections/{id}` | 更新文集信息 |
| `set_document_parent.py` | PATCH | `/api/collections/{collection_id}/documents/{document_id}/parent` | 设置文档父级 |
| `add_document.py` | POST | `/api/documents` | 新建文档到指定文集 |
| `list_documents.py` | GET | `/api/documents` | 查询文档列表 |
| `get_document.py` | GET | `/api/documents/{id}` | 查询文档详情 |
| `update_document.py` | PATCH | `/api/documents/{id}` | 更新文档 |
| `move_document.py` | PATCH | `/api/documents/{id}/collection` | 修改文档归属（移动到目标文集） |
| `get_garden_limits_usage.py` | GET | `/api/garden/limits-usage` | 查询当前用户个人花园限制与用量 |
| `create_image_group.py` | POST | `/api/image-groups` | 创建图片分组 |
| `list_image_groups.py` | GET | `/api/image-groups` | 查询图片分组列表 |
| `update_image_group.py` | PATCH | `/api/image-groups/{id}` | 修改图片分组名称 |
| `get_image_limits_usage.py` | GET | `/api/images/limits-usage` | 查询图片上传额度与占用 |
| `upload_image.py` | POST | `/api/images/upload` | 上传图片（multipart） |
| `list_images.py` | GET | `/api/images` | 查询当前用户图片列表 |
| `get_image.py` | GET | `/api/images/{id}` | 查询图片详情 |
| `retrieve_documents.py` | POST | `/api/rag/retrieve` | 文档片段检索（RAG，不调用大模型） |

---

## 脚本参数说明

### create_collection.py — 新建文集

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | 是 | 文集名称 |
| `--description` | string | 否 | 文集简短介绍（50 字以内），默认「关于{name}的文集」 |
| `--brief` | string | 否 | 文集详细介绍 |
| `--get-if-exists` | flag | 否 | 若同名文集已存在则直接返回其 ID |

**请求体**：`{"name": "...", "description": "...", "brief": "...", "get_if_exists": bool}`

---

### list_collections.py — 查询文集列表

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | 否 | 按名称模糊搜索 |

**Query 参数**：`name`（可选）

---

### get_collection.py — 查询文集详情

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 文集 ID |
| `--include-docs` | flag | 否 | 是否包含完整文档列表 |

**路径参数**：`{id}`（文集 ID）  
**Query 参数**：`include_docs`（可选，默认 false）

---

### update_collection.py — 更新文集信息

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 文集 ID |
| `--name` | string | 否 | 新文集名称 |
| `--description` | string | 否 | 新简短介绍（50 字以内） |
| `--brief` | string | 否 | 新详细介绍 |

至少指定 `--name`、`--description`、`--brief` 之一。

**路径参数**：`{id}`  
**请求体**：`{"name": "...", "description": "...", "brief": "..."}`（均为可选）

---

### set_document_parent.py — 设置文档父级

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--collection-id` | int | 是 | 文集 ID |
| `--document-id` | int | 是 | 文档 ID |
| `--parent` | int | 是 | 父文档 ID，0 表示根文档 |
| `--sort` | int | 否 | 同级排序（如第一节=1、第二节=2），sort 越小越靠前 |

**路径参数**：`{collection_id}`、`{document_id}`  
**请求体**：`{"parent": int, "sort": int?}`

---

### add_document.py — 新建文档

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--collection-id` | int | 是 | 文集 ID |
| `--name` | string | 是 | 文档标题 |
| `--content` | string | 否 | 文档正文 |
| `--content-file` | path | 否 | 从文件读取正文（与 `--content` 二选一） |
| `--parent` | int | 否 | 父文档 ID，默认 0 |

**请求体**：`{"collection_id": int, "name": "...", "content": "...", "parent": int}`

---

### list_documents.py — 查询文档列表

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | 否 | 按文档名称模糊搜索 |
| `--collection-id` | int | 是 | 按文集 ID 筛选（必须提供） |

**Query 参数**：`name`（可选）、`collection_id`（必填）

---

### get_document.py — 查询文档详情

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 文档 ID |

**路径参数**：`{id}`（文档 ID）

---

### update_document.py — 更新文档

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 文档 ID |
| `--name` | string | 否 | 新文档标题 |
| `--content` | string | 否 | 新正文 |
| `--content-file` | path | 否 | 从文件读取并更新正文 |
| `--sort` | int | 否 | 排序值 |
| `--parent` | int | 否 | 父文档 ID |

至少指定 `--name`、`--content`、`--content-file`、`--sort`、`--parent` 之一。

**路径参数**：`{id}`  
**请求体**：`{"name": "...", "content": "...", "sort": int?, "parent": int?}`（均为可选）

---

### move_document.py — 修改文档归属

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 文档 ID |
| `--collection-id` | int | 是 | 目标文集 ID |
| `--from-collection-id` | int | 否 | 原文集 ID（若文档属于多个文集则必填） |

**路径参数**：`{id}`（文档 ID）  
**请求体**：`{"collection_id": int, "from_collection_id": int?}`

---

### get_garden_limits_usage.py — 查询个人花园限制与用量

无参数，直接调用：

```bash
python scripts/get_garden_limits_usage.py
```

返回内容包含：
- 个人花园限制：文集上限、每文集文档上限、单文档字数上限（仅统计 `source_type=garden` 文集）
- 会员状态：`membership.is_member`、`membership.member_status`（1=会员，2=非会员）；实际上限仍以 `limits` 为准
- 当前用量：当前文集数、总文档数、每个文集的文档占用情况、是否还能新建文集

---

### retrieve_documents.py — 文档片段检索（RAG）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--content` | string | 是 | 检索内容 |
| `--collection-ids` | string[] | 是 | 文集 ID 列表，从[灏天文库文集完整目录公开](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80)获取；支持 `21` 或 `collection_21`；最多 5 个 |

**请求体**：`{"content": "...", "collection_ids": ["189"]}`

**文集 ID 来源**：公开目录按分类列出 ID 与文集名称；勿用 `list_collections.py`（仅个人花园）。返回片段数量由服务端默认（10）；所有登录用户均可检索。超出 5 个文集时响应中会带 `warning` 字段。

---

### create_image_group.py — 创建图片分组

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | 是 | 分组名称（对应服务端 `group_name`） |

---

### list_image_groups.py — 查询图片分组

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--limit` | int | 否 | 每页条数，默认 100，服务端最大 200 |
| `--offset` | int | 否 | 偏移，默认 0 |

---

### update_image_group.py — 修改图片分组名称

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 分组 ID |
| `--name` | string | 是 | 新分组名称 |

---

### get_image_limits_usage.py — 查询图片额度与占用

无参数。返回 `max_images`、`max_image_size_mb`、`current_images`、`can_upload` 等。

---

### upload_image.py — 上传图片

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | path | 是 | 本地图片路径（相对路径相对 client 根目录解析） |
| `--remark` | string | 否 | 备注 |
| `--group-id` | int | 否 | 图片分组 ID（须属于当前用户） |

成功时响应 `data.file_url` 为外链地址（需服务端配置 `cos.public_base_url` 或 `cos.domain`）。

---

### list_images.py — 查询图片列表

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--group-id` | int | 否 | 按分组筛选 |
| `--name` | string | 否 | 文件名关键词（Query：`file_name`） |
| `--limit` | int | 否 | 默认 50，服务端最大 100 |
| `--offset` | int | 否 | 默认 0 |

---

### get_image.py — 查询图片详情

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--id` | int | 是 | 图片 ID |

---

## 使用示例

```bash
# 查询文集
python scripts/list_collections.py --name "我的文集"

# 新建文集（有则用、无则建）
python scripts/create_collection.py --name "学习笔记" --get-if-exists

# 新建文档
python scripts/add_document.py --collection-id 1 --name "第一章" --content "正文内容"
python scripts/add_document.py --collection-id 1 --name "第二章" --content-file ./chapter2.md

# 更新文档
python scripts/update_document.py --id 10 --content "新内容"
python scripts/update_document.py --id 10 --content-file ./new_content.md

# 设置文档层级
python scripts/set_document_parent.py --collection-id 1 --document-id 5 --parent 3 --sort 1

# 修改文档归属（移动到另一文集）
python scripts/move_document.py --id 10 --collection-id 2
python scripts/move_document.py --id 10 --collection-id 2 --from-collection-id 1  # 文档属于多文集时

# 查询当前用户个人花园限制与用量
python scripts/get_garden_limits_usage.py

# 文档片段检索（RAG，不调用大模型）
python scripts/retrieve_documents.py --content "什么是人工智能？" --collection-ids 21 22

# 图片：分组、额度、上传、列表、详情
python scripts/create_image_group.py --name "插图"
python scripts/list_image_groups.py
python scripts/get_image_limits_usage.py
python scripts/upload_image.py --file ./photo.png --remark "封面" --group-id 1
python scripts/list_images.py --group-id 1 --name "封面"
python scripts/get_image.py --id 100
```

---

## 常见问题（FAQ）

### 1) 报错「未配置 token」

请检查是否已在 `config.json` 写入 `token`，或是否正确设置了环境变量 `HT_SKILL_TOKEN`。

### 2) 报错「请求服务端失败」

优先检查网络连接；再确认服务地址是否为默认 `https://zzht.tech`。

### 3) 查询文档必须带 `--collection-id` 吗？

是的，`list_documents.py` 必须传 `--collection-id`。如果你不知道文集 ID，请先执行：

```bash
python scripts/list_collections.py --name "文集名称关键词"
```
