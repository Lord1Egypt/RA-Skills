# linkfox-amazon-store-uploads — API 参考

Uploads **v2020-11-01**，用于在调用 A+ Content、Messaging 等 API 之前**上传二进制文件**。

---

## 1. createUploadDestinationForResource

| 项 | 值 |
|----|-----|
| method | POST |
| path | `uploads/2020-11-01/uploadDestinations/{resource}` |
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

字段 **`uploadDestination`**，通常含：

- `uploadDestinationId` — 后续业务 API 引用
- `url` — PUT 上传地址
- `headers` — 上传时必须附带的 HTTP 头

---

## 2. 上传文件（非 SP-API 代理）

| 脚本 | `upload_to_destination.py` |
|------|---------------------------|
| method | PUT |
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

与 Amazon 要求一致：对文件字节做 MD5，再 **Base64** 编码摘要：

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

---

## 6. Feedback

`skillName`: **`linkfox-amazon-store-uploads`**
