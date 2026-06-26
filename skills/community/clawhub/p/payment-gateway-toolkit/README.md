---
name: payment-gateway-toolkit
description: 支付网关工具包 - 集成Stripe、支付宝等多渠道支付处理，支持订单创建、退款、查询等功能 | Payment Gateway Toolkit - Multi-channel payment processing with Stripe, Alipay integration
homepage: https://github.com/kaiyuelv/payment-gateway-toolkit
category: payment
tags:
  - payment
  - stripe
  - alipay
  - gateway
  - order
  - refund
  - ecommerce
version: 1.0.0
---

# 支付网关工具包

集成多渠道支付网关的工具包，支持 Stripe、支付宝等主流支付方式。

## 概述

本Skill提供完整的支付处理能力：
- Stripe 信用卡/借记卡支付
- 支付宝网页支付/扫码支付
- 订单创建与管理
- 退款处理
- 支付状态查询
- 异步回调处理
- 订单历史记录

## 依赖

- Python >= 3.8
- stripe >= 7.0.0
- alipay-sdk-python >= 3.3.0
- requests >= 2.28.0

## 文件结构

```
payment-gateway-toolkit/
├── SKILL.md                  # 本文件
├── README.md                 # 使用文档
├── requirements.txt          # 依赖声明
├── scripts/
│   └── payment_handler.py    # 核心支付处理脚本
├── examples/
│   └── basic_usage.py        # 使用示例
└── tests/
    └── test_payment.py       # 单元测试
```

## 快速开始

```python
from scripts.payment_handler import PaymentHandler

# 初始化支付处理器
handler = PaymentHandler(
    stripe_key="sk_test_...",
    alipay_config={
        "app_id": "your_app_id",
        "private_key": "your_private_key",
        "alipay_public_key": "alipay_public_key"
    }
)

# 创建 Stripe 支付
order = handler.create_stripe_order(
    amount=99.99,
    currency="usd",
    description="Test Order"
)

# 创建支付宝订单
alipay_order = handler.create_alipay_order(
    amount=100.00,
    subject="商品购买",
    out_trade_no="ORDER123456"
)
```

## 许可证

MIT

---

# Payment Gateway Toolkit

Multi-channel payment gateway toolkit supporting Stripe, Alipay and other mainstream payment methods.

## Overview

This Skill provides complete payment processing capabilities:
- Stripe credit/debit card payments
- Alipay web/scan code payments
- Order creation and management
- Refund processing
- Payment status queries
- Async webhook handling
- Order history tracking

## Dependencies

- Python >= 3.8
- stripe >= 7.0.0
- alipay-sdk-python >= 3.3.0
- requests >= 2.28.0

## File Structure

```
payment-gateway-toolkit/
├── SKILL.md                  # This file
├── README.md                 # Usage documentation
├── requirements.txt          # Dependencies
├── scripts/
│   └── payment_handler.py    # Core payment handler script
├── examples/
│   └── basic_usage.py        # Usage examples
└── tests/
    └── test_payment.py       # Unit tests
```

## Quick Start

```python
from scripts.payment_handler import PaymentHandler

# Initialize payment handler
handler = PaymentHandler(
    stripe_key="sk_test_...",
    alipay_config={
        "app_id": "your_app_id",
        "private_key": "your_private_key",
        "alipay_public_key": "alipay_public_key"
    }
)

# Create Stripe payment
order = handler.create_stripe_order(
    amount=99.99,
    currency="usd",
    description="Test Order"
)

# Create Alipay order
alipay_order = handler.create_alipay_order(
    amount=100.00,
    subject="Product Purchase",
    out_trade_no="ORDER123456"
)
```

## License

MIT
