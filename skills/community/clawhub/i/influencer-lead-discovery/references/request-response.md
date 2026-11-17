# Request and Response Guide

## `GET /api/ping`
- operationId: `ping`
- summary: ping
- parameters: none
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `string` |
- `200` top-level fields: none
- `200` data level-1 fields: none
- `200` minimal example:
```json
"string"
```

## `GET /api/v1/instagram/user/brands`
- operationId: `instagram_user_brands`
- summary: 合作品牌
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `page` | `query` | `false` | `integer` | 页码 |
| `page_size` | `query` | `false` | `integer` | 每页数量 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_VideoBrandCollaborationItem__` |
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

## `GET /api/v1/instagram/user/hashtag/engagement`
- operationId: `instagram_user_hashtag_engagement`
- summary: 用户top10 hashtag互动数据
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_KolHashtagEngagementRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.hashtag`, `items.frequency`, `items.engagement_rate_median`, `items.engagement_rate_mean`, `items.views_median`, `items.interactions_median`, `items.interactions_total`, `items.grade`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "hashtag": "#Clips",
      "frequency": 10,
      "engagement_rate_median": "7.89%",
      "engagement_rate_mean": "8.09%",
      "views_median": 26817,
      "interactions_median": "2548.50",
      "interactions_total": 27655,
      "grade": "A"
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

## `GET /api/v1/instagram/user/info`
- operationId: `instagram_db_user_info`
- summary: 用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_InstagramUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `user_id`, `related_platforms`, `username`, `nickname`, `avatar`, `description`, `channel_url`, `follower_count`, `country`, `language`, `gender`, `is_business_account`, `is_verified`, `tags`, `publish_count_month`, `publish_count_week`, `last_publish_at`, `total_media_count`, `total_video_count`, `avg_engagement_rate_5`, `avg_view_rate_5`, `avg_like_count_5`, `avg_comment_count_5`, `avg_engagement_rate_10`, `avg_view_rate_10`, `avg_like_count_10`, `avg_comment_count_10`, `avg_engagement_rate_30`, `avg_view_rate_30`, `avg_like_count_30`, `avg_comment_count_30`, `med_engagement_rate_30`, `med_view_rate_30`, `med_like_count_30`, `med_comment_count_30`, `evaluation_min`, `evaluation_max`, `last_update_at`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "user_id": "695995017",
    "related_platforms": [],
    "username": "chanelofficial",
    "nickname": "CHANEL",
    "avatar": "https://img.scrumball.cn/instagram/Fnu9-hyneWMt_HWQsMQJz7WK5nmG",
    "description": "",
    "channel_url": "https://www.instagram.com/chanelofficial/",
    "follower_count": 59840913
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

## `GET /api/v1/instagram/user/medias`
- operationId: `instagram_db_user_medias`
- summary: 用户贴文
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `publish_at_start` | `query` | `false` | `string` | 发布时间开始 |
| `publish_at_end` | `query` | `false` | `string` | 发布时间结束 |
| `media_code` | `query` | `false` | `string` | 帖子Code |
| `is_paid` | `query` | `false` | `integer \| string` | 是否合作帖子，1:是 |
| `page` | `query` | `false` | `integer` | Page number |
| `page_size` | `query` | `false` | `integer` | Page size |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_InstagramUserMediaItem__` |
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
      {
        "media_code": "DKruTaYRac_",
        "media_url": "https://www.instagram.com/p/DKruTaYRac_/",
        "description": "The future of tennis is in good hands.",
        "cover_url": "https://img.scrumball.cn/instagram/Fpr2ndmGyZJECypIFBKcbklDFT3B?imageView2/2/w/300",
        "publish_at": "2025-06-09 22:20:35",
        "like_count": 144865,
        "comment_count": 376,
        "view_count": 0
      }
    ],
    "total": 765,
    "page": 1,
    "page_size": 1,
    "total_pages": 765
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

## `GET /api/v1/instagram/user/similar`
- operationId: `instagram_user_similar`
- summary: 相似用户推荐
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_InstagramUserSimilarItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.username`, `items.nickname`, `items.avatar`, `items.description`, `items.follower_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "username": "psg",
      "nickname": "Paris Saint-Germain",
      "avatar": "https://img.scrumball.cn/FrnaI8Vmawgv7_lzJnvZ5oNwP31z",
      "description": "CHAMPIONS D’EUROPE 🏆❤️💙",
      "follower_count": 65722412
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

## `POST /api/v1/search/instagram/media`
- operationId: `search_instagram_media`
- summary: 搜索instagram帖文
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchInstagramMediaReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchInstagramMediaRep__` |
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

## `POST /api/v1/search/instagram/user`
- operationId: `search_instagram_user`
- summary: 搜索instagram用户
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchInstagramUserReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchInstagramUserRep__` |
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

## `POST /api/v1/search/suggest`
- operationId: `search_instagram_suggest`
- summary: 搜索联想
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `platform` | `query` | `true` | `string` | 平台: youtube/tiktok/instagram |
| `query` | `query` | `true` | `string` | 搜索关键词 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_SearchSuggestItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.platform`, `items.user_id`, `items.username`, `items.display_name`, `items.avatar`, `items.country`, `items.gender`, `items.follower_count`, `items.avg_engagement_rate`, `items.avg_comment_count`, `items.avg_like_count`, `items.avg_play_count`, `items.video_count`, `items.last_publish_at`, `items.recent_month_publish_count`, `items.recent_week_publish_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "platform": "youtube",
      "user_id": "UCzBDWY1snLBV8ykf_3mw8Eg",
      "username": "telefoninopuntonet",
      "display_name": "TELEFONINO.NET",
      "avatar": "https://img.scrumball.cn/FiZmqu2ha908kFqJlHC7tFbsId0-",
      "country": "IT",
      "gender": "unknown",
      "follower_count": 312000
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

## `POST /api/v1/search/tiktok/user`
- operationId: `search_tiktok_user`
- summary: 搜索tiktok用户
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchTiktokUserReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchTiktokUserRep__` |
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

## `POST /api/v1/search/tiktok/video`
- operationId: `search_tiktok_video`
- summary: 搜索tiktok视频
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchTiktokVideoReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchTiktokVideoRep__` |
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

## `POST /api/v1/search/youtube/user`
- operationId: `search_youtube_user`
- summary: 搜索youtube用户
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchYoutubeUserReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchYoutubeUserRep__` |
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

## `POST /api/v1/search/youtube/video`
- operationId: `search_youtube_video`
- summary: 搜索youtube视频
- parameters: none
- requestBody:
| content-type | schema | required fields |
|---|---|---|
| `application/json` | `SearchYoutubeVideoReq` | `query` |
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_SearchYoutubeVideoRep__` |
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

## `GET /api/v1/tiktok/user/brands`
- operationId: `tiktok_user_brands`
- summary: 合作品牌
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `page` | `query` | `false` | `integer` | 页码 |
| `page_size` | `query` | `false` | `integer` | 每页数量 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_VideoBrandCollaborationItem__` |
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

## `GET /api/v1/tiktok/user/hashtag/engagement`
- operationId: `tiktok_user_hashtag_engagement`
- summary: 用户top10 hashtag互动数据
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_KolHashtagEngagementRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.hashtag`, `items.frequency`, `items.engagement_rate_median`, `items.engagement_rate_mean`, `items.views_median`, `items.interactions_median`, `items.interactions_total`, `items.grade`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "hashtag": "#Clips",
      "frequency": 10,
      "engagement_rate_median": "7.89%",
      "engagement_rate_mean": "8.09%",
      "views_median": 26817,
      "interactions_median": "2548.50",
      "interactions_total": 27655,
      "grade": "A"
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

## `GET /api/v1/tiktok/user/info`
- operationId: `tiktok_db_user_info`
- summary: 用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `false` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_TiktokUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `user_id`, `related_platforms`, `unique_id`, `nickname`, `channel_url`, `description`, `avatar`, `country`, `language`, `gender`, `follower_count`, `following_count`, `is_verified`, `is_private`, `tags`, `publish_count_month`, `publish_count_week`, `last_publish_at`, `total_video_count`, `total_like_count`, `avg_engagement_rate_5`, `avg_view_rate_5`, `avg_view_count_5`, `avg_comment_count_5`, `avg_like_count_5`, `avg_share_count_5`, `avg_engagement_rate_10`, `avg_view_rate_10`, `avg_view_count_10`, `avg_comment_count_10`, `avg_like_count_10`, `avg_share_count_10`, `avg_engagement_rate_30`, `avg_view_rate_30`, `avg_view_count_30`, `avg_comment_count_30`, `avg_like_count_30`, `avg_share_count_30`, `med_engagement_rate_30`, `med_view_rate_30`, `med_view_count_30`, `med_comment_count_30`, `med_like_count_30`, `med_share_count_30`, `evaluation_min`, `evaluation_max`, `last_update_at`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "user_id": "208464585232822272",
    "related_platforms": [
      {
        "platform": "youtube",
        "platform_url": "https://www.youtube.com/channel/UCUFgkRb0ZHc4Rpq15VRCICA"
      }
    ],
    "unique_id": "nike",
    "nickname": "Nike",
    "channel_url": "https://www.tiktok.com/@nike",
    "description": "Just Do It.",
    "avatar": "https://img.scrumball.cn/tiktok/Fs6qFtdehp7X-BBzS8tfmaB46mB8",
    "country": "US"
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

## `GET /api/v1/tiktok/user/similar`
- operationId: `tiktok_user_similar`
- summary: 相似用户推荐
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `false` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_TiktokUserSimilarItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.unique_id`, `items.nickname`, `items.description`, `items.avatar`, `items.follower_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "unique_id": "joshotusanya",
      "nickname": "Josh Otusanya 🇳🇬",
      "description": "American Stand up Comedian \nSelf Help | Comedy | Lifestyle\n📍Barcelona • 🇺🇸🇳🇬 \njosh@joshotusanya.com\nLive Shows/Newsletter/Free Guides ⤵️",
      "avatar": "https://img.scrumball.cn/Fr6IT6ZSn00Mvv--iHRo0pp4YdoH",
      "follower_count": 7520125
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

## `GET /api/v1/tiktok/user/videos`
- operationId: `tiktok_db_user_videos`
- summary: 用户视频
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `publish_at_start` | `query` | `false` | `string` | 发布时间开始 |
| `publish_at_end` | `query` | `false` | `string` | 发布时间结束 |
| `video_id` | `query` | `false` | `string` | 视频ID |
| `is_paid` | `query` | `false` | `integer \| string` | 是否合作视频，1:是 |
| `page` | `query` | `false` | `integer` | Page number |
| `page_size` | `query` | `false` | `integer` | Page size |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_TiktokUserVideoInfoItem__` |
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
      {
        "video_id": "7508413737670413614",
        "description": "Things you might experience on Fly Vini Airlines with captain @Vini Jr.: speed, samba and smiles. #NikeFootball ",
        "video_url": "https://www.tiktok.com/@nike/video/7508413737670413614",
        "cover_url": "https://img.scrumball.cn/tiktok/FuaboiN2W8mT6WnSCI9Qs1Ywo9LE?imageView2/2/w/300",
        "duration_second": 32,
        "tags": [
          null
        ],
        "publish_at": "2025-05-26 00:00:39",
        "view_count": 188037
      }
    ],
    "total": 704,
    "page": 1,
    "page_size": 1,
    "total_pages": 704
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

## `GET /api/v1/youtube/user/brands`
- operationId: `youtube_user_brands`
- summary: 合作品牌
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `page` | `query` | `false` | `integer` | 页码 |
| `page_size` | `query` | `false` | `integer` | 每页数量 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_VideoBrandCollaborationItem__` |
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

## `GET /api/v1/youtube/user/hashtag/engagement`
- operationId: `youtube_user_hashtag_engagement`
- summary: 用户top10 hashtag互动数据
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_KolHashtagEngagementRes__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.hashtag`, `items.frequency`, `items.engagement_rate_median`, `items.engagement_rate_mean`, `items.views_median`, `items.interactions_median`, `items.interactions_total`, `items.grade`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "hashtag": "#Clips",
      "frequency": 10,
      "engagement_rate_median": "7.89%",
      "engagement_rate_mean": "8.09%",
      "views_median": 26817,
      "interactions_median": "2548.50",
      "interactions_total": 27655,
      "grade": "A"
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

## `GET /api/v1/youtube/user/info`
- operationId: `youtube_db_user_info`
- summary: 用户信息
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `false` | `string` | channel_id |
| `username` | `query` | `false` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_YoutubeUserInfoRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `channel_id`, `related_platforms`, `title`, `channel_url`, `avatar`, `description`, `gender`, `country`, `language`, `tags`, `register_at`, `subscriber_count`, `publish_count_month`, `publish_count_week`, `last_publish_at`, `total_video_count`, `total_view_count`, `avg_view_count`, `avg_engagement_rate_5`, `avg_view_rate_5`, `avg_view_count_5`, `avg_comment_count_5`, `avg_like_count_5`, `avg_engagement_rate_10`, `avg_view_rate_10`, `avg_view_count_10`, `avg_comment_count_10`, `avg_like_count_10`, `avg_engagement_rate_30`, `avg_view_rate_30`, `avg_view_count_30`, `avg_comment_count_30`, `avg_like_count_30`, `med_engagement_rate_30`, `med_view_rate_30`, `med_view_count_30`, `med_comment_count_30`, `med_like_count_30`, `evaluation_min`, `evaluation_max`, `last_update_at`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "channel_id": "UCX6OQ3DkcsbYNE6H8uQQuVA",
    "related_platforms": [],
    "title": "MrBeast",
    "channel_url": "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",
    "avatar": "https://img.scrumball.cn/FpiY4unAm7NroQ3dS4heDOp89moK",
    "description": "SUBSCRIBE FOR A COOKIE!\nNew MrBeast or MrBeast Gaming video every single Saturday at noon eastern time!\nAccomplishments:\n- Raised $20,000,000 To Plant 20,000,000 Trees\n- Removed 30,000,000 pounds of trash from the ocean\n- Helped 2,000 people walk again\n- Helped 1,000 blind people see\n- Helped 1,000 deaf people hear\n- Built wells in Africa\n- Built and gave away 100 houses\n- Adopted every dog in a shelter (twice)\n- Given millions to charity\n- Started my own snack company Feastables\n- Started my own software company Viewstats\n- Started Lunchly, a tasty, better-for-you lunch option\n- Gave away a private island (twice)\n- Gave away 1 million meals\n- I counted to 100k\n- Ran a marathon in the world's largest shoes\n- Survived 50 hours in Antarctica\n- Recreated Squid Game in real life\n- Created the largest competition show with 1000 people (Beast Games)\n- Gave $5,000,000 to one person\n- Passed T-Series to become most subscribed YouTube channel 🥹\nyou get it, I appreciate all of you so much :)\n",
    "gender": "male",
    "country": "US"
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

## `GET /api/v1/youtube/user/similar`
- operationId: `youtube_user_similar`
- summary: 相似用户推荐
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `false` | `string` | channel_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_YoutubeUserSimilarItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.channel_id`, `items.title`, `items.avatar`, `items.description`, `items.subscriber_count`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "channel_id": "UClNwztERQAfHAb9zKWuelAg",
      "title": "Cleaning The Dirtiest",
      "avatar": "https://img.scrumball.cn/FjZ6BIztbbmQPMxKixn16DvwoCH3",
      "description": "Cleaning The Dirtiest. ",
      "subscriber_count": 2110000
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

## `GET /api/v1/youtube/user/videos`
- operationId: `youtube_db_user_videos`
- summary: 用户视频
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `publish_at_start` | `query` | `false` | `string` | 发布时间开始 |
| `publish_at_end` | `query` | `false` | `string` | 发布时间结束 |
| `video_id` | `query` | `false` | `string` | 视频ID |
| `is_paid` | `query` | `false` | `integer \| string` | 是否合作视频，1:是 |
| `page` | `query` | `false` | `integer` | Page number |
| `page_size` | `query` | `false` | `integer` | Page size |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_YoutubeUserVideoInfoItem__` |
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
      {
        "video_id": "hTSaweR8qMI",
        "video_url": "https://www.youtube.com/watch?v=hTSaweR8qMI",
        "title": "$1 vs $500,000 Romantic Date",
        "description": "Experiencing all of this was incredible\nBuy Feastables! It tastes amazing and it's ethically sourced 👉 https://fstbls.com/5mj6dv\n\nNew Merch - https://mrbeast.store\n\nCheck out Viewstats! - https://www.viewstats.com/\n\nSUBSCRIBE OR I TAKE YOUR DOG\n╔═╦╗╔╦╗╔═╦═╦╦╦╦╗╔═╗\n║╚╣║║║╚╣╚╣╔╣╔╣║╚╣═╣ \n╠╗║╚╝║║╠╗║╚╣║║║║║═╣\n╚═╩══╩═╩═╩═╩╝╚╩═╩═╝\n\nFor any questions or inquiries regarding this video, please reach out to chucky@mrbeastbusiness.com\n\n----------------------------------------------------------------\nfollow all of these or i will kick you\n• Facebook - https://www.facebook.com/MrBeast/\n• Twitter - https://twitter.com/MrBeast\n•  Instagram - https://www.instagram.com/mrbeast\n•  Im Hiring! - https://www.mrbeastjobs.com/\n--------------------------------------------------------------------",
        "cover_url": "https://img.scrumball.cn/FskvLUVwLC3ka5xax-Tw1APV80on?imageView2/2/w/300",
        "publish_at": "2025-06-08 00:00:00",
        "duration_second": 1042,
        "like_count": 1892706
      }
    ],
    "total": 293,
    "page": 1,
    "page_size": 1,
    "total_pages": 293
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
