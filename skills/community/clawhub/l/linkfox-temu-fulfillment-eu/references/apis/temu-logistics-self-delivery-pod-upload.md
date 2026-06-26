# 自配送 POD 上传 — `temu.logistics.self.delivery.pod.upload`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_self_fulfilled_logistics_self_delivery_pod_upload.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=39dce790742249f39998ee87eb75e5cf |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.self.delivery.pod.upload`，业务载荷放在 Body 的 `params` |

**Description:** Upload self-delivery POD proof URLs for packages (returns applySn per package).

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=order-shipping`**。  
> Partner 导出 HTML 中 **Response** 嵌套行多为折叠状态，下列 **Response** 层级按 **Response 表 + Response Example** 全部展开。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── podPackageInfoList (OBJECT[] **必填**)
    └── podPackageInfoList[].packageSn (STRING **必填**)
    └── podPackageInfoList[].proofUrlList (STRING[] **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| podPackageInfoList | OBJECT[] | **是** | POD Details |

#### `request.podPackageInfoList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | **是** | Package serial number（包裹号） |
| proofUrlList | STRING[] | **是** | POD proof image/document URL list（签收凭证 URL 列表） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "podPackageInfoList": [
      {
        "packageSn": "PKG-001",
        "proofUrlList": [
          "https://example.com/pod1.jpg"
        ]
      }
    ]
  }
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
    ├── resultList[] (OBJECT[])
    ├── resultList[].packageSn (STRING)
    ├── resultList[].applySn (STRING)
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
| resultList | OBJECT[] | 上传结果列表（按请求的 `podPackageInfoList` 逐条返回） |

#### `resultList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package serial number（包裹号，与请求一致） |
| applySn | STRING | Apply number（POD 申请单号；用于 **`temu.logistics.self.delivery.pod.audit.result.get`** 查询审核结果） |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_self_fulfilled_logistics_self_delivery_pod_upload.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "podPackageInfoList": [
      {
        "packageSn": "PKG-001",
        "proofUrlList": [
          "https://example.com/pod1.jpg"
        ]
      }
    ]
  }
}'
```
