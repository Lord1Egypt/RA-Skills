---
name: my_stock_longbridge_skill
description: 长桥证券(Longbridge)OpenAPI 集成与交易管理技能
version: 1.0.1
author: 老大
---

# my_stock_longbridge_skill

## Purpose
Longbridge OpenAPI integration for automated stock management.

## Setup
1. Configure credentials via `openclaw secrets configure`.
2. Ensure `longbridge` is installed (`pip install -r requirements.txt`).

## Functions
- `trade`: Execute, Modify, Cancel orders.
  - Supports Market Orders (MO) by default.
  - Supports Limit Orders (LO) when `order_type=OrderType.LO` and `price` is provided.
- `market`: Real-time quotes.
- `account`: Asset & Position tracking.
- `push`: Real-time streaming handler.

---
_Warning: Do not hardcode credentials._
