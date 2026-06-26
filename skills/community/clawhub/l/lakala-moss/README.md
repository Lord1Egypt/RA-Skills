# lakala-moss

拉卡拉MOSS支付下单技能 — 通过MOSS统一支付API发起支付订单并获取支付链接。

## 功能

- 🧾 创建支付订单，生成支付链接
- 💳 支持支付宝/微信/银联二维码支付
- 🔧 适用于支付接口测试和电商集成演示

## 安装

```bash
clawhub install lakala-moss
```

或让AI自动发现：在对话中提及"拉卡拉MOSS支付"即可自动调用。

## 快速使用

### 命令行方式
```bash
python scripts/create_order.py --order-no "TEST001" --total-amount "1"
```

### 代码方式
```python
from scripts.create_order import create_order

result = create_order(order_no="TEST001", total_amount="1")
print(result["pay_url"])  # 输出支付链接
```

## 依赖

- Python 3.8+
- requests>=2.28.0

## 注意

当前版本使用测试商户号（M00002042），仅用于演示和测试。生产环境需替换为真实商户号并配置签名验证。

## License

MIT
