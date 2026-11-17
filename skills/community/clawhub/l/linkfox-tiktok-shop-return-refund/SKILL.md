---
name: linkfox-tiktok-shop-return-refund
description: TikTok Shop ERP 售后（Return & Refund）业务技能，经 /tiktokShop/developerProxy（appType=erp）转发 Return Refund Open API：获取拒退/拒取消原因（Get Reject Reasons）。依赖 linkfox-tiktok-shop-auth 选店（传 openId；token 后台化，勿手动 refresh）。当用户提到 TikTok 拒退原因、拒绝退款原因、拒绝取消原因、Get Reject Reasons、reject_reasons、return_or_cancel_id、售后拒因列表 时触发。**不含授权**；**不含订单查询**（用 shop-order）；同意/拒绝退货等写操作可后续扩展本 skill。
---

# TikTok Shop ERP 售后（Return & Refund）

本 skill 调用 TikTok Shop **卖家 ERP 售后**开放接口。统一经 LinkFox 网关：

```
linkfox-tiktok-shop-auth  →  openId（选店）
        ↓
POST /tiktokShop/developerProxy
  appType = erp
  openId  = <ERP openId>
  path / method / queryString
        ↓
401 或 token 失效 → 网关自动 refresh 并重试一次
```

> 📌 **前置依赖**：`linkfox-tiktok-shop-auth`
> 📌 **勿手动刷新 token**
> 📌 官方入口：[Get Reject Reasons](https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309)
> 📌 完整参考：`references/apis/<api>.md`

## Prerequisites

1. `python scripts/check_auth_dependency.py`；exit **42** → 先完成 **`linkfox-tiktok-shop-auth`**。
2. 需要有效的 `return_or_cancel_id`（退货单或取消单 ID）。

## Core Concepts

| 概念 | 说明 |
|------|------|
| path 白名单 | `return_refund/`、`authorization/` |
| Get Reject Reasons | Query：`return_or_cancel_id`（必填）+ `shop_cipher`；可选 `locale` |
| 用途 | 拒绝退货/取消前，先拉可选拒因列表 |

## Available Scripts

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测 auth skill |
| `return_refund_api.py` | 具名 API |
| `return_refund_proxy.py` | 通用 path/method |
| `get_authorized_shops.py` | 取 `shop_cipher` |
| `get_reject_reasons.py` | 拒因列表 |

## Usage Examples

```bash
python scripts/get_reject_reasons.py '{
  "openId": "...",
  "return_or_cancel_id": "4035633471902223141"
}'

python scripts/return_refund_api.py '{
  "api": "get_reject_reasons",
  "openId": "...",
  "return_or_cancel_id": "4035..."
}'
```

## Important Limitations

- 当前以 **Get Reject Reasons** 为主；搜索退货/同意拒绝等可后续扩展。
- 不含订单 list/detail（`linkfox-tiktok-shop-order`）。

**Feedback**：`skillName` = `linkfox-tiktok-shop-return-refund`。
