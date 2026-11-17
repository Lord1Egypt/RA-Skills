# TikTok Shop ERP Return & Refund API Reference

> ⚠️ 依赖 **`linkfox-tiktok-shop-auth`**（`appType=erp`）。
> 官方入口：[Get Reject Reasons](https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309)。

## 转发约定

- 入口：`POST /tiktokShop/developerProxy`，固定 `appType=erp`，传 `openId`（token 后台化；401 自动刷新）。
- path 白名单：`authorization/`、`return_refund/`
- `ttsAccessToken` 已废弃忽略。

## 接口索引

| api | Method | path | shop_cipher | 参考 | 官方 |
|-----|--------|------|-------------|------|------|
| `get_authorized_shops` | GET | `authorization/202309/shops` | 否 | [doc](apis/get_authorized_shops.md) | [link](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309) |
| `get_reject_reasons` | GET | `return_refund/202309/reject_reasons` | 是 | [doc](apis/get_reject_reasons.md) | [link](https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309) |

```bash
python scripts/get_reject_reasons.py '{"openId":"...","return_or_cancel_id":"..."}'
```

## Notes

1. `return_or_cancel_id` 为 Query 必填。
2. 勿输出完整 ERP token。
