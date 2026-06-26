# 自配送 POD 审核结果查询 — `temu.logistics.self.delivery.pod.audit.result.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_self_fulfilled_logistics_self_delivery_pod_audit_result_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=e7ada01f9b044cf98adc4e5a6ebcfd62 |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.self.delivery.pod.audit.result.get`，业务载荷放在 Body 的 `params` |

**Description:** Query self-delivery POD (proof of delivery) audit/review results by apply numbers.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=order-shipping`**。  
> Partner 导出 HTML 中 **Response** 嵌套行多为折叠状态，下列 **Response** 层级按 **Response 表 + Response Example** 全部展开。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── applySnList (STRING[] **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| applySnList | STRING[] | **是** | Apply number. Maximum supported queries: 100. |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "applySnList": [
      "APPLY_SN_1",
      "APPLY_SN_2"
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
    ├── resultList[].reviewStatus (INTEGER)
    ├── resultList[].rejectedReasonList[] (STRING[])
    ├── resultList[].applyTime (STRING)
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
| resultList | OBJECT[] | POD 审核结果列表 |

#### `resultList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package serial number（包裹号） |
| applySn | STRING | Apply number（POD 申请单号，由 **`temu.logistics.self.delivery.pod.upload`** 返回） |
| reviewStatus | INTEGER | Review status（审核状态；具体枚举以 Partner 在线 Response 表为准，Example 为 `1`） |
| rejectedReasonList | STRING[] | Rejected reason list（审核未通过时的拒绝原因列表） |
| applyTime | STRING | Apply time（申请/提交时间） |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_self_fulfilled_logistics_self_delivery_pod_audit_result_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "applySnList": [
      "APPLY_SN_1",
      "APPLY_SN_2"
    ]
  }
}'
```
