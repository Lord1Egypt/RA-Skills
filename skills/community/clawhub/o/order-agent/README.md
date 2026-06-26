# order-agent 智能订单处理助手

基于 OpenClaw 的 WMS 订单处理技能，帮助用户快速创建发货单。

## 功能特性

- 📚 **商品查询** - 根据书名/ISBN查询商品库存、价格等信息
- 🛒 **单品下单** - 快速创建单个发货单
- 📦 **批量下单** - 支持解析 Excel 表格批量创建订单
- ✅ **订单确认** - 下单前展示详情，确认后执行

## 适用场景

- "帮我采购一本《斗破苍穹》"
- "帮我下单购买这本书"
- "帮我完成这个 Excel 表格中的订单发货"

## 快速开始

### 前置要求

- Python 3.7+
- WMS 后端服务（默认: http://localhost:9303）

### 安装

```bash
# 克隆仓库
git clone https://github.com/NeroD9408/order-agent.git
cd order-agent
```

### 查询商品

```bash
python3 scripts/order_api.py query --book-name "斗破苍穹"
python3 scripts/order_api.py query --isbn "9787533978297"
```

### 创建订单

```bash
python3 scripts/order_api.py create \
  --name "张三" \
  --phone "13800138000" \
  --province "北京市" \
  --city "北京市" \
  --district "朝阳区" \
  --detail "建国路88号SOHO现代城" \
  --book-name "斗破苍穹1：莫欺少年穷" \
  --stock-id 13048 \
  --stock-name "库书邦" \
  --isbn "9787533978297" \
  --buy-count 1 \
  --make-price 49.0
```

## 在 OpenClaw 中使用

安装此技能后，可以直接对话使用：

```
用户：帮我采购一本《斗破苍穹》
Agent：查询到以下版本，请问你要哪一本？
- 斗破苍穹1：莫欺少年穷
- 斗破苍穹2：少年志在天
...
```

## API 接口

### 商品查询

```bash
POST /goods/queryGoods
{
  "bookName": "书名",
  "isbn": "ISBN码"
}
```

### 创建订单

```bash
POST /order/createOrder
{
  "shopOrder": {
    "name": "收货人",
    "phone": "手机号",
    "province": "省份",
    "city": "城市",
    "district": "区县",
    "detail": "详细地址"
  },
  "orderInfoList": [{
    "bookName": "书名",
    "stockId": 库存ID,
    "buyCount": 数量,
    "makePrice": 制价
  }]
}
```

## 配置

修改 `scripts/order_api.py` 中的配置：

```python
BASE_URL = "https://aifx.tushu.cloud/prod-api/dispatch"  # WMS API 地址
TIMEOUT = 120  # 请求超时时间
```

## 开源协议

MIT License

## 作者

NeroD9408
