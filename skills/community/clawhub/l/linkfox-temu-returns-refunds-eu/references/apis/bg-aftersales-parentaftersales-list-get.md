# 父售后单列表查询 — `bg.aftersales.parentaftersales.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_returns_refunds_aftersales_parentaftersales_list_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.aftersales.parentaftersales.list.get`，业务载荷放在 Body 的 `params` |

**Description:** Query parent after-sales order list.

> 入参 **`createAtStart`/`createAtEnd`** 与 **`updateAtStart`/`updateAtEnd`** 至少提供一组时间范围（Partner Request 表说明）。
> 入参分页为 **`pageNo`**，出参当前页为 **`pageNumber`**，勿混用。
> 列表项中的 **`afterSalesStatusGroup`** 与入参筛选枚举一致（见下表）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageSize (INTEGER, 否)
    ├── pageNo (INTEGER, 否)
    ├── parentOrderSnList (STRING[], 否)
    ├── parentAfterSalesSnList (STRING[], 否)
    ├── createAtStart (INTEGER, 否)
    ├── createAtEnd (INTEGER, 否)
    ├── updateAtStart (INTEGER, 否)
    ├── updateAtEnd (INTEGER, 否)
    └── afterSalesStatusGroup (INTEGER, 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageSize | INTEGER | 否 | Page size for pagination, default is 10, max is 200. |
| pageNo | INTEGER | 否 | Page number for pagination, default is 1. |
| parentOrderSnList | STRING[] | 否 | The list of parent order numbers to limit the query. |
| parentAfterSalesSnList | STRING[] | 否 | The list of parent after-sales order numbers to limit the query. |
| createAtStart | INTEGER | 否 | The start time for querying the status change time of parent after-sales orders, in seconds (timestamp). Defines the starting range of the status change time when querying parent after-sales orders. |
| createAtEnd | INTEGER | 否 | The end time for querying the creation time of parent after-sales orders, in seconds (timestamp). Defines the ending range (closed interval) of the creation time when querying parent after-sales orders. -Must be used in conjunction with createAtStart. -- At least one set of creation or update times must be provided as required input parameters. |
| updateAtStart | INTEGER | 否 | The start time for querying the status change time of parent after-sales orders, in seconds (timestamp). Defines the starting range of the status change time when querying parent after-sales orders. |
| updateAtEnd | INTEGER | 否 | The end time for querying the status change time of parent after-sales orders, in seconds (timestamp). Defines the ending range (closed interval) of the status change time when querying parent after-sales orders. - Must be used in conjunction with updateAtStart. - At least one set of creation or update times must be provided as required input parameters. |
| afterSalesStatusGroup | INTEGER | 否 | The after-sales order status group, enumerated as follows: 1: Pending, 2: Requested, 3: Package Shipped, 4: Platform Reviewing, 5: Refunded, 6: Rejected, 7: Cancelled. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "afterSalesStatusGroup": 1,
    "createAtStart": 1714521600,
    "createAtEnd": 1714608000
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result
    ├── total (LONG)
    ├── pageNumber (INTEGER)
    └── data[]
        ├── parentAfterSalesSn (STRING)
        ├── afterSalesStatusGroup (INTEGER)
        ├── operateExpireTimeMs (LONG)
        ├── availableOperateList[] (INTEGER)
        ├── returnDeliveryType (INTEGER)
        ├── parentAfterSalesStatus (INTEGER)
        ├── parentOrderSn (STRING)
        ├── updateAt (INTEGER)
        ├── afterSalesType (INTEGER)
        └── createAt (INTEGER)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（见下表） |

### `data[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentAfterSalesSn | STRING | Parent after-sales order number（父售后单号） |
| afterSalesStatusGroup | INTEGER | The after-sales order status group（售后状态组），见下表 |
| operateExpireTimeMs | LONG | Operation expiration time in milliseconds（可操作截止时间，毫秒时间戳） |
| availableOperateList | INTEGER[] | List of available operations for the seller（卖家可执行操作列表，元素为操作码） |
| returnDeliveryType | INTEGER | Return delivery type（退货配送/交付方式类型） |
| parentAfterSalesStatus | INTEGER | Current parent after-sales status（父售后单当前状态码） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| updateAt | INTEGER | Last update time in seconds（最后更新时间，秒级 UNIX 时间戳） |
| afterSalesType | INTEGER | After-sales type（售后类型） |
| createAt | INTEGER | Creation time in seconds（创建时间，秒级 UNIX 时间戳） |

#### `afterSalesStatusGroup`（入参筛选 / 出参）

| 值 | 说明 |
|----|------|
| `1` | Pending |
| `2` | Requested |
| `3` | Package Shipped |
| `4` | Platform Reviewing |
| `5` | Refunded |
| `6` | Rejected |
| `7` | Cancelled |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_returns_refunds_aftersales_parentaftersales_list_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"pageNo": 1, "pageSize": 20, "afterSalesStatusGroup": 1, "createAtStart": 1714521600, "createAtEnd": 1714608000}}'
```

**典型流程：** 退货退款流程入口：按时间窗与 **`afterSalesStatusGroup`** 分页拉取父售后单 → 用 **`parentAfterSalesSn`** 调详情/子单列表/退货物流等接口。
