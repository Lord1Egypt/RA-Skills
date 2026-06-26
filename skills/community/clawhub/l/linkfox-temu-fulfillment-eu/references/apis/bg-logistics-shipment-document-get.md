# 获取面单/运单文档 — `bg.logistics.shipment.document.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_shipment_document_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.document.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.document.get` interface is for sellers to obtain the express delivery waybill which has been fulfilled successfully by Temu-integrated channel so as to facilitate the printing of the express delivery waybill and the package out of the warehouse.

（卖家获取已通过 **Temu 集成物流渠道** 成功履约包裹的**快递面单/运单文档 URL**，用于打印面单、包裹出库。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`packageSnList`** 来自 **`bg.logistics.shipment.create`** 或 **`bg.logistics.shipment.result.get`**（购标成功 **`shippingLabelStatus=1`**）。  
> - 须在订单 **`earliestTimeGetShippingDocument`** 之后调用（错误码 **120012038**）。  
> - USPS 等渠道可能须先完成 **manifestation**；可通过 **`bg.logistics.shipment.result.get`** 查看 **`shipLabelPrintableTime`**，或使用 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) / 卖家中心 Scan Form（错误码 **120018012**）。  
> 返回的 **`url`** 若为加签链接，可用本 skill 的 **`temu_eu_file_download.py`**（`POST /temu/fileDownload`）下载 PDF/PNG 文件。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── documentType (STRING, 选填)
    └── packageSnList[] (STRING[], 选填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| documentType | STRING | 否 | Document Type（面单文档类型），见下表 |
| packageSnList | STRING[] | 否 | Package List that needs to get the shipping label（需要获取面单的包裹号列表） |

#### `documentType`

| 值 | 说明 |
|----|------|
| `SHIPPING_LABEL_PDF` | The document URL will return the shipping label in **PDF** format for all the carriers you choose（返回 PDF 格式面单；**推荐使用**） |
| `SHIPPING_LABEL_PNG` | The document URL will return the shipping label in **PNG** format for all the carriers you choose（返回 PNG 格式面单） |
| 不传 | The document URL will return the shipping label in PDF format or PNG format **based on which carrier you choose**（按承运商默认返回 PDF 或 PNG） |

> 官方 Request 表将 **`request`**、**`documentType`**、**`packageSnList`** 均标为选填（False）；实际调用须传入有效 **`packageSnList`**（错误码 **120018027**）。Partner **Request Example** CURL 将字段写在顶层，经 LinkFox 网关时建议放在 **`params.request`** 下。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "documentType": "SHIPPING_LABEL_PDF",
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`。**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── shippingLabelUrlList[] (OBJECT[])
    │   ├── packageSn
    │   ├── documentType
    │   └── url
    └── warningMessage[] (STRING[])
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shippingLabelUrlList | OBJECT[] | 面单文档 URL 列表（每个元素对应一个 **`packageSn`** 的可打印面单链接） |
| warningMessage | STRING[] | Warning messages（警告信息列表；部分包裹成功、部分有提示时可能出现，见 Response Example） |

#### `shippingLabelUrlList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package SN（包裹号；与请求 **`packageSnList`** 中项对应） |
| documentType | STRING | Document type actually returned（实际返回的文档类型，如 **`SHIPPING_LABEL_PDF`** / **`SHIPPING_LABEL_PNG`**） |
| url | STRING | Document download URL（面单/运单文档下载地址；用于打印或经 **`temu_eu_file_download.py`** 拉取文件） |

#### `warningMessage[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| （元素） | STRING | 单条警告文案（Partner 未在 Response 表展开子字段；示例为字符串数组） |

> 调用成功时先判断 **`response.success === true`**，再遍历 **`result.shippingLabelUrlList`** 取 **`url`** 打印或下载。若 **`warningMessage`** 非空，须阅读警告内容（可能部分包裹未返回 URL 或需额外操作）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120018027 | The packageSn is invalid. Please check the request area or if the packageSn is nonexistent etc. | 核对 **`packageSn`** 与站点 |
| 120012038 | Order can only get shipping document after the "earliestTimeGetShippingDocument". | 等待订单到达可获取面单时间后再调 |
| 120018012 | USPS labels require manifestation before printing. Check 'shipLabelPrintableTime' via 'bg.logistics.shipment.result.get' or use 'temu.logistics.scanform.create'/Seller Central Scan Form to update immediately. | 先查 **`shipLabelPrintableTime`** 或调用 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) |
| 120018075 | The package {*} only supports shipping from cooperative warehouses and restricts the printing of shippingLabel | 合作仓包裹限制打印面单 |
| 120011030 | Cooperative warehouse order fulfillment restricted. | 合作仓履约受限 |
| 120018010 | The packages {*} have been canceled. Please fulfill again by Temu non-integrated logistics or Temu integrated logistics. | 包裹已取消，需重新履约 |

---

## 典型用法

```text
1. bg.logistics.shipment.create              → packageSnList
2. bg.logistics.shipment.result.get          → shippingLabelStatus=1，确认可打印时间
3. bg.logistics.shipment.document.get        → shippingLabelUrlList[].url
4. temu_eu_file_download.py（可选）         → 下载加签 PDF/PNG
5. 打印面单 / 出库
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_shipment_document_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "documentType": "SHIPPING_LABEL_PDF",
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}'
```

```bash
# 下载面单（若 url 需网关加签下载）
python scripts/temu_eu_file_download.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "url": "<shippingLabelUrlList[].url>"
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.document.get",
  "params": {
    "request": {
      "packageSnList": ["PKG-001"]
    }
  }
}'
```
