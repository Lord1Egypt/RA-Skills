# Request and Response Guide

## `GET /api/v1/instagram/task/video/download`
- operationId: `instagram_task_video_download`
- summary: 任务-视频下载
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `video_code` | `query` | `true` | `string` | 视频code |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_InstagramTaskVideoDownloadRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `video_code`, `task_id`, `task_status`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "video_code": null,
    "task_id": null,
    "task_status": null
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/instagram/user/monitor/metrics`
- operationId: `instagram_user_monitor_metrics`
- summary: 用户监控指标
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `period` | `query` | `false` | `string` | 周期(last_31_days,monthly) |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_InstagramUserMonitorMetricsRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.date`, `items.follower_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "date": "2025-11-02",
      "follower_count": 121000000
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `POST /api/v1/monitor/video/tasks/create`
- operationId: `create_monitor_task`
- summary: 创建视频监测任务
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `VideoMonitorTaskCreateReq` | `platform`, `video_id` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_VideoMonitorTaskRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `monitor_id`, `platform`, `video_id`, `video_title`, `author_id`, `author_name`, `monitor_status`, `monitor_start_date`, `monitor_end_date`, `last_snapshot_time`, `snapshot_count`, `created_time`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "monitor_id": "string",
    "platform": "string",
    "video_id": "string",
    "video_title": null,
    "author_id": null,
    "author_name": null,
    "monitor_status": 0,
    "monitor_start_date": "2026-01-01"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/monitor/video/tasks/detail`
- operationId: `get_monitor_task_detail`
- summary: 获取视频监测任务详情
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `monitor_id` | `query` | `true` | `string` | 监测ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_VideoMonitorTaskDetailRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `monitor_id`, `platform`, `video_id`, `video_title`, `author_id`, `author_name`, `monitor_status`, `monitor_start_date`, `monitor_end_date`, `last_snapshot_time`, `snapshot_count`, `created_time`, `snapshots`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "monitor_id": "string",
    "platform": "string",
    "video_id": "string",
    "video_title": null,
    "author_id": null,
    "author_name": null,
    "monitor_status": 0,
    "monitor_start_date": "2026-01-01"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/monitor/video/tasks/list`
- operationId: `list_monitor_tasks`
- summary: 获取视频监测任务列表
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `platform` | `query` | `false` | `string` | 平台筛选：tiktok、youtube、instagram |
| `monitor_status` | `query` | `false` | `integer` | 状态筛选：0-监测中 10-已完成 20-已停止 |
| `page` | `query` | `false` | `integer` | 页码 |
| `page_size` | `query` | `false` | `integer` | 每页数量 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_VideoMonitorTaskRep__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items`, `total`, `page`, `page_size`, `total_pages`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "items": [
      null
    ],
    "total": 0,
    "page": 0,
    "page_size": 0,
    "total_pages": 0
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `POST /api/v1/monitor/video/tasks/refresh`
- operationId: `refresh_monitor_task`
- summary: 手动刷新视频监测数据
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `monitor_id` | `query` | `true` | `string` | 监测ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_VideoMonitorSnapshotRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `id`, `snapshot_time`, `snapshot_type`, `like_count`, `comment_count`, `play_count`, `share_count`, `collect_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "id": 0,
    "snapshot_time": "2026-01-01T00:00:00Z",
    "snapshot_type": "string",
    "like_count": null,
    "comment_count": null,
    "play_count": null,
    "share_count": null,
    "collect_count": null
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/monitor/video/tasks/stop`
- operationId: `stop_monitor_task`
- summary: 停止视频监测任务
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `monitor_id` | `query` | `true` | `string` | 监测ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `none`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": null
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/tiktok/task/video/download`
- operationId: `tiktok_task_video_download`
- summary: 任务-视频下载
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `video_id` | `query` | `true` | `string` | 视频ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_TiktokTaskVideoDownloadRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `video_id`, `task_id`, `task_status`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "video_id": null,
    "task_id": null,
    "task_status": null
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/tiktok/user/monitor/metrics`
- operationId: `tiktok_user_monitor_metrics`
- summary: 用户监控指标
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `period` | `query` | `false` | `string` | 周期(last_31_days,monthly) |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_TiktokUserMonitorMetricsRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.date`, `items.follower_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "date": "2025-11-02",
      "follower_count": 121000000
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/youtube/task/video/download`
- operationId: `youtube_task_video_download`
- summary: 任务-视频下载
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `video_id` | `query` | `true` | `string` | 视频ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_YoutubeTaskVideoDownloadRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `video_id`, `task_id`, `task_status`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "video_id": null,
    "task_id": null,
    "task_status": null
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/youtube/user/monitor/metrics`
- operationId: `youtube_user_monitor_metrics`
- summary: 用户监控指标
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `period` | `query` | `false` | `string` | 周期(last_31_days,monthly) |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_YoutubeUserMonitorMetricsRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.date`, `items.subscriber_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "date": "2025-11-02",
      "subscriber_count": 121000000
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
