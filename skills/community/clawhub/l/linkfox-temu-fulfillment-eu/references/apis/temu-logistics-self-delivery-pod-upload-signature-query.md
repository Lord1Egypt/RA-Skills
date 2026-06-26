# 自配送 POD 上传签名查询 — `temu.logistics.self.delivery.pod.upload.signature.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_self_fulfilled_logistics_self_delivery_pod_upload_signature_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=b42a002b6a3d42a58aa809cfc1ea14fd |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.self.delivery.pod.upload.signature.query`，业务载荷放在 Body 的 `params` |

**Description:** Get upload signature for self-delivery POD file upload to Temu storage.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=order-shipping`**。  
> Partner 导出 HTML 中 **Response** 嵌套行多为折叠状态，下列 **Response** 层级按 **Response 表 + Response Example** 全部展开。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
```



### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {}
}
```

> Partner **Request Example** CURL 可能将业务字段写在顶层（如 `applySnList`）；经 LinkFox 网关请放在 **`params.request`**（或脚本接受的顶层 `request` 字段，由 `_eu_fulfillment_script` 转发）。

---

## Response（Temu `body` 解析后）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── signature (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | 业务结果 |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| signature | STRING | Upload signature（POD 凭证文件上传至 Temu 存储所需的签名；上传完成后将文件 URL 填入 **`temu.logistics.self.delivery.pod.upload`** 的 `proofUrlList`） |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_self_fulfilled_logistics_self_delivery_pod_upload_signature_query.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {}
}'
```
