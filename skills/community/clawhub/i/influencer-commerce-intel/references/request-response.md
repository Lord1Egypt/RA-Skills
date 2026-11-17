# Request and Response Guide

## `GET /api/v1/tiktok/realtime/product/detail`
- operationId: `tiktok_realtime_product_detail`
- summary: 实时采集-商品详情
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `product_id` | `query` | `true` | `string` | 视频ID |
| `region` | `query` | `true` | `string` | country code:US,VN... |
| `user_id` | `query` | `false` | `string` | tiktok user id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_dict_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: none
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {}
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

## `GET /api/v1/tiktok/user/shop/goods/list`
- operationId: `tiktok_user_shop_goods_list`
- summary: 用户带货商品列表
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `page` | `query` | `false` | `integer` | 页码 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_TiktokUserShopGoodsItem__` |
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
        "goods_id": "1731491957866860552",
        "goods_name": "THE MONSTERS Let's Checkmate Series-Vinyl Plush Doll",
        "goods_pic_url": "https://d3uucz7wx6jq40.cloudfront.net/tiktok.product/1731491957866860552/cover.png",
        "currency_symbol": "$",
        "goods_price": "114.99",
        "goods_sales_revenue": "240559.08",
        "goods_sales_volumn": 2092
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "total_pages": 10
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

## `GET /api/v1/tiktok/user/shop/live/list`
- operationId: `tiktok_user_shop_live_list`
- summary: 用户带货直播列表
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `sort_field` | `query` | `false` | `string` | 排序字段，live_revenue_amount, live_view_count, live_price, live_revenue_per_thousand |
| `sort_type` | `query` | `false` | `string` | 排序类型, asc:升序, desc:降序 |
| `page` | `query` | `false` | `integer` | 页码 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_TiktokUserShopLiveItem__` |
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
        "live_name": "SKULLPANDA Launch!",
        "live_cover_url": "https://d3uucz7wx6jq40.cloudfront.net/tiktok.live/7541145940804029239/cover.png",
        "live_start_time": "08/22 05:00",
        "live_end_time": "08/22 17:08",
        "live_duration": "12.1h",
        "live_revenue_amount": "405921.55",
        "live_view_count": 1647040,
        "live_price": "43.76"
      }
    ],
    "total": 35,
    "page": 1,
    "page_size": 10,
    "total_pages": 4
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

## `GET /api/v1/tiktok/user/shop/sale`
- operationId: `tiktok_user_shop_sale`
- summary: 用户带货数据
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_TiktokUserShopSaleRes_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `currency_symbol`, `revenue_amount`, `sales_volumn`, `video_revenue_amount`, `live_revenue_amount`, `avg_sales_price`, `live_views_number`, `video_views_number`, `new_followers_number`, `start_time`, `end_time`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "currency_symbol": "$",
    "revenue_amount": "3132136.98",
    "sales_volumn": 83007,
    "video_revenue_amount": "309.90",
    "live_revenue_amount": "3123058.84",
    "avg_sales_price": "37.73",
    "live_views_number": 22712398,
    "video_views_number": 13409031
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

## `GET /api/v1/tiktok/user/shop/video/ad/list`
- operationId: `tiktok_user_shop_video_ad_list`
- summary: 用户带货视频广告列表
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `sort_field` | `query` | `false` | `string` | 排序字段，revenue_amount, views_count, ads_deal_rate, ads_view_rate, ads_roas_rate |
| `sort_type` | `query` | `false` | `string` | 排序类型, asc:升序, desc:降序 |
| `page` | `query` | `false` | `integer` | 页码 |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_BasePage_TiktokUserShopVideoAdItem__` |
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
        "video_id": "7483378078563962142",
        "video_description": "I love.❤️  #popmart #skullpanda #wintersymphony #blindbox #vinyl #plush ",
        "video_url": "https://www.tiktok.com/@popmart.usshop/video/7483378078563962142",
        "video_cover_url": "https://d3uucz7wx6jq40.cloudfront.net/tiktok.video/7483378078563962142/cover.png",
        "video_publish_at": "2024-03-29",
        "revenue_amount": "309.90",
        "view_count": 47129,
        "like_count": 18310
      }
    ],
    "total": 47,
    "page": 1,
    "page_size": 10,
    "total_pages": 5
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
