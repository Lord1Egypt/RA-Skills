---
name: order-agent
description: |
  智能订单处理助手，帮助用户快速创建WMS发货单。
  当用户请求以下操作时使用：
  1. 采购/下单/创建发货单（如"帮我采购一本书"、"帮我下单"）
  2. 批量处理订单（如"帮我完成这个表格中所有订单的发货"）
  3. 从Excel/CSV文件导入订单
  支持从标准格式的Excel表格中提取：商品名称、数量、ISBN、收件人姓名、手机号、地址等信息，
  并调用WMS API创建发货单。
---

# Order Agent - 智能订单处理

## 功能概述

- **商品查询**: 根据书名/ISBN查询商品详情（库存、价格等）
- **单品下单**: 用户提供商品信息，快速创建发货单
- **批量下单**: 解析Excel表格，批量创建发货单
- **订单确认**: 下单前展示订单详情，确认后执行

## 使用流程

### 1. 查询商品信息（必做）

先查询商品，获取商品详情：

```bash
python3 scripts/order_api.py query --book-name "红楼梦"
```

**商品返回字段说明：**

| 字段 | 说明 | 用于下单 |
|------|------|----------|
| bookName | 书名 | ✓ --book-name |
| productName | 产品名称 | ✓ --product-name |
| productCode | 货号 | ✓ --product-code |
| stockId | 库存ID | ✓ --stock-id |
| stockName | 库存名称 | ✓ --stock-name |
| isbn | ISBN | ✓ --isbn |
| wholesalePrice | 批发价 | 参考 |
| makePrice | 制作价格 | ✓ --make-price |
| author | 作者 | 参考 |
| press | 出版社 | 参考 |
| stayOutboundCount | 库存数量 | 参考 |

### 2. 创建订单

使用商品查询返回的字段创建订单：

```bash
python3 scripts/order_api.py create \
  --name "张三" \
  --phone "13800138000" \
  --province "北京市" \
  --city "北京市" \
  --district "朝阳区" \
  --detail "建国路88号SOHO现代城" \
  --book-name "名师教你读经典《红楼梦》" \
  --stock-id 13048 \
  --stock-name "库书邦" \
  --isbn "9787545919547" \
  --buy-count 1
```

### 3. 返回结果

返回订单号和详情链接

## API 接口说明

### 商品查询接口

- **URL**: `POST /goods/queryGoods`
- **请求体**:
```json
{
  "bookName": "红楼梦",
  "isbn": "9787545919547",
  "pageNum": 1,
  "pageSize": 20
}
```
- **响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "productName": "名师教你读经典《红楼梦》",
      "productCode": "1849866049445462016",
      "img": "/source/wenxuanBook/20220930/DoiBcQLV.png",
      "isbn": "9787545919547",
      "bookName": "名师教你读经典《红楼梦》",
      "wholesalePrice": 6.26,
      "makePrice": 28.0,
      "stockName": "库书邦",
      "stockId": 13048,
      "stayOutboundCount": 7319,
      "stockType": 1,
      "author": "【清】曹雪芹 著",
      "press": "鹭江出版社",
      "wholesaleDiscount": 0.22
    }
  ]
}
```

### 创建订单接口

- **URL**: `POST /order/createOrder`
- **请求体**:
```json
{
  "shopOrder": {
    "name": "张三",
    "phone": "13800138000",
    "province": "北京市",
    "city": "北京市",
    "district": "朝阳区",
    "detail": "建国路88号SOHO现代城",
    "countrysideName": "",
    "remark": "",
    "orderSource": 15,
    "orderSort": 1,
    "initOrderNum": ""
  },
  "orderInfoList": [
    {
      "productName": "名师教你读经典《红楼梦》",
      "productCode": "1849866049445462016",
      "bookName": "名师教你读经典《红楼梦》",
      "isbn": "9787545919547",
      "stockName": "库书邦",
      "stockId": 13048,
      "buyCount": 1,
      "author": "【清】曹雪芹 著",
      "press": "鹭江出版社",
      "makePrice": 28.0
    }
  ]
}
```
- **响应**:
```json
{
  "code": 200,
  "data": {
    "orderNum": "ORDER123456",
    "detailUrl": "https://xxx.com/order/ORDER123456"
  },
  "msg": "success"
}
```

## Scripts

### order_api.py

主脚本，支持两个子命令：

**查询商品:**
```bash
python3 scripts/order_api.py query --book-name "红楼梦"
python3 scripts/order_api.py query --isbn "9787545919547"
```

**创建订单:**（必须先查询商品，获取stockId和stockName）
```bash
python3 scripts/order_api.py create \
  --name "张三" \
  --phone "13800138000" \
  --province "北京市" \
  --city "北京市" \
  --district "朝阳区" \
  --detail "建国路88号" \
  --book-name "名师教你读经典《红楼梦》" \
  --stock-id 13048 \
  --stock-name "库书邦" \
  --isbn "9787545919547" \
  --buy-count 1 \
  --make-price 28.0
```

## 错误处理

- 网络超时: 已设置120秒超时
- 校验失败: 提示具体字段问题
- API返回失败: 展示错误信息，允许用户修改重试

## 配置说明

后端 API 地址和超时在脚本中配置：
```python
BASE_URL = "https://aifx.tushu.cloud/prod-api/dispatch"
TIMEOUT = 120  # 查询接口较慢，设置120秒
```

如需修改，编辑 `scripts/order_api.py` 中的配置变量。
