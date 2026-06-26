# 获取 Scan Form 文档 — `temu.logistics.scanform.document.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_scanform_document_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.scanform.document.get`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.scanform.document.get` interface is for sellers to get scanform documents with package numbers.（卖家根据 **Scan Form 编号** 获取 Scan Form 文档下载 URL，用于打印交运扫描单（manifest）等。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：** **`scanFormSn`** 来自 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) 返回的 **`result.scanFormInfoList[].scanFormSn`**。若 Scan Form 状态异常，可先调用 **`temu.logistics.scanform.get`** 查看失败原因（错误码 **120016058**）。  
> 返回的 **`result.url`** 若为加签链接，可用本 skill 的 **`temu_eu_file_download.py`**（`POST /temu/fileDownload`）下载文件。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── scanFormSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| scanFormSn | STRING | **是** | Scan form serial number, the unique identification field when creating a scan form（Scan Form 序列号；创建 Scan Form 时的唯一标识，来自 **`temu.logistics.scanform.create`** 的 **`scanFormInfoList[].scanFormSn`**） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`scanFormSn`** 为必填。Partner **Request Example** CURL 将 **`scanFormSn`** 写在顶层，经 LinkFox 网关时建议放在 **`params.request.scanFormSn`**（与 Request 表一致）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "scanFormSn": "SF-20260101001"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 说明为 **Specific information**。  
**`result`** 子行在导出 HTML 中为折叠状态；下列字段来自 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)                    ← Specific information
    └── url (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |
| result | OBJECT | Specific information（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| url | STRING | Scan Form document URL（Scan Form 文档下载地址；用于打印或下载 manifest/扫描单文件。若为 Temu 加签 URL，须通过 **`temu_eu_file_download.py`** 按网关规范下载） |

> 调用成功时先判断 **`success === true`**，再使用 **`result.url`** 下载或打印 Scan Form 文档。USPS 等渠道完成 Scan Form 后，相关包裹面单 **`shipLabelPrintableTime`** 可能更新，可再查 [**`bg.logistics.shipment.result.get`**](./bg-logistics-shipment-result-get.md) 或 [**`bg.logistics.shipment.document.get`**](./bg-logistics-shipment-document-get.md)。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120016058 | The status of {*} is failed. Please check the failReason by "temu.logistics.scanform.get". | 调用 **`temu.logistics.scanform.get`** 查看 Scan Form 失败原因 |
| 120011070 | The {*} is invalid. Please check the request area or if the scanFormSn is nonexistent. | 核对 **`scanFormSn`** 是否存在、请求区域是否为 US |
| 120011001 | System abnormality, please check the data and try again | 检查入参后重试 |
| 120011002 | Invalid request parameters. | 确认 **`scanFormSn`** 已传入且格式正确 |

---

## 典型用法

```text
1. bg.logistics.shipment.create / result.get     → 购标成功 packageSn
2. temu.logistics.candidate.scanform.list.get    →（推荐）可合并包裹（见 [文档](./temu-logistics-candidate-scanform-list-get.md)）
3. temu.logistics.scanform.create                → 获得 scanFormSn
4. temu.logistics.scanform.document.get（本接口） → 获取 Scan Form 文档 url
5. temu_eu_file_download                         → 下载文档（若 url 为加签）
6. bg.logistics.shipment.document.get            → 再取包裹面单（USPS manifestation 后）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_scanform_document_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "scanFormSn": "SF-20260101001"
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.scanform.document.get",
  "params": {
    "request": {
      "scanFormSn": "SF-20260101001"
    }
  }
}'
```
