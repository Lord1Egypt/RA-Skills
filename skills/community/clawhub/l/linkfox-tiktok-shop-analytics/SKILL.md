---
name: linkfox-tiktok-shop-analytics
description: TikTok Shop ERP 数据分析（Analytics）业务技能，经 /tiktokShop/developerProxy（appType=erp）转发 Analytics Open API：获取店铺视频表现（Get Video Performances）。依赖 linkfox-tiktok-shop-auth 选店（传 openId；token 后台化，勿手动 refresh）。当用户提到 TikTok 视频表现、店铺视频数据、视频 GMV、Get Video Performances、shop_videos/performance、视频销量/浏览量分析、analytics video 时触发。**不含授权**；**不含达人侧视频发布**（用 linkfox-tiktok-video）；商品/店铺绩效等可后续扩展本 skill。
---

# TikTok Shop ERP 数据分析（Analytics）

本 skill 调用 TikTok Shop **卖家 ERP 分析**开放接口。统一经 LinkFox 网关：

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
> 📌 官方入口：[Get Video Performances](https://partner.tiktokshop.com/docv2/page/get-video-performances-202403)
> 📌 完整参考：`references/apis/<api>.md`

## Prerequisites

1. `python scripts/check_auth_dependency.py`；exit **42** → 先完成 **`linkfox-tiktok-shop-auth`**。
2. 需要时间范围：`start_date` / `end_date`（通常 `YYYYMMDD`）。

## Core Concepts

| 概念 | 说明 |
|------|------|
| path 白名单 | `analytics/`、`authorization/` |
| Get Video Performances | `GET analytics/202403/shop_videos/performance` |
| 时间窗 | Query：`start_date`、`end_date`（必填） |
| 分页 | `page_size` / `page_token` |

## Available Scripts

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测 auth skill |
| `analytics_api.py` | 具名 API |
| `analytics_proxy.py` | 通用 path/method |
| `get_authorized_shops.py` | 取 `shop_cipher` |
| `get_video_performances.py` | 视频表现列表 |

## Usage Examples

```bash
python scripts/get_video_performances.py '{
  "openId": "...",
  "start_date": "20240301",
  "end_date": "20240331",
  "page_size": 20
}'

python scripts/analytics_api.py '{
  "api": "get_video_performances",
  "openId": "...",
  "start_date": "20240301",
  "end_date": "20240331"
}'
```

## Important Limitations

- 当前以 **Get Video Performances（202403）** 为主；单视频详情/商品绩效等可后续扩展。
- 不含达人可购物视频发布（`linkfox-tiktok-video`）。

**Feedback**：`skillName` = `linkfox-tiktok-shop-analytics`。
