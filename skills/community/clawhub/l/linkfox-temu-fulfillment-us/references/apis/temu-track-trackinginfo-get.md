# 物流轨迹详情查询 — `temu.track.trackinginfo.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_tracking_track_trackinginfo_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=e8a433cf16604acf82e20af25672cec0&sub_menu_code=e4ec6bc629bf42e38346de78b297d349 |
| **网关** | `POST /temu/proxy`，`type`=`temu.track.trackinginfo.get`，业务载荷放在 Body 的 `params` |

**Description:** Logistics trajectory detail query interface.（物流轨迹详情查询接口：按 **packageSn** 查询包裹的物流跟踪号及轨迹节点列表。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **关联能力：** **`packageSn`** 来自 **`linkfox-temu-fulfillment-us`**（如 **`bg.logistics.shipment.create`** / **`bg.logistics.shipment.result.get`**）；订单上下文见 **`linkfox-temu-order-us`**。  
> **`language`** 用于轨迹文案语言；不支持的语言将报错 **170070012**（见 Partner **TEMU Logistics Tracking API Documentation** 指南）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── packageSn (STRING, 选填)
    └── language (STRING, 选填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | 否 | packageSn（Temu 包裹号；购标/履约后由 **`bg.logistics.shipment.create`** 等返回，用于查询该包裹的物流轨迹） |
| language | STRING | 否 | language（轨迹节点 **`statusText`** 等展示语言的 locale/语言代码；须为平台支持的语言，否则报错 **170070012 Unsupported languages, {*}`**） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），且 **`packageSn`**、**`language`** 在表中亦为选填；实际查询须传入有效的 **`packageSn`**（及按需的 **`language`**）。Partner **Request Example** CURL 将 **`packageSn`**、**`language`** 写在 JSON 顶层，经 LinkFox 网关时建议放在 **`params.request`**（与 Request 表结构一致）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSn": "PKG-001",
    "language": "en"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象。  
**`result`** 子行在导出 HTML 中为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── packageSn (STRING)
    ├── trackingNum (STRING)
    └── trackingInfo[] (OBJECT[])
        ├── logisticsStatus (STRING)
        ├── logisticsUpdatedAt (STRING)
        └── statusText (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（物流轨迹详情） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | packageSn（包裹号；与请求 **`packageSn`** 对应） |
| trackingNum | STRING | Tracking number（物流运单号/跟踪号；Partner **Response Example** 字段名为 **`trackingNum`**） |
| trackingInfo | OBJECT[] | Logistics tracking information list（物流轨迹节点列表，按时间顺序展示承运商扫描/状态更新） |

#### `trackingInfo[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| logisticsStatus | STRING | Logistics status code（物流状态码；承运商/平台内部状态标识，具体枚举以 Temu 与承运商约定为准） |
| logisticsUpdatedAt | STRING | Logistics updated time（该轨迹节点更新时间；Partner **Response Example** 为字符串，一般为时间戳或 ISO 时间字符串） |
| statusText | STRING | Status description text（状态描述文案；语言由请求 **`language`** 决定） |

> 调用成功时先判断 **`success === true`**，再读取 **`result.trackingNum`** 与 **`result.trackingInfo`**。若返回 **170070011 Tracking Number Not Found**，表示暂无轨迹或单号无效，可稍后重试或核对 **`packageSn`**。

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 170070012 | Unsupported languages, {*} | Change the supported language（更换为 Partner **TEMU Logistics Tracking API Documentation** 支持的语言代码） |
| 170070011 | Tracking Number Not Found | Tracking information for this logistics number was not found. Please confirm the number is correct or try again later.（确认 **`packageSn`** 正确；包裹可能尚未产生轨迹，稍后重试） |
| 170070010 | Invalid Parameters: {*} | Parameters are invalid or missing. Please check the value and format of the {field name} field.（检查 **`packageSn`**、**`language`** 等字段格式与必填逻辑） |

---

## 典型用法

```text
1. linkfox-temu-fulfillment-us  → 购标获得 packageSn / trackingNumber
2. temu.track.trackinginfo.get（本接口）     → 按 packageSn 查询物流轨迹详情
3. linkfox-temu-order-us                     → 结合订单状态做履约跟进
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_tracking_track_trackinginfo_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSn": "PKG-001",
    "language": "en"
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.track.trackinginfo.get",
  "params": {
    "request": {
      "packageSn": "PKG-001",
      "language": "en"
    }
  }
}'
```
