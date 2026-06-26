# WMS API 文档

## 接口信息

- **基础 URL**: `https://wms.example.com/api/v1`
- **认证方式**: Bearer Token
- **Content-Type**: `application/json`

## 创建发货单

### 接口地址

```
POST /shipment/create
```

### 请求头

| 字段 | 类型 | 说明 |
|------|------|------|
| Authorization | string | Bearer {api_key} |
| Content-Type | string | application/json |

### 请求体

```json
{
  "orderNo": "客户订单号",
  "warehouseCode": "仓库编码",
  "consignee": {
    "name": "收件人姓名",
    "phone": "收件人电话",
    "address": "详细地址"
  },
  "items": [
    {
      "sku": "商品SKU/ISBN",
      "name": "商品名称",
      "quantity": 数量
    }
  ],
  "remark": "备注"
}
```

### 响应示例

```json
{
  "success": true,
  "orderId": "WMS202602250001",
  "orderNo": "ORDER123456",
  "trackingUrl": "https://wms.example.com/order/WMS202602250001",
  "message": "订单创建成功",
  "createTime": "2026-02-25 15:00:00"
}
```

### 错误码

| code | message | 说明 |
|------|---------|------|
| 400 | 参数错误 | 请求参数缺失或格式错误 |
| 401 | 认证失败 | API 密钥无效 |
| 404 | 仓库不存在 | warehouseCode 无效 |
| 500 | 服务错误 | WMS 内部错误 |

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| orderNo | 是 | 客户订单号，需唯一 |
| warehouseCode | 是 | 仓库编码 |
| consignee.name | 是 | 收件人姓名 |
| consignee.phone | 是 | 收件人电话 |
| consignee.address | 是 | 收件人地址 |
| items[].sku | 是 | 商品SKU或ISBN |
| items[].name | 是 | 商品名称 |
| items[].quantity | 是 | 数量 |
| remark | 否 | 备注 |
