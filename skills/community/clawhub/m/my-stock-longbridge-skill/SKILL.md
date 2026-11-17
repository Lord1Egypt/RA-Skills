# my_longbridge_mgnt_skill

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
