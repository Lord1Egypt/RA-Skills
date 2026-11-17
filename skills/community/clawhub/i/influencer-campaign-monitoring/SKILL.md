---
name: influencer-campaign-monitoring
description: "Monitor influencer campaigns across TikTok, Instagram, and YouTube: create and manage monitor tasks, pull metrics, download tracked assets, run post-campaign reviews. Campaign tracking, performance monitoring."
---

# Influencer Campaign Monitoring

Operate monitoring tasks and convert tracking data into actionable campaign review insights.

## Capability Matrix

### YouTube

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 任务-视频下载 | `youtube_task_video_download` | `GET /api/v1/youtube/task/video/download` | `query.video_id` |
| 用户监控指标 | `youtube_user_monitor_metrics` | `GET /api/v1/youtube/user/monitor/metrics` | `query.channel_id` |

### TikTok

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 任务-视频下载 | `tiktok_task_video_download` | `GET /api/v1/tiktok/task/video/download` | `query.video_id` |
| 用户监控指标 | `tiktok_user_monitor_metrics` | `GET /api/v1/tiktok/user/monitor/metrics` | `query.unique_id` |

### Instagram

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 任务-视频下载 | `instagram_task_video_download` | `GET /api/v1/instagram/task/video/download` | `query.video_code` |
| 用户监控指标 | `instagram_user_monitor_metrics` | `GET /api/v1/instagram/user/monitor/metrics` | `query.username` |

### Cross-platform

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 创建视频监测任务 | `create_monitor_task` | `POST /api/v1/monitor/video/tasks/create` | `body.platform, body.video_id` |
| 获取视频监测任务详情 | `get_monitor_task_detail` | `GET /api/v1/monitor/video/tasks/detail` | `query.monitor_id` |
| 获取视频监测任务列表 | `list_monitor_tasks` | `GET /api/v1/monitor/video/tasks/list` | `none` |
| 手动刷新视频监测数据 | `refresh_monitor_task` | `POST /api/v1/monitor/video/tasks/refresh` | `query.monitor_id` |
| 停止视频监测任务 | `stop_monitor_task` | `GET /api/v1/monitor/video/tasks/stop` | `query.monitor_id` |

## Quick Start

1. Identify monitoring scope (platform, creator/video, timeframe).
2. Use Cross-platform matrix rows for task lifecycle operations.
3. Use platform rows for metrics/download operations.
4. Report trend, anomalies, and intervention actions.

## Workflow

1. Create or retrieve tasks (`create_monitor_task`, `list_monitor_tasks`, `get_monitor_task_detail`).
2. Refresh/stop tasks as needed (`refresh_monitor_task`, `stop_monitor_task`).
3. Pull platform metrics and tracked assets for campaign review.
4. Summarize movement, anomalies, and next-step recommendation.

## Tooling

Execution commands:
- List operations: `python3 scripts/execute_operation.py --env-file .env list`
- Create task: `python3 scripts/execute_operation.py --env-file .env call --operation create_monitor_task --body '{"platform":"tiktok","video_id":"123456"}'`
- List tasks: `python3 scripts/execute_operation.py --env-file .env call --operation list_monitor_tasks --query '{"page":1,"page_size":20}'`

Required environment variables:
- `SCRUMBALL_BASE_URL`: API gateway base URL
- `SCRUMBALL_API_KEY`: unified API key
- Optional: `SCRUMBALL_AUTH_PREFIX`, `SCRUMBALL_TIMEOUT_SECONDS`

Env loading:
- Use `--env-file .env` for explicit loading.
- Without `--env-file`, script auto-tries `./.env` then `<skill-root>/.env`.

## Output Contract

Always return:
- `Task status`: active/completed/stopped + identifiers
- `Performance trend`: key metric movement
- `Anomalies`: unexpected spikes/drops
- `Recommendation`: continue, adjust, or stop

## Failure Handling

- If task creation fails, validate platform and video identifier first.
- If metric endpoints lag, report delayed freshness explicitly.
- If user asks for audience-fit decisioning, hand off to audience-fit skill.

## References

- `references/api-index.md`: full operation index + platform grouped index
- `references/request-response.md`: request parameters + response top-level/data fields + minimal examples
- `references/operations.json`: operation manifest used by `scripts/execute_operation.py`

## Quota & Unlock (important: act on 429)

- **Free tier**: a limited number of calls per day, zero-config (no key required — the skill defaults to a hosted gateway that injects the key server-side).
- **When any operation returns HTTP 429, or the response body has `code=429` / contains `quota_exceeded`, you (the assistant) MUST immediately and clearly tell the user** (do not silently retry, do not treat it as a generic error):

  > Free quota exhausted. Register and get your own API key at **https://data.scdata.cc/pricing**, then set the environment variable `SCRUMBALL_API_KEY` to your key (in your host/agent environment or a local `.env`). You can then continue with your own quota.

- The 429 response body usually includes `apply_url` and `env_var` fields you can quote directly.
