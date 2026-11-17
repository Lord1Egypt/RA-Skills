# linkfox-shopee-store-video — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Video 模块**全部 15 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.video.get_cover_list](https://open.shopee.com/documents/v2/v2.video.get_cover_list?module=129&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/video/...`
- **标识**：店铺级 API，通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.video.{api}?module=129&type=1`
- **官方拼写**：`get_prodcut_performance_list`（product 拼写为 prodcut）

---

## Video 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | delete_video | POST | `api/v2/video/delete_video` | `delete_video.py` | [apis/delete-video.md](./apis/delete-video.md) |
| 2 | edit_video_info | POST | `api/v2/video/edit_video_info` | `edit_video_info.py` | [apis/edit-video-info.md](./apis/edit-video-info.md) |
| 3 | get_cover_list | GET | `api/v2/video/get_cover_list` | `get_cover_list.py` | [apis/get-cover-list.md](./apis/get-cover-list.md) |
| 4 | get_metric_trend | GET | `api/v2/video/get_metric_trend` | `get_metric_trend.py` | [apis/get-metric-trend.md](./apis/get-metric-trend.md) |
| 5 | get_overview_performance | GET | `api/v2/video/get_overview_performance` | `get_overview_performance.py` | [apis/get-overview-performance.md](./apis/get-overview-performance.md) |
| 6 | get_prodcut_performance_list | GET | `api/v2/video/get_prodcut_performance_list` | `get_prodcut_performance_list.py` | [apis/get-prodcut-performance-list.md](./apis/get-prodcut-performance-list.md) |
| 7 | get_user_demographics | GET | `api/v2/video/get_user_demographics` | `get_user_demographics.py` | [apis/get-user-demographics.md](./apis/get-user-demographics.md) |
| 8 | get_video_detail | GET | `api/v2/video/get_video_detail` | `get_video_detail.py` | [apis/get-video-detail.md](./apis/get-video-detail.md) |
| 9 | get_video_detail_audience_distribution | GET | `api/v2/video/get_video_detail_audience_distribution` | `get_video_detail_audience_distribution.py` | [apis/get-video-detail-audience-distribution.md](./apis/get-video-detail-audience-distribution.md) |
| 10 | get_video_detail_metric_trend | GET | `api/v2/video/get_video_detail_metric_trend` | `get_video_detail_metric_trend.py` | [apis/get-video-detail-metric-trend.md](./apis/get-video-detail-metric-trend.md) |
| 11 | get_video_detail_performance | GET | `api/v2/video/get_video_detail_performance` | `get_video_detail_performance.py` | [apis/get-video-detail-performance.md](./apis/get-video-detail-performance.md) |
| 12 | get_video_detail_product_performance | GET | `api/v2/video/get_video_detail_product_performance` | `get_video_detail_product_performance.py` | [apis/get-video-detail-product-performance.md](./apis/get-video-detail-product-performance.md) |
| 13 | get_video_list | GET | `api/v2/video/get_video_list` | `get_video_list.py` | [apis/get-video-list.md](./apis/get-video-list.md) |
| 14 | get_video_performance_list | GET | `api/v2/video/get_video_performance_list` | `get_video_performance_list.py` | [apis/get-video-performance-list.md](./apis/get-video-performance-list.md) |
| 15 | post_video | POST | `api/v2/video/post_video` | `post_video.py` | [apis/post-video.md](./apis/post-video.md) |
通用入口：`video_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 视频管理

| API | 要点 |
|-----|------|
| `get_cover_list` | 视频封面列表 — [apis/get-cover-list.md](./apis/get-cover-list.md) |
| `post_video` | 发布/上传视频；POST `body` — [apis/post-video.md](./apis/post-video.md) |
| `get_video_list` | 店铺视频列表 — [apis/get-video-list.md](./apis/get-video-list.md) |
| `get_video_detail` | 视频详情 — [apis/get-video-detail.md](./apis/get-video-detail.md) |
| `edit_video_info` | 编辑标题/描述/封面 — [apis/edit-video-info.md](./apis/edit-video-info.md) |
| `delete_video` | 删除视频 — [apis/delete-video.md](./apis/delete-video.md) |

### 效果分析

| API | 要点 |
|-----|------|
| `get_overview_performance` | 整体效果概览 — [apis/get-overview-performance.md](./apis/get-overview-performance.md) |
| `get_metric_trend` | 指标趋势 — [apis/get-metric-trend.md](./apis/get-metric-trend.md) |
| `get_user_demographics` | 观众画像 — [apis/get-user-demographics.md](./apis/get-user-demographics.md) |
| `get_video_performance_list` | 视频效果列表 — [apis/get-video-performance-list.md](./apis/get-video-performance-list.md) |
| `get_video_detail_performance` | 单视频效果详情 — [apis/get-video-detail-performance.md](./apis/get-video-detail-performance.md) |
| `get_video_detail_metric_trend` | 单视频指标趋势 — [apis/get-video-detail-metric-trend.md](./apis/get-video-detail-metric-trend.md) |
| `get_video_detail_audience_distribution` | 单视频受众分布 — [apis/get-video-detail-audience-distribution.md](./apis/get-video-detail-audience-distribution.md) |
| `get_video_detail_product_performance` | 单视频商品效果 — [apis/get-video-detail-product-performance.md](./apis/get-video-detail-product-performance.md) |
| `get_prodcut_performance_list` | 商品在视频中的效果（官方拼写 prodcut） — [apis/get-prodcut-performance-list.md](./apis/get-prodcut-performance-list.md) |

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/video/...` |
| HTTP 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |

---

## curl 示例

```bash
export KEY=${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}
BASE=${LINKFOX_TOOL_GATEWAY}

curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/video/get_cover_list",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-video","sentiment":"POSITIVE",
       "category":"OTHER","content":"视频列表查询正常"}'
```
