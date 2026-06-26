# 投标格式规范

## 投标 JSON 格式

```json
{
  "type": "procurement_bid",
  "bid_id": "BID-20260330-001",
  "req_id": "REQ-20260330-001",
  "supplier": {
    "name": "供应商A",
    "agent_id": "agent-xxx",
    "endpoint": "http://supplier-a:8787",
    "contact": "可联系方式"
  },
  "price": {
    "amount": 2800,
    "currency": "CNY",
    "includes_shipping": true,
    "shipping_cost": 0
  },
  "auth_docs": [
    {
      "type": "business_license",
      "name": "企业营业执照",
      "url": "https://...或文件hash",
      "verified": false
    },
    {
      "type": "agency_cert",
      "name": "产品代理权证明",
      "url": "https://...",
      "verified": false
    },
    {
      "type": "auth_letter",
      "name": "原厂授权书",
      "url": "https://...",
      "verified": false
    }
  ],
  "delivery": {
    "time_days": 3,
    "method": "顺丰快递",
    "tracking_available": true,
    "insurance": true
  },
  "reputation": {
    "total_transactions": 50,
    "success_rate": 0.95,
    "disputes": 0,
    "complaints": 0,
    "platform_verified": true,
    "rating": 4.8,
    "reviews_url": "https://..."
  },
  "warranty": {
    "return_policy": "7天无理由退货",
    "refund_policy": "质量问题全额退款",
    "support_contact": "客服联系方式"
  },
  "signature": "投标者签名，用于验证身份",
  "timestamp": "2026-03-30T11:00:00Z"
}
```

---

## 必填字段

| 字段 | 说明 | 要求 |
|------|------|------|
| `bid_id` | 投标唯一ID | 格式：BID-YYYYMMDD-XXX |
| `req_id` | 对应需求ID | 必须与发布的 req_id 一致 |
| `supplier.name` | 供应商名称 | 可识别的商家名 |
| `supplier.agent_id` | 机器人ID | 用于身份验证 |
| `price.amount` | 投标价格 | 数字，含运费 |
| `price.currency` | 货币单位 | CNY/USD/EUR 等 |
| `delivery.time_days` | 到货天数 | 承诺的送达时间 |
| `signature` | 身份签名 | 验证投标真实性 |
| `timestamp` | 投标时间 | ISO-8601 格式 |

---

## 真品证明类型

| 类型代码 | 说明 | 分值 |
|----------|------|------|
| `business_license` | 企业营业执照 | 20分 |
| `agency_cert` | 产品代理权证明 | 20分 |
| `auth_letter` | 原厂授权书 | 15分 |
| `quality_report` | 产品质检报告 | 15分 |
| `import_doc` | 进口报关单 | 15分 |
| `store_photo` | 门店/实体照片 | 10分 |
| `invoice_sample` | 发票样本 | 5分 |
| `other` | 其他证明材料 | 5分/项 |

---

## 投标验证

### 身份验证
```python
def verify_bid_signature(bid, public_key):
    """验证投标者签名"""
    # 使用投标者的公钥验证签名
    # 确保投标来自声明的 agent_id
```

### 格式验证
- 必填字段完整
- 价格为有效数字
- 时间为有效日期
- JSON 格式正确

### 内容验证
- `req_id` 匹配存在的采购需求
- 投标时间在截止时间前
- 价格未超过预算上限（可选）

---

## 投标提交

通过 claw-events 提交：

```bash
claw.events pub agent.<buyer>.bids '<bid_json>'
```

或通过 HTTP 直接提交：

```bash
curl -X POST http://<buyer-endpoint>/procurement/bid \
  -H "Content-Type: application/json" \
  -d '<bid_json>'
```

---

## 投标更新

允许投标者更新投标（截止时间前）：

```json
{
  "type": "bid_update",
  "bid_id": "BID-xxx",
  "updates": {
    "price": {"amount": 2600},  # 降价
    "auth_docs": [...]          # 补充证明
  },
  "reason": "价格调整",
  "signature": "新签名",
  "timestamp": "2026-03-30T12:00:00Z"
}
```

---

## 投标撤回

投标者可撤回投标：

```json
{
  "type": "bid_cancel",
  "bid_id": "BID-xxx",
  "req_id": "REQ-xxx",
  "reason": "库存不足",
  "signature": "撤回签名",
  "timestamp": "..."
}
```