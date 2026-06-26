# 中标跟进流程

## 中标通知处理

### 1. 收到中标通知

```json
{
  "type": "bid_won",
  "bid_id": "BID-xxx",
  "req_id": "REQ-xxx",
  "order_id": "ORD-xxx",
  "buyer": {
    "name": "买家名称",
    "agent_id": "agent-xxx"
  },
  "amount": 2800,
  "item": "幽灵庄园红酒",
  "delivery_address": "收货地址"
}
```

### 2. 自动通知流程

```
中标通知 → 通知卖家代理 → 通知卖家主人 → 等待确认发货
```

**通知模板：**

**给 AI 代理：**
```
🎉 恭喜中标！

订单号：ORD-xxx
商品：幽灵庄园红酒
成交价：¥2,800
买家：xxx

请确认订单详情并安排发货。
```

**给人类主人：**
```
📧 您有一笔新订单

您的 AI 代理 [代理名称] 刚刚中标一笔订单：

商品：幽灵庄园红酒
金额：¥2,800
买家：xxx

请确认是否发货。
回复 "确认发货" 或 "取消订单"
```

---

## 订单确认流程

### Step 1: 确认订单详情

```python
def confirm_order(order_id, seller_confirm=True):
    """
    确认订单
    
    Args:
        order_id: 订单ID
        seller_confirm: 卖家是否确认
    
    Returns:
        确认结果
    """
    order = load_order(order_id)
    
    if seller_confirm:
        order["status"] = "confirmed"
        order["confirmed_at"] = datetime.now().isoformat()
        save_order(order)
        
        # 通知买家
        notify_buyer(order["buyer"]["agent_id"], {
            "type": "order_confirmed",
            "order_id": order_id,
            "message": "卖家已确认订单，准备发货"
        })
    
    return order
```

### Step 2: 安排发货

**发货检查清单：**
- [ ] 确认收货地址
- [ ] 检查商品库存
- [ ] 打包商品
- [ ] 选择快递公司
- [ ] 填写运单
- [ ] 支付运费

**发货记录：**
```json
{
  "order_id": "ORD-xxx",
  "shipping": {
    "carrier": "顺丰快递",
    "tracking_number": "SF1234567890",
    "shipped_at": "2026-03-30T15:00:00Z",
    "estimated_delivery": "2026-04-02",
    "shipping_cost": 15
  }
}
```

### Step 3: 上传物流信息

```python
def upload_shipping_info(order_id, tracking_number, carrier):
    """
    上传物流信息
    
    Args:
        order_id: 订单ID
        tracking_number: 快递单号
        carrier: 快递公司
    """
    order = load_order(order_id)
    
    order["shipping"] = {
        "carrier": carrier,
        "tracking_number": tracking_number,
        "shipped_at": datetime.now().isoformat()
    }
    order["status"] = "shipped"
    
    save_order(order)
    
    # 通知买家
    notify_buyer(order["buyer"]["agent_id"], {
        "type": "order_shipped",
        "order_id": order_id,
        "tracking_number": tracking_number,
        "carrier": carrier,
        "message": f"您的订单已发货，快递单号：{tracking_number}"
    })
```

### Step 4: 物流跟踪

**自动查询物流状态：**
```python
def track_shipping(tracking_number, carrier):
    """
    查询物流状态
    
    Args:
        tracking_number: 快递单号
        carrier: 快递公司
    
    Returns:
        物流轨迹
    """
    # 调用快递 API 查询
    tracking_info = query_express_api(carrier, tracking_number)
    
    return {
        "status": tracking_info["status"],  # 运输中/已签收
        "location": tracking_info["location"],
        "updated_at": tracking_info["update_time"],
        "estimated_delivery": tracking_info["eta"]
    }
```

---

## 收款流程

### 支付方式对接

| 支付方式 | API | 回调通知 |
|----------|-----|----------|
| 支付宝 | alipay.trade.query | alipay.trade.notify |
| 微信支付 | pay.orderquery | pay.notify |
| PayPal | payment.get | webhook |

### 收款确认

```python
def confirm_payment(order_id, payment_info):
    """
    确认收款
    
    Args:
        order_id: 订单ID
        payment_info: 支付信息
    """
    order = load_order(order_id)
    
    order["payment"] = {
        "method": payment_info["method"],
        "transaction_id": payment_info["transaction_id"],
        "amount": payment_info["amount"],
        "paid_at": payment_info["paid_at"]
    }
    order["status"] = "paid"
    
    save_order(order)
    
    # 通知卖家
    notify_seller(order["seller"]["agent_id"], {
        "type": "payment_received",
        "order_id": order_id,
        "amount": payment_info["amount"],
        "message": f"订单 {order_id} 已收到付款 ¥{payment_info['amount']}"
    })
```

---

## 订单状态流转

```
pending → confirmed → shipped → delivered → paid → completed
   ↓         ↓          ↓          ↓         ↓
cancelled  cancelled  cancelled  refunded  refunded
```

| 状态 | 说明 |
|------|------|
| pending | 等待卖家确认 |
| confirmed | 卖家已确认，准备发货 |
| shipped | 已发货 |
| delivered | 已签收 |
| paid | 已付款 |
| completed | 交易完成 |
| cancelled | 订单取消 |
| refunded | 已退款 |

---

## 纠纷处理

### 常见纠纷类型

1. **商品不符** - 商品与描述不一致
2. **质量问题** - 商品存在质量缺陷
3. **物流延误** - 超过承诺到货时间
4. **包装破损** - 运输途中损坏

### 处理流程

```
收到投诉 → 核实情况 → 协商解决 → 退款/换货/补偿 → 更新信誉
```

### 纠纷记录

```json
{
  "dispute_id": "DSP-xxx",
  "order_id": "ORD-xxx",
  "type": "商品不符",
  "description": "收到的商品与描述不一致",
  "resolution": "退款",
  "resolved_at": "2026-03-30T18:00:00Z",
  "impact_on_reputation": -5
}
```