# Request and Response Guide

## `GET /api/v1/instagram/realtime/media/detail`
- operationId: `instagram_realtime_media_detail`
- summary: 实时采集-贴文详情
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `media_code` | `query` | `true` | `string` | media code |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeInstagramMediaInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `author_user_id`, `author_username`, `media_id`, `media_code`, `create_at`, `cover_url`, `resources`, `description`, `accessibility_caption`, `media_url`, `media_type`, `duration`, `like_count`, `comment_count`, `play_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "author_user_id": null,
    "author_username": null,
    "media_id": null,
    "media_code": null,
    "create_at": null,
    "cover_url": null,
    "resources": null,
    "description": null
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

## `GET /api/v1/instagram/realtime/user/info`
- operationId: `instagram_realtime_user_info`
- summary: 实时采集-用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `false` | `string` | username |
| `user_id` | `query` | `false` | `string` | user_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeInstagramUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `user_id`, `username`, `full_name`, `profile_url`, `description`, `follower_count`, `following_count`, `media_count`, `is_private`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "user_id": null,
    "username": null,
    "full_name": null,
    "profile_url": null,
    "description": null,
    "follower_count": null,
    "following_count": null,
    "media_count": null
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

## `GET /api/v1/instagram/realtime/user/medias`
- operationId: `instagram_realtime_user_medias`
- summary: 实时采集-用户贴文
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `user_id` | `query` | `true` | `string` | user_id |
| `offset` | `query` | `false` | `string` | offset |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeInstagramUserMediasRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `more`, `offset`, `medias`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "more": null,
    "offset": null,
    "medias": null
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

## `GET /api/v1/instagram/realtime/user/stories`
- operationId: `instagram_realtime_user_stories`
- summary: 实时采集-用户故事
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `user_id` | `query` | `true` | `string` | user_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeInstagramUserStoriesRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `user`, `stories`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "user": null,
    "stories": null
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

## `GET /api/v1/tiktok/realtime/user/info`
- operationId: `tiktok_realtime_user_info`
- summary: 实时采集-用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `false` | `string` | unique_id |
| `user_id` | `query` | `false` | `string` | user_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeTiktokUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `uid`, `unique_id`, `sec_uid`, `nickname`, `profile_url`, `avatar`, `description`, `verified`, `country`, `follower_count`, `following_count`, `total_favorited`, `video_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "uid": null,
    "unique_id": null,
    "sec_uid": null,
    "nickname": null,
    "profile_url": null,
    "avatar": null,
    "description": null,
    "verified": null
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

## `GET /api/v1/tiktok/realtime/user/videos`
- operationId: `tiktok_realtime_user_videos`
- summary: 实时采集-用户视频
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `uid` | `query` | `true` | `string` | uid or sec_uid |
| `region` | `query` | `false` | `string` | country code:US,VN... |
| `offset` | `query` | `false` | `string` | offset |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeTiktokUserVideosRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `more`, `offset`, `videos`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "more": null,
    "offset": null,
    "videos": null
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

## `GET /api/v1/tiktok/realtime/video/detail`
- operationId: `tiktok_realtime_video_detail`
- summary: 实时采集-视频详情
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `video_id` | `query` | `true` | `string` | 视频ID |
| `region` | `query` | `true` | `string` | country code:US,VN... |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeTiktokVideoInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `video_id`, `description`, `create_at`, `author_uid`, `author_unique_id`, `author_nickname`, `duration`, `share_count`, `like_count`, `comment_count`, `play_count`, `collect_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "video_id": null,
    "description": null,
    "create_at": null,
    "author_uid": null,
    "author_unique_id": null,
    "author_nickname": null,
    "duration": null,
    "share_count": null
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

## `GET /api/v1/youtube/realtime/user/info`
- operationId: `youtube_realtime_user_info`
- summary: 实时采集-用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `false` | `string` | channel_id |
| `username` | `query` | `false` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeYoutubeUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `channel_id`, `username`, `title`, `profile_url`, `description`, `subscriber_count`, `video_count`, `country`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "channel_id": null,
    "username": null,
    "title": null,
    "profile_url": null,
    "description": null,
    "subscriber_count": null,
    "video_count": null,
    "country": null
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

## `GET /api/v1/youtube/realtime/user/videos`
- operationId: `youtube_realtime_user_videos`
- summary: 实时采集-用户视频
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | channel_id |
| `offset` | `query` | `false` | `string` | offset |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeYoutubeUserVideosRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `more`, `offset`, `videos`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "more": null,
    "offset": null,
    "videos": null
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

## `GET /api/v1/youtube/realtime/video/detail`
- operationId: `youtube_realtime_video_detail`
- summary: 实时采集-视频详情
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `video_id` | `query` | `true` | `string` | video_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_RealTimeYoutubeVideoInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `video_id`, `title`, `description`, `create_at`, `duration`, `video_url`, `channel_title`, `channel_id`, `video_type`, `category_id`, `caption`, `like_count`, `comment_count`, `play_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "video_id": null,
    "title": null,
    "description": null,
    "create_at": null,
    "duration": null,
    "video_url": null,
    "channel_title": null,
    "channel_id": null
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
