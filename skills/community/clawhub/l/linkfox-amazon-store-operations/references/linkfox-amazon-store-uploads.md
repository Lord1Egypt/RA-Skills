---
name: linkfox-amazon-store-uploads
description: 亚马逊店铺文件上传预签名。为 A+ Content、Messaging 附件等功能生成文件上传所需的预签名 URL。
---

# Amazon 店铺 Uploads（文件上传）

本 skill 专用于向 Amazon 申请上传目的地并上传文件，与 `linkfox-amazon-store-auth` 同系列：先 `storeTokens`，再 `developerProxy` 调用 createUploadDestinationForResource，最后用 `upload_to_destination.py` 对返回的 URL 执行 PUT（不经网关）。参数与响应字段详见 [references/api.md](references/api.md)。

> 这是 Uploads API，不是 Orders 订单接口。订单见 `linkfox-amazon-store-orders`；批量 Feed 文件见 `linkfox-amazon-store-feeds`。

## 能力边界

### ✅ 能力范围

- 调用 Uploads API `createUploadDestinationForResource` 为 A+ Content、Messaging 等下游 API 生成上传目的地（`uploadDestinationId`、`url`、`headers`）。
- 向返回的预签名 `url` 执行 PUT 上传二进制文件（图片、附件等）。
- 自动计算文件内容的 Base64 MD5 摘要（`contentMD5`）。

### ❌ 边界与限制

- **依赖前置**：须先完成 `linkfox-amazon-store-auth` 的 `storeTokens`，否则认证失败。
- **不经网关上传**：`upload_to_destination.py` 直接 PUT 到返回 URL，不走 `developerProxy`。
- **`resource` 格式**：不得带前导 `/`；须与下游 API 文档一致。
- **字节一致性**：上传字节须与申请 `contentMD5` 时一致，否则校验失败。
- **不在范围内**：订单查询（用 `linkfox-amazon-store-orders`）；批量 Feed 文件（用 `linkfox-amazon-store-feeds`）；A+ Content / Messaging 业务接口本身只提供文件上传前置步骤。

## 执行流程

### 步骤 1：创建上传目的地

- 【输入】`sellerId`、`region`、`resource`（如 `aplus/2020-11-01/contentDocuments`）、`marketplaceId`、文件来源（`filePath` / `content` / `contentBase64`）、`contentType`。
- 【动作】运行 `scripts/create_upload_destination_for_resource.py`，脚本自动计算 `contentMD5`，经 `developerProxy` 调用 `createUploadDestinationForResource`。
- 【输出】`uploadDestination` 对象，含 `uploadDestinationId`、`url`、`headers`。

### 步骤 2：上传文件到预签名 URL

- 【输入】步骤 1 返回的 `uploadDestination`（`url` + `headers`）、待上传文件（`filePath` / `content` / `contentBase64`）。
- 【动作】运行 `scripts/upload_to_destination.py`，向 `url` 执行 PUT，并完整附带 `headers`。
- 【输出】上传成功后，在 A+ Content / Messaging 等下游 API 中以 `uploadDestinationId` 引用该文件。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见下方脚本一览）
- **成本约束**：本工具会消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-uploads-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；禁止写入 /tmp，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 前置条件

1. 依赖 `linkfox-amazon-store-auth`。
2. `resource` 须与下游 API 文档一致（例如 A+：`aplus/2020-11-01/contentDocuments`；Messaging 为对应 messages 资源路径）。
3. `contentMD5` 为待上传文件内容的 Base64 MD5 摘要；传 `filePath` / `content` 时脚本可自动计算。

## 脚本一览

| 脚本 | 说明 |
|------|------|
| `create_upload_destination_for_resource.py` | POST `uploads/2020-11-01/uploadDestinations/{resource}` |
| `upload_to_destination.py` | PUT 到返回的 `url`（带 `headers`） |
| `_spapi_uploads_common.py` | 内部公共模块 |

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 1) 创建上传目的地（自动根据 filePath 计算 contentMD5）
python scripts/create_upload_destination_for_resource.py '{
  "sellerId":"A1...",
  "region":"NA",
  "resource":"aplus/2020-11-01/contentDocuments",
  "marketplaceId":"ATVPDKIKX0DER",
  "filePath":"/path/to/banner.jpg",
  "contentType":"image/jpeg"
}'

# 2) 上传文件（将上一步 stdout 中的 uploadDestination 传入）
python scripts/upload_to_destination.py '{
  "uploadDestination": { "url": "...", "headers": { } },
  "filePath": "/path/to/banner.jpg"
}'
```

## 展示规则

1. 成功创建目的地常为 HTTP 201；先看 `developerProxy`，再看 `uploadDestination`。
2. `resource` 不要带前导 `/`；path 中会对 `/` 做编码。
3. 网关需放行 `uploads/2020-11-01/` 前缀。
4. 只呈现上传目的地上传结果数据，不做主观商业建议。

## 用户表达与场景速查

**适用** —— Amazon 店铺文件上传与预签名：

| 用户说 | 场景 |
|--------|------|
| "上传 A+ 图片"、"A+ Content 图片上传" | A+ Content 文件上传 |
| "上传 Messaging 附件" | 消息附件上传 |
| "生成预签名上传 URL"、"createUploadDestinationForResource" | 创建上传目的地 |
| "SP-API 上传文件"、"upload destination" | 上传目的地申请 |
| "contentMD5 上传校验" | 带 MD5 校验的上传 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

## 官方参考

[createUploadDestinationForResource](https://developer-docs.amazon.com/sp-api/reference/createuploaddestinationforresource) · [Create an upload destination](https://developer-docs.amazon.com/sp-api/docs/create-an-upload-destination)

---

# linkfox-amazon-store-uploads — API 参考

Uploads **v2020-11-01**，用于在调用 A+ Content、Messaging 等 API 之前上传二进制文件。

---

## 1. createUploadDestinationForResource

| 项 | 值 |
|----|-----|
| 请求方法 | POST |
| 路径 | `uploads/2020-11-01/uploadDestinations/{resource}` |
| 脚本 | `create_upload_destination_for_resource.py` |

`{resource}` 为下游 API 的资源路径（URL 编码），例如：

- `aplus/2020-11-01/contentDocuments`
- Messaging：`messaging/v1/orders/{amazonOrderId}/messages/...`（以官方为准）

### Query（写入 `queryString`）

| 参数 | 必填 | 说明 |
|------|------|------|
| marketplaceIds | 是 | 单站点 ID（脚本用 `marketplaceId` 或 `marketplaceIds[0]`） |
| contentMD5 | 是 | 文件内容的 Base64 MD5；或由 `filePath`/`content` 自动计算 |
| contentType | 否 | 如 `image/jpeg` |

### 入参 JSON（脚本）

| 字段 | 必填 |
|------|------|
| sellerId, region | 是 |
| resource | 是 |
| marketplaceId | 是 |
| contentMD5 或 filePath/content/contentBase64 | 是（二选一组合） |
| contentType | 建议 |

### 响应解析

字段 `uploadDestination`，通常含：

- `uploadDestinationId` — 后续业务 API 引用
- `url` — PUT 上传地址
- `headers` — 上传时必须附带的 HTTP 头

---

## 2. 上传文件（非 SP-API 代理）

| 项 | 值 |
|----|-----|
| 脚本 | `upload_to_destination.py` |
| 请求方法 | PUT |
| URL | `uploadDestination.url` |
| headers | `uploadDestination.headers` 全文带上 |

| 字段 | 必填 |
|------|------|
| uploadUrl 或 uploadDestination | 是 |
| headers（若未包在 uploadDestination 内） | 是 |
| filePath / content / contentBase64 | 是 |

**注意**：PUT 使用的字节须与申请 `contentMD5` 时一致。

---

## 3. contentMD5 计算

与 Amazon 要求一致：对文件字节做 MD5，再 Base64 编码摘要：

```python
base64.b64encode(hashlib.md5(data).digest()).decode("ascii")
```

---

## 4. 常见 resource 示例

| 场景 | resource 示例 |
|------|----------------|
| A+ 内容文档 | `aplus/2020-11-01/contentDocuments` |
| Messaging 附件 | 见 [Messaging API](https://developer-docs.amazon.com/sp-api/docs/messaging-api-v1-reference) 各 message 操作的 resource 说明 |

---

## 5. 错误与白名单

- **403**：Uploads 或下游角色未授权。
- **1005**：网关需放行 `uploads/2020-11-01/`。
- **429**：默认约 0.1 req/s（以官方为准）。

认证或积分类异常（401 / 402 / 余额不足提示）按 SKILL.md 的 **## 解决认证和积分问题** 处理。
