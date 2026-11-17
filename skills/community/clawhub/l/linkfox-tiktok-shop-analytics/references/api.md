# TikTok Shop ERP Analytics API Reference

> ⚠️ 依赖 **`linkfox-tiktok-shop-auth`**（`appType=erp`）。
> 官方入口：[Get Video Performances](https://partner.tiktokshop.com/docv2/page/get-video-performances-202403)。

## 转发约定

- 入口：`POST /tiktokShop/developerProxy`，固定 `appType=erp`，传 `openId`（token 后台化；401 自动刷新）。
- path 白名单：`authorization/`、`analytics/`
- `ttsAccessToken` 已废弃忽略。

## 接口索引

| api | Method | path | shop_cipher | 参考 | 官方 |
|-----|--------|------|-------------|------|------|
| `get_authorized_shops` | GET | `authorization/202309/shops` | 否 | [doc](apis/get_authorized_shops.md) | [link](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309) |
| `get_video_performances` | GET | `analytics/202403/shop_videos/performance` | 是 | [doc](apis/get_video_performances.md) | [link](https://partner.tiktokshop.com/docv2/page/get-video-performances-202403) |

```bash
python scripts/get_video_performances.py '{"openId":"...","start_date":"20240301","end_date":"20240331"}'
```

## Notes

1. `start_date` / `end_date` 为 Query 必填（通常 `YYYYMMDD`）。
2. 勿输出完整 ERP token。
3. 若网关返回 path 未白名单（1005），联系运维放行 `analytics/`。
