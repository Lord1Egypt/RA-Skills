# linkfox-amazon-store-external-fulfillment — API 与网关调用说明

## 1. 调用链

1. 依赖 **`linkfox-amazon-store-auth`** 完成店铺授权（`sellerId` + `region`）。
2. **`POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`**  
   Body 字段：
   - **`region`**
   - **`path`**：Amazon SP-API 相对 path，**无**前导 `/`
   - **`method`**：`GET` | `POST` | `PUT` | `PATCH`
   - **`sellerId`**：由网关解析 token（勿优先传 `amzAccessToken`）
   - **`queryString`**（可选）：不含 `?`
   - **`body`**（写操作）：JSON 字符串
   - **`contentType`**：`application/json`

环境变量：

- **`LINKFOX_AGENT_API_KEY`**（或 **`LINKFOXAGENT_API_KEY`**）
- **`LINKFOX_TOOL_GATEWAY`**（或 `STORE_API_BASE_URL` / `SPAPI_BASE_URL`）：默认 `https://tool-gateway.linkfox.com`

---

## 2. 脚本与 path / method 对照

| 脚本 | method | path 模板 |
|------|--------|-----------|
| `post_batch_inventory.py` | POST | `externalFulfillment/inventory/2024-09-11/inventories` |
| `get_shipments.py` | GET | `externalFulfillment/2024-09-11/shipments` |
| `get_shipment.py` | GET | `externalFulfillment/2024-09-11/shipments/{shipmentId}` |
| `process_shipment.py` | POST | `externalFulfillment/2024-09-11/shipments/{shipmentId}` + `operation` |
| `create_packages.py` | POST | `.../shipments/{shipmentId}/packages` |
| `update_package.py` | PUT | `.../shipments/{shipmentId}/packages/{packageId}` |
| `update_package_status.py` | PATCH | `.../shipments/{shipmentId}/packages/{packageId}` |
| `retrieve_shipping_options.py` | GET | `.../shipments/{shipmentId}/shippingOptions` + `packageId` |
| `generate_invoice.py` | POST | `.../shipments/{shipmentId}/invoice` |
| `retrieve_invoice.py` | GET | `.../shipments/{shipmentId}/invoice` |
| `generate_ship_labels.py` | PUT | `.../shipments/{shipmentId}/shipLabels` + `operation` |
| `list_returns.py` | GET | `externalFulfillment/2024-09-11/returns` |
| `get_return.py` | GET | `externalFulfillment/2024-09-11/returns/{returnId}` |

路径段经 percent-encoding。

---

## 3. 公共入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sellerId | string | 是 | 卖家 ID |
| region | string | 是 | NA / EU / FE |
| skipDepCheck | boolean | 否 | true 时跳过本地依赖探测 |

---

## 4. Inventory — `post_batch_inventory.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| requests | object[] | 是 | 1～10 条 |
| useAmazonRequestShape | boolean | 否 | true 时 `requests` 为官方原始数组 |

简化项字段：

| 字段 | 说明 |
|------|------|
| action | `fetch` 或 `update` |
| locationId | MFN 单仓常用 `DEFAULT`；Seller Flex 为 4 位仓码 |
| skuId | 卖家 SKU |
| quantity | update 必填；绝对库存 |
| clientSequenceNumber | 可选 |
| marketplaceAttributes | 可选；多站点时常需 `{marketplaceId, channelName}` |

脚本会组装为：

```json
{
  "requests": [
    {
      "method": "POST",
      "uri": "/inventory/fetch?locationId=DEFAULT&skuId=SKU-1",
      "body": { "marketplaceAttributes": { "marketplaceId": "...", "channelName": "MFN" } }
    }
  ]
}
```

解析字段：**`batchInventory`**（上游常为 HTTP **207**）。

官方：

- [Publish location-level inventory](https://developer-docs.amazon.com/sp-api/docs/publish-location-level-inventory)
- [Retrieve location-level inventory](https://developer-docs.amazon.com/sp-api/docs/retrieve-location-level-inventory)

---

## 5. Shipping

### 5.1 `get_shipments.py`

| 字段 | 必填 | 说明 |
|------|------|------|
| status | 是 | 如 ACCEPTED、CREATED、CONFIRMED、SHIPPED… |
| locationId | 否 | 渠道 location |
| marketplaceId / channelName | 否 | |
| lastUpdatedAfter / lastUpdatedBefore | 否 | ISO 8601 |
| maxResults | 否 | 1～100 |
| paginationToken | 否 | 上一页 nextToken |

解析字段：**`shipments`**。

### 5.2 `get_shipment.py`

| 字段 | 必填 |
|------|------|
| shipmentId | 是 |

解析字段：**`shipment`**。

### 5.3 `process_shipment.py`

| 字段 | 必填 | 说明 |
|------|------|------|
| shipmentId | 是 | |
| operation | 是 | CONFIRM / REJECT |
| requestBody | 否 | 官方 body |
| referenceId / lineItems | 否 | 简化字段，合成 body |

### 5.4 `create_packages.py`

| 字段 | 必填 |
|------|------|
| shipmentId | 是 |
| packages 或 requestBody | 是 |

### 5.5 `update_package.py`

| 字段 | 必填 |
|------|------|
| shipmentId / packageId / requestBody | 是 |

### 5.6 `update_package_status.py`

| 字段 | 必填 | 说明 |
|------|------|------|
| shipmentId / packageId | 是 | |
| status 或 requestBody | 是 | 可附带 subStatus、reason |

### 5.7 `retrieve_shipping_options.py`

| 字段 | 必填 |
|------|------|
| shipmentId / packageId | 是 |

解析字段：**`shippingOptions`**。

### 5.8 `generate_invoice.py` / `retrieve_invoice.py`

| 字段 | 必填 |
|------|------|
| shipmentId | 是 |

解析字段：**`invoice`**（含 `document.format` / `document.content` Base64）。

### 5.9 `generate_ship_labels.py`

| 字段 | 必填 | 说明 |
|------|------|------|
| shipmentId | 是 | |
| operation | 是 | GENERATE / REGENERATE |
| shippingOptionId | 否 | 需 URL 编码（脚本处理） |
| packageIds / requestBody | 否 | 三方承运等场景 |

解析字段：**`shipLabels`**。

---

## 6. Returns

### 6.1 `list_returns.py`

可选：`returnLocationId`、`rmaId`、`status`、`reverseTrackingId`、`createdSince`、`createdUntil`、`lastUpdatedSince`、`lastUpdatedUntil`、`maxResults`、`nextToken`。

解析字段：**`returns`**。

### 6.2 `get_return.py`

| 字段 | 必填 |
|------|------|
| returnId | 是 |

解析字段：**`returnItem`**。

---

## 7. 错误与白名单

| 现象 | 处理 |
|------|------|
| 401/402 / 算力不足 | 见 `references/onboarding.md` |
| 403 | 角色/allowlist/签名问题，非 onboarding 范围 |
| 1005 路径拒绝 | 后端放行 `externalFulfillment/` |
| 409 / 422 | 履约状态机冲突或参数不可处理，检查当前 shipment status |
| 429 | 降速重试（先征得用户同意） |

---

## 8. Feedback

`skillName`：`linkfox-amazon-store-external-fulfillment`
