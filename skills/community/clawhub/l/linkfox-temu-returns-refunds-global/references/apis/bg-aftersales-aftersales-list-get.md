# 子售后单列表查询 — `bg.aftersales.aftersales.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_returns_refunds_aftersales_aftersales_list_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.aftersales.aftersales.list.get`，业务载荷放在 Body 的 `params` |

**Description:** Query after-sales order list by parent after-sales SN.

> **`parentAfterSalesSnList`** 为必填，通常来自 [bg-aftersales-parentaftersales-list-get](./bg-aftersales-parentaftersales-list-get.md)。
> 入参 **`pageNo`**，出参 **`pageNumber`**。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageSize (INTEGER, 否)
    ├── pageNo (INTEGER, 否)
    └── parentAfterSalesSnList (STRING[], 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageSize | INTEGER | 否 | Page size for pagination, default is 10, max is 200. |
| pageNo | INTEGER | 否 | Page number for pagination, default is 1. |
| parentAfterSalesSnList | STRING[] | **是** | The list of parent after-sales order numbers to limit the query. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "parentAfterSalesSnList": [
      "PAS-001"
    ]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── total (LONG)
    ├── pageNumber (INTEGER)
    └── data[]
        ├── parentAfterSalesSn (STRING)
        ├── productSkuId (LONG)
        ├── applyAfterSalesGoodsNumber (INTEGER)
        ├── afterSalesSn (STRING)
        ├── goodsId (LONG)
        ├── skuId (LONG)
        ├── productList[]
        │   ├── productSkuId (LONG)
        │   └── extCode (STRING)
        ├── afterSalesStatus (INTEGER)
        └── afterSalesType (INTEGER)
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
| productSkuId | LONG | Product SKU ID（商品 SKU ID） |
| applyAfterSalesGoodsNumber | INTEGER | Number of goods applied for after-sales（申请售后商品件数） |
| afterSalesSn | STRING | After-sales order number（子售后单号） |
| goodsId | LONG | Goods ID（商品 ID） |
| skuId | LONG | SKU ID |
| productList | OBJECT[] | Product SKU list（关联商品 SKU 列表） |
| afterSalesStatus | INTEGER | After-sales status（子售后单状态码） |
| afterSalesType | INTEGER | After-sales type（售后类型） |

#### `productList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| productSkuId | LONG | Product SKU ID |
| extCode | STRING | External code / merchant SKU code（商家外部编码） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_returns_refunds_aftersales_aftersales_list_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"pageNo": 1, "pageSize": 20, "parentAfterSalesSnList": ["PAS-001"]}}'
```

**典型流程：** 在取得 **`parentAfterSalesSn`** 后查询子售后行项（含 **`afterSalesSn`**、SKU 与 **`productList`**）。
