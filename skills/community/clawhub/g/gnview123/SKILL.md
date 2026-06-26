# Skill: 抖音信息提取器
## 1. 描述
通过Douyin TikTok Download API获取抖音/TikTok/Bilibili视频数据信息，支持多种API接口。

## 2. 配置信息
配置文件：`config.json`

```json
{
  "api_name": "Douyin TikTok Download API",
  "version": "V4.1.2",
  "host": "http://xxx.com",
  "base_url": "http://xxx.com",
}
```

## Bilibili-Web-API

### GET /api/bilibili/web/fetch_one_video
**Summary**: 获取单个视频详情信息/Get single video data

**Description**:
# [中文]
### 用途:
- 获取单个视频详情信息
### 参数:
- bv_id: 作品id
### 返回:
- 视频详情信息

# [English]
### Purpose:
- Get single video data
### Parameters:
- bv_id: Video id
### Return:
- Video data

# [示例/Example]
bv_id = "BV1M1421t7hT"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |


### GET /api/bilibili/web/fetch_video_playurl
**Summary**: 获取视频流地址/Get video playurl

**Description**:
# [中文]
### 用途:
- 获取视频流地址
### 参数:
- bv_id: 作品id
- cid: 作品cid
### 返回:
- 视频流地址

# [English]
### Purpose:
- Get video playurl
### Parameters:
- bv_id: Video id
- cid: Video cid
### Return:
- Video playurl

# [示例/Example]
bv_id = "BV1y7411Q7Eq"
cid = "171776208"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |
| cid | string | 是 | 作品cid/Video cid |


### GET /api/bilibili/web/fetch_user_post_videos
**Summary**: 获取用户主页作品数据/Get user homepage video data

**Description**:
# [中文]
### 用途:
- 获取用户发布的视频数据
### 参数:
- uid: 用户UID
- pn: 页码
### 返回:
- 用户发布的视频数据

# [English]
### Purpose:
- Get user post video data
### Parameters:
- uid: User UID
- pn: Page number
### Return:
- User posted video data

# [示例/Example]
uid = "178360345"
pn = 1

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| uid | string | 是 | 用户UID |
| pn | integer | 否 | 页码/Page number |


### GET /api/bilibili/web/fetch_collect_folders
**Summary**: 获取用户所有收藏夹信息/Get user collection folders

**Description**:
# [中文]
### 用途:
- 获取用户收藏作品数据
### 参数:
- uid: 用户UID
### 返回:
- 用户收藏夹信息

# [English]
### Purpose:
- Get user collection folders
### Parameters:
- uid: User UID
### Return:
- user collection folders

# [示例/Example]
uid = "178360345"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| uid | string | 是 | 用户UID |


### GET /api/bilibili/web/fetch_user_collection_videos
**Summary**: 获取指定收藏夹内视频数据/Gets video data from a collection folder

**Description**:
# [中文]
### 用途:
- 获取指定收藏夹内视频数据
### 参数:
- folder_id: 用户UID
- pn: 页码
### 返回:
- 指定收藏夹内视频数据

# [English]
### Purpose:
- Gets video data from a collection folder
### Parameters:
- folder_id: collection folder id
- pn: Page number
### Return:
- video data from collection folder

# [示例/Example]
folder_id = "1756059545"
pn = 1

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| folder_id | string | 是 | 收藏夹id/collection folder id |
| pn | integer | 否 | 页码/Page number |


### GET /api/bilibili/web/fetch_user_profile
**Summary**: 获取指定用户的信息/Get information of specified user

**Description**:
# [中文]
### 用途:
- 获取指定用户的信息
### 参数:
- uid: 用户UID
### 返回:
- 指定用户的个人信息

# [English]
### Purpose:
- Get information of specified user
### Parameters:
- uid: User UID
### Return:
- information of specified user

# [示例/Example]
uid = "178360345"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| uid | string | 是 | 用户UID |


### GET /api/bilibili/web/fetch_com_popular
**Summary**: 获取综合热门视频信息/Get comprehensive popular video information

**Description**:
# [中文]
### 用途:
- 获取综合热门视频信息
### 参数:
- pn: 页码
### 返回:
- 综合热门视频信息

# [English]
### Purpose:
- Get comprehensive popular video information
### Parameters:
- pn: Page number
### Return:
- comprehensive popular video information

# [示例/Example]
pn = 1

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| pn | integer | 否 | 页码/Page number |


### GET /api/bilibili/web/fetch_video_comments
**Summary**: 获取指定视频的评论/Get comments on the specified video

**Description**:
# [中文]
### 用途:
- 获取指定视频的评论
### 参数:
- bv_id: 作品id
- pn: 页码
### 返回:
- 指定视频的评论数据

# [English]
### Purpose:
- Get comments on the specified video
### Parameters:
- bv_id: Video id
- pn: Page number
### Return:
- comments of the specified video

# [示例/Example]
bv_id = "BV1M1421t7hT"
pn = 1

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |
| pn | integer | 否 | 页码/Page number |


### GET /api/bilibili/web/fetch_comment_reply
**Summary**: 获取视频下指定评论的回复/Get reply to the specified comment

**Description**:
# [中文]
### 用途:
- 获取视频下指定评论的回复
### 参数:
- bv_id: 作品id
- pn: 页码
- rpid: 回复id
### 返回:
- 指定评论的回复数据

# [English]
### Purpose:
- Get reply to the specified comment
### Parameters:
- bv_id: Video id
- pn: Page number
- rpid: Reply id
### Return:
- Reply of the specified comment

# [示例/Example]
bv_id = "BV1M1421t7hT"
pn = 1
rpid = "237109455120"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |
| pn | integer | 否 | 页码/Page number |
| rpid | string | 是 | 回复id/Reply id |


### GET /api/bilibili/web/fetch_user_dynamic
**Summary**: 获取指定用户动态/Get dynamic information of specified user

**Description**:
# [中文]
### 用途:
- 获取指定用户动态
### 参数:
- uid: 用户UID
- offset: 开始索引
### 返回:
- 指定用户动态数据

# [English]
### Purpose:
- Get dynamic information of specified user
### Parameters:
- uid: User UID
- offset: offset
### Return:
- dynamic information of specified user

# [示例/Example]
uid = "178360345"
offset = "953154282154098691"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| uid | string | 是 | 用户UID |
| offset | string | 否 | 开始索引/offset |


### GET /api/bilibili/web/fetch_video_danmaku
**Summary**: 获取视频实时弹幕/Get Video Danmaku

**Description**:
# [中文]
### 用途:
- 获取视频实时弹幕
### 参数:
- cid: 作品cid
### 返回:
- 视频实时弹幕

# [English]
### Purpose:
- Get Video Danmaku
### Parameters:
- cid: Video cid
### Return:
- Video Danmaku

# [示例/Example]
cid = "1639235405"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| cid | string | 是 | 作品cid/Video cid |


### GET /api/bilibili/web/fetch_live_room_detail
**Summary**: 获取指定直播间信息/Get information of specified live room

**Description**:
# [中文]
### 用途:
- 获取指定直播间信息
### 参数:
- room_id: 直播间ID
### 返回:
- 指定直播间信息

# [English]
### Purpose:
- Get information of specified live room
### Parameters:
- room_id: Live room ID
### Return:
- information of specified live room

# [示例/Example]
room_id = "22816111"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| room_id | string | 是 | 直播间ID/Live room ID |


### GET /api/bilibili/web/fetch_live_videos
**Summary**: 获取直播间视频流/Get live video data of specified room

**Description**:
# [中文]
### 用途:
- 获取指定直播间视频流
### 参数:
- room_id: 直播间ID
### 返回:
- 指定直播间视频流

# [English]
### Purpose:
- Get live video data of specified room
### Parameters:
- room_id: Live room ID
### Return:
- live video data of specified room

# [示例/Example]
room_id = "1815229528"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| room_id | string | 是 | 直播间ID/Live room ID |


### GET /api/bilibili/web/fetch_live_streamers
**Summary**: 获取指定分区正在直播的主播/Get live streamers of specified live area

**Description**:
# [中文]
### 用途:
- 获取指定分区正在直播的主播
### 参数:
- area_id: 直播分区id
- pn: 页码
### 返回:
- 指定分区正在直播的主播

# [English]
### Purpose:
- Get live streamers of specified live area
### Parameters:
- area_id: Live area ID
- pn: Page number
### Return:
- live streamers of specified live area

# [示例/Example]
area_id = "9"
pn = 1

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| area_id | string | 是 | 直播分区id/Live area ID |
| pn | integer | 否 | 页码/Page number |


### GET /api/bilibili/web/fetch_all_live_areas
**Summary**: 获取所有直播分区列表/Get a list of all live areas

**Description**:
# [中文]
### 用途:
- 获取所有直播分区列表
### 参数:
### 返回:
- 所有直播分区列表

# [English]
### Purpose:
- Get a list of all live areas
### Parameters:
### Return:
- list of all live areas

# [示例/Example]


### GET /api/bilibili/web/bv_to_aid
**Summary**: 通过bv号获得视频aid号/Generate aid by bvid

**Description**:
# [中文]
### 用途:
- 通过bv号获得视频aid号
### 参数:
- bv_id: 作品id
### 返回:
- 视频aid号

# [English]
### Purpose:
- Generate aid by bvid
### Parameters:
- bv_id: Video id
### Return:
- Video aid

# [示例/Example]
bv_id = "BV1M1421t7hT"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |


### GET /api/bilibili/web/fetch_video_parts
**Summary**: 通过bv号获得视频分p信息/Get Video Parts By bvid

**Description**:
# [中文]
### 用途:
- 通过bv号获得视频分p信息
### 参数:
- bv_id: 作品id
### 返回:
- 视频分p信息

# [English]
### Purpose:
- Get Video Parts By bvid
### Parameters:
- bv_id: Video id
### Return:
- Video Parts

# [示例/Example]
bv_id = "BV1vf421i7hV"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| bv_id | string | 是 | 作品id/Video id |


## Douyin-Web-API

### GET /api/douyin/web/fetch_one_video
**Summary**: 获取单个作品数据/Get single video data

**Description**:
# [中文]
### 用途:
- 获取单个作品数据
### 参数:
- aweme_id: 作品id
### 返回:
- 作品数据

# [English]
### Purpose:
- Get single video data
### Parameters:
- aweme_id: Video id
### Return:
- Video data

# [示例/Example]
aweme_id = "7372484719365098803"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| aweme_id | string | 是 | 作品id/Video id |


### GET /api/douyin/web/fetch_user_post_videos
**Summary**: 获取用户主页作品数据/Get user homepage video data

**Description**:
# [中文]
### 用途:
- 获取用户主页作品数据
### 参数:
- sec_user_id: 用户sec_user_id
- max_cursor: 最大游标
- count: 最大数量
### 返回:
- 用户主页作品数据

# [English]
### Purpose:
- Get user homepage video data
### Parameters:
- sec_user_id: User sec_user_id
- max_cursor: Maximum cursor
- count: Maximum count number
### Return:
- User video data

# [示例/Example]
sec_user_id = "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"
max_cursor = 0
counts = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| sec_user_id | string | 是 | 用户sec_user_id/User sec_user_id |
| max_cursor | integer | 否 | 最大游标/Maximum cursor |
| count | integer | 否 | 每页数量/Number per page |


### GET /api/douyin/web/fetch_user_like_videos
**Summary**: 获取用户喜欢作品数据/Get user like video data

**Description**:
# [中文]
### 用途:
- 获取用户喜欢作品数据
### 参数:
- sec_user_id: 用户sec_user_id
- max_cursor: 最大游标
- count: 最大数量
### 返回:
- 用户作品数据

# [English]
### Purpose:
- Get user like video data
### Parameters:
- sec_user_id: User sec_user_id
- max_cursor: Maximum cursor
- count: Maximum count number
### Return:
- User video data

# [示例/Example]
sec_user_id = "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
max_cursor = 0
counts = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| sec_user_id | string | 是 | 用户sec_user_id/User sec_user_id |
| max_cursor | integer | 否 | 最大游标/Maximum cursor |
| counts | integer | 否 | 每页数量/Number per page |


### GET /api/douyin/web/fetch_user_collection_videos
**Summary**: 获取用户收藏作品数据/Get user collection video data

**Description**:
# [中文]
### 用途:
- 获取用户收藏作品数据
### 参数:
- cookie: 用户网页版抖音Cookie(此接口需要用户提供自己的Cookie)
- max_cursor: 最大游标
- count: 最大数量
### 返回:
- 用户作品数据

# [English]
### Purpose:
- Get user collection video data
### Parameters:
- cookie: User's web version of Douyin Cookie (This interface requires users to provide their own Cookie)
- max_cursor: Maximum cursor
- count: Maximum number
### Return:
- User video data

# [示例/Example]
cookie = "YOUR_COOKIE"
max_cursor = 0
counts = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| cookie | string | 是 | 用户网页版抖音Cookie/Your web version of Douyin Cookie |
| max_cursor | integer | 否 | 最大游标/Maximum cursor |
| counts | integer | 否 | 每页数量/Number per page |


### GET /api/douyin/web/fetch_user_mix_videos
**Summary**: 获取用户合辑作品数据/Get user mix video data

**Description**:
# [中文]
### 用途:
- 获取用户合辑作品数据
### 参数:
- mix_id: 合辑id
- max_cursor: 最大游标
- count: 最大数量
### 返回:
- 用户作品数据

# [English]
### Purpose:
- Get user mix video data
### Parameters:
- mix_id: Mix id
- max_cursor: Maximum cursor
- count: Maximum number
### Return:
- User video data

# [示例/Example]
url = https://www.douyin.com/collection/7348687990509553679
mix_id = "7348687990509553679"
max_cursor = 0
counts = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| mix_id | string | 是 | 合辑id/Mix id |
| max_cursor | integer | 否 | 最大游标/Maximum cursor |
| counts | integer | 否 | 每页数量/Number per page |


### GET /api/douyin/web/fetch_user_live_videos
**Summary**: 获取用户直播流数据/Get user live video data

**Description**:
# [中文]
### 用途:
- 获取用户直播流数据
### 参数:
- webcast_id: 直播间webcast_id
### 返回:
- 直播流数据

# [English]
### Purpose:
- Get user live video data
### Parameters:
- webcast_id: Room webcast_id
### Return:
- Live stream data

# [示例/Example]
webcast_id = "285520721194"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| webcast_id | string | 是 | 直播间webcast_id/Room webcast_id |


### GET /api/douyin/web/fetch_user_live_videos_by_room_id
**Summary**: 获取指定用户的直播流数据/Get live video data of specified user

**Description**:
# [中文]
### 用途:
- 获取指定用户的直播流数据
### 参数:
- room_id: 直播间room_id
### 返回:
- 直播流数据

# [English]
### Purpose:
- Get live video data of specified user
### Parameters:
- room_id: Room room_id
### Return:
- Live stream data

# [示例/Example]
room_id = "7318296342189919011"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| room_id | string | 是 | 直播间room_id/Room room_id |


### GET /api/douyin/web/fetch_live_gift_ranking
**Summary**: 获取直播间送礼用户排行榜/Get live room gift user ranking

**Description**:
# [中文]
### 用途:
- 获取直播间送礼用户排行榜
### 参数:
- room_id: 直播间room_id
- rank_type: 排行类型，默认为30不用修改。
### 返回:
- 排行榜数据

# [English]
### Purpose:
- Get live room gift user ranking
### Parameters:
- room_id: Room room_id
- rank_type: Leaderboard type, default is 30, no need to modify.
### Return:
- Leaderboard data

# [示例/Example]
room_id = "7356585666190461731"
rank_type = 30

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| room_id | string | 是 | 直播间room_id/Room room_id |
| rank_type | integer | 否 | 排行类型/Leaderboard type |


### GET /api/douyin/web/fetch_live_room_product_result
**Summary**: 抖音直播间商品信息/Douyin live room product information

**Description**:
# [中文]
### 用途:
- 抖音直播间商品信息
### 参数:
- cookie: 用户网页版抖音Cookie(此接口需要用户提供自己的Cookie，如获取失败请手动过一次验证码)
- room_id: 直播间room_id
- author_id: 作者id
- limit: 数量
### 返回:
- 商品信息

# [English]
### Purpose:
- Douyin live room product information
### Parameters:
- cookie: User's web version of Douyin Cookie (This interface requires users to provide their own Cookie, if the acquisition fails, please manually pass the captcha code once)
- room_id: Room room_id
- author_id: Author id
- limit: Number
### Return:
- Product information

# [示例/Example]
cookie = "YOUR_COOKIE"
room_id = "7356742011975715619"
author_id = "2207432981615527"
limit = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| cookie | string | 是 | 用户网页版抖音Cookie/Your web version of Douyin Cookie |
| room_id | string | 是 | 直播间room_id/Room room_id |
| author_id | string | 是 | 作者id/Author id |
| limit | integer | 否 | 数量/Number |


### GET /api/douyin/web/handler_user_profile
**Summary**: 获取指定用户的信息/Get information of specified user

**Description**:
# [中文]
### 用途:
- 获取指定用户的信息
### 参数:
- sec_user_id: 用户sec_user_id
### 返回:
- 用户信息，包含用户的unique_id(抖音号)。

# [English]
### Purpose:
- Get information of specified user
### Parameters:
- sec_user_id: User sec_user_id
### Return:
- User information

# [示例/Example]
sec_user_id = "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| sec_user_id | string | 是 | 用户sec_user_id/User sec_user_id |


### GET /api/douyin/web/fetch_video_comments
**Summary**: 获取单个视频评论数据/Get single video comments data

**Description**:
# [中文]
### 用途:
- 获取单个视频评论数据
### 参数:
- aweme_id: 作品id
- cursor: 游标
- count: 数量
### 返回:
- 评论数据

# [English]
### Purpose:
- Get single video comments data
### Parameters:
- aweme_id: Video id
- cursor: Cursor
- count: Number
### Return:
- Comments data

# [示例/Example]
aweme_id = "7372484719365098803"
cursor = 0
count = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| aweme_id | string | 是 | 作品id/Video id |
| cursor | integer | 否 | 游标/Cursor |
| count | integer | 否 | 数量/Number |


### GET /api/douyin/web/fetch_video_comment_replies
**Summary**: 获取指定视频的评论回复数据/Get comment replies data of specified video

**Description**:
# [中文]
### 用途:
- 获取指定视频的评论回复数据
### 参数:
- item_id: 作品id
- comment_id: 评论id
- cursor: 游标
- count: 数量
### 返回:
- 评论回复数据

# [English]
### Purpose:
- Get comment replies data of specified video
### Parameters:
- item_id: Video id
- comment_id: Comment id
- cursor: Cursor
- count: Number
### Return:
- Comment replies data

# [示例/Example]
aweme_id = "7354666303006723354"
comment_id = "7354669356632638218"
cursor = 0
count = 20

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| item_id | string | 是 | 作品id/Video id |
| comment_id | string | 是 | 评论id/Comment id |
| cursor | integer | 否 | 游标/Cursor |
| count | integer | 否 | 数量/Number |


### GET /api/douyin/web/generate_real_msToken
**Summary**: 生成真实msToken/Generate real msToken

**Description**:
# [中文]
### 用途:
- 生成真实msToken
### 返回:
- msToken

# [English]
### Purpose:
- Generate real msToken
### Return:
- msToken


### GET /api/douyin/web/generate_ttwid
**Summary**: 生成ttwid/Generate ttwid

**Description**:
# [中文]
### 用途:
- 生成ttwid
### 返回:
- ttwid

# [English]
### Purpose:
- Generate ttwid
### Return:
- ttwid


### GET /api/douyin/web/generate_verify_fp
**Summary**: 生成verify_fp/Generate verify_fp

**Description**:
# [中文]
### 用途:
- 生成verify_fp
### 返回:
- verify_fp

# [English]
### Purpose:
- Generate verify_fp
### Return:
- verify_fp


### GET /api/douyin/web/generate_s_v_web_id
**Summary**: 生成s_v_web_id/Generate s_v_web_id

**Description**:
# [中文]
### 用途:
- 生成s_v_web_id
### 返回:
- s_v_web_id

# [English]
### Purpose:
- Generate s_v_web_id
### Return:
- s_v_web_id


### GET /api/douyin/web/generate_x_bogus
**Summary**: 使用接口网址生成X-Bogus参数/Generate X-Bogus parameter using API URL

**Description**:
# [中文]
### 用途:
- 使用接口网址生成X-Bogus参数
### 参数:
- url: 接口网址

# [English]
### Purpose:
- Generate X-Bogus parameter using API URL
### Parameters:
- url: API URL

# [示例/Example]
url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=7148736076176215311&device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=117.0.2045.47&browser_online=true&engine_name=Blink&engine_version=117.0.0.0&os_name=Windows&os_version=10&cpu_core_num=128&device_memory=10240&platform=PC&downlink=10&effective_type=4g&round_trip_time=100"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |
| user_agent | string | 是 | N/A |


### GET /api/douyin/web/generate_a_bogus
**Summary**: 使用接口网址生成A-Bogus参数/Generate A-Bogus parameter using API URL

**Description**:
# [中文]
### 用途:
- 使用接口网址生成A-Bogus参数
### 参数:
- url: 接口网址
- user_agent: 用户代理，暂时不支持自定义，直接使用默认值即可。

# [English]
### Purpose:
- Generate A-Bogus parameter using API URL
### Parameters:
- url: API URL
- user_agent: User agent, temporarily does not support customization, just use the default value.

# [示例/Example]
url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_online=true&engine_name=Gecko&os_name=Windows&os_version=10&platform=PC&screen_width=1920&screen_height=1080&browser_version=124.0&engine_version=122.0.0.0&cpu_core_num=12&device_memory=8&aweme_id=7372484719365098803"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |
| user_agent | string | 是 | N/A |


### GET /api/douyin/web/get_sec_user_id
**Summary**: 提取单个用户id/Extract single user id

**Description**:
# [中文]
### 用途:
- 提取单个用户id
### 参数:
- url: 用户主页链接
### 返回:
- 用户sec_user_id

# [English]
### Purpose:
- Extract single user id
### Parameters:
- url: User homepage link
### Return:
- User sec_user_id

# [示例/Example]
url = "https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |


### POST /api/douyin/web/get_all_sec_user_id
**Summary**: 提取列表用户id/Extract list user id

**Description**:
# [中文]
 ### 用途:
 - 提取列表用户id
 ### 参数:
 - url: 用户主页链接列表
 ### 返回:
 - 用户sec_user_id列表

 # [English]
 ### Purpose:
 - Extract list user id
 ### Parameters:
 - url: User homepage link list
 ### Return:
 - User sec_user_id list

 # [示例/Example]
 ```json
 {
"urls":[
   "https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE?vid=7285950278132616463",
   "https://www.douyin.com/user/MS4wLjABAAAAVsneOf144eGDFf8Xp9QNb1VW6ovXnNT5SqJBhJfe8KQBKWKDTWK5Hh-_i9mJzb8C",
   "长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/idFqvUms/",
   "https://v.douyin.com/idFqvUms/"
    ]
 }
 ```


### GET /api/douyin/web/get_aweme_id
**Summary**: 提取单个作品id/Extract single video id

**Description**:
# [中文]
### 用途:
- 提取单个作品id
### 参数:
- url: 作品链接
### 返回:
- 作品id

# [English]
### Purpose:
- Extract single video id
### Parameters:
- url: Video link
### Return:
- Video id

# [示例/Example]
url = "https://www.douyin.com/video/7298145681699622182"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |


### POST /api/douyin/web/get_all_aweme_id
**Summary**: 提取列表作品id/Extract list video id

**Description**:
# [中文]
 ### 用途:
 - 提取列表作品id
 ### 参数:
 - url: 作品链接列表
 ### 返回:
 - 作品id列表

 # [English]
 ### Purpose:
 - Extract list video id
 ### Parameters:
 - url: Video link list
 ### Return:
 - Video id list

 # [示例/Example]
 ```json
 {
"urls":[
    "0.53 02/26 I@v.sE Fus:/ 你别太帅了郑润泽# 现场版live # 音乐节 # 郑润泽  https://v.douyin.com/iRNBho6u/ 复制此链接，打开Dou音搜索，直接观看视频!",
    "https://v.douyin.com/iRNBho6u/",
    "https://www.iesdouyin.com/share/video/7298145681699622182/?region=CN&mid=7298145762238565171&u_code=l1j9bkbd&did=MS4wLjABAAAAtqpCx0hpOERbdSzQdjRZw-wFPxaqdbAzsKDmbJMUI3KWlMGQHC-n6dXAqa-dM2EP&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title&share_sign=05kGlqGmR4_IwCX.ZGk6xuL0osNA..5ur7b0jbOx6cc-&share_version=170400&ts=1699262937&from_aid=6383&from_ssr=1&from=web_code_link",
    "https://www.douyin.com/video/7298145681699622182?previous_page=web_code_link",
    "https://www.douyin.com/video/7298145681699622182",
 ]
 }
 ```


### GET /api/douyin/web/get_webcast_id
**Summary**: 提取列表直播间号/Extract list webcast id

**Description**:
# [中文]
### 用途:
- 提取列表直播间号
### 参数:
- url: 直播间链接
### 返回:
- 直播间号

# [English]
### Purpose:
- Extract list webcast id
### Parameters:
- url: Room link
### Return:
- Room id

# [示例/Example]
url = "https://live.douyin.com/775841227732"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |


### POST /api/douyin/web/get_all_webcast_id
**Summary**: 提取列表直播间号/Extract list webcast id

**Description**:
# [中文]
### 用途:
- 提取列表直播间号
### 参数:
- url: 直播间链接列表
### 返回:
- 直播间号列表

# [English]
### Purpose:
- Extract list webcast id
### Parameters:
- url: Room link list
### Return:
- Room id list

# [示例/Example]
```json
{
  "urls": [
        "https://live.douyin.com/775841227732",
        "https://live.douyin.com/775841227732?room_id=7318296342189919011&enter_from_merge=web_share_link&enter_method=web_share_link&previous_page=app_code_link",
        'https://webcast.amemv.com/douyin/webcast/reflow/7318296342189919011?u_code=l1j9bkbd&did=MS4wLjABAAAAEs86TBQPNwAo-RGrcxWyCdwKhI66AK3Pqf3ieo6HaxI&iid=MS4wLjABAAAA0ptpM-zzoliLEeyvWOCUt-_dQza4uSjlIvbtIazXnCY&with_sec_did=1&use_link_command=1&ecom_share_track_params=&extra_params={"from_request_id":"20231230162057EC005772A8EAA0199906","im_channel_invite_id":"0"}&user_id=3644207898042206&liveId=7318296342189919011&from=share&style=share&enter_method=click_share&roomId=7318296342189919011&activity_info={}',
        "6i- Q@x.Sl 03/23 【醒子8ke的直播间】  点击打开👉https://v.douyin.com/i8tBR7hX/  或长按复制此条消息，打开抖音，看TA直播",
        "https://v.douyin.com/i8tBR7hX/",
        ]
}
```


## Download

### GET /api/download
**Summary**: 在线下载抖音|TikTok|Bilibili视频/图片/Online download Douyin|TikTok|Bilibili video/image

**Description**:
# [中文]
### 用途:
- 在线下载抖音|TikTok|Bilibili 无水印或有水印的视频/图片
- 通过传入的视频URL参数，获取对应的视频或图片数据，然后下载到本地。
- 如果你在尝试直接访问TikTok单一视频接口的JSON数据中的视频播放地址时遇到HTTP403错误，那么你可以使用此接口来下载视频。
- Bilibili视频会自动合并视频流和音频流，确保下载的视频有声音。
- 这个接口会占用一定的服务器资源，所以在Demo站点是默认关闭的，你可以在本地部署后调用此接口。
### 参数:
- url: 视频或图片的URL地址，支持抖音|TikTok|Bilibili的分享链接，例如：https://v.douyin.com/e4J8Q7A/ 或 https://www.bilibili.com/video/BV1xxxxxxxxx
- prefix: 下载文件的前缀，默认为True，可以在配置文件中修改。
- with_watermark: 是否下载带水印的视频或图片，默认为False。(注意：Bilibili没有水印概念)
### 返回:
- 返回下载的视频或图片文件响应。

# [English]
### Purpose:
- Download Douyin|TikTok|Bilibili video/image with or without watermark online.
- By passing the video URL parameter, get the corresponding video or image data, and then download it to the local.
- If you encounter an HTTP403 error when trying to access the video playback address in the JSON data of the TikTok single video interface directly, you can use this interface to download the video.
- Bilibili videos will automatically merge video and audio streams to ensure downloaded videos have sound.
- This interface will occupy a certain amount of server resources, so it is disabled by default on the Demo site, you can call this interface after deploying it locally.
### Parameters:
- url: The URL address of the video or image, supports Douyin|TikTok|Bilibili sharing links, for example: https://v.douyin.com/e4J8Q7A/ or https://www.bilibili.com/video/BV1xxxxxxxxx
- prefix: The prefix of the downloaded file, the default is True, and can be modified in the configuration file.
- with_watermark: Whether to download videos or images with watermarks, the default is False. (Note: Bilibili has no watermark concept)
### Returns:
- Return the response of the downloaded video or image file.

# [示例/Example]
url: https://www.bilibili.com/video/BV1U5efz2Egn

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 视频或图片的URL地址，支持抖音|TikTok|Bilibili的分享链接，例如：https://v.douyin.com/e4J8Q7A/ 或 https://www.bilibili.com/video/BV1xxxxxxxxx |
| prefix | boolean | 否 | N/A |
| with_watermark | boolean | 否 | N/A |


## Hybrid-API

### GET /api/hybrid/video_data
**Summary**: 混合解析单一视频接口/Hybrid parsing single video endpoint

**Description**:
# [中文]
### 用途:
- 该接口用于解析抖音/TikTok单一视频的数据。
### 参数:
- `url`: 视频链接、分享链接、分享文本。
### 返回:
- `data`: 视频数据。

# [English]
### Purpose:
- This endpoint is used to parse data of a single Douyin/TikTok video.
### Parameters:
- `url`: Video link, share link, or share text.
### Returns:
- `data`: Video data.

# [Example]
url = "https://v.douyin.com/L4FJNR3/"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |
| minimal | boolean | 否 | N/A |


### GET /api/hybrid/video_data
**Summary**: 混合解析单一视频接口/Hybrid parsing single video endpoint

**Description**:
# [中文]
### 用途:
- 该接口用于解析抖音/TikTok单一视频的数据。
### 参数:
- `url`: 视频链接、分享链接、分享文本。
### 返回:
- `data`: 视频数据。

# [English]
### Purpose:
- This endpoint is used to parse data of a single Douyin/TikTok video.
### Parameters:
- `url`: Video link, share link, or share text.
### Returns:
- `data`: Video data.

# [Example]
url = "https://v.douyin.com/L4FJNR3/"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | N/A |
| minimal | boolean | 否 | N/A |


### POST /api/hybrid/update_cookie
**Summary**: 更新Cookie/Update Cookie

**Description**:
# [中文]
### 用途:
- 更新指定服务的Cookie
### 参数:
- service: 服务名称 (如: douyin_web)
- cookie: 新的Cookie值
### 返回:
- 更新结果

# [English]
### Purpose:
- Update Cookie for specified service
### Parameters:
- service: Service name (e.g.: douyin_web)
- cookie: New Cookie value
### Return:
- Update result

# [示例/Example]
service = "douyin_web"
cookie = "YOUR_NEW_COOKIE"


## TikTok-Web-API

### GET /api/tiktok/web/fetch_one_video
**Summary**: 获取单个作品数据/Get single video data

**Description**:
# [中文]
### 用途:
- 获取单个作品数据
### 参数:
- itemId: 作品id
### 返回:
- 作品数据

# [English]
### Purpose:
- Get single video data
### Parameters:
- itemId: Video id
### Return:
- Video data

# [示例/Example]
itemId = "7339393672959757570"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| itemId | string | 是 | 作品id/Video id |


### GET /api/tiktok/web/fetch_user_profile
**Summary**: 获取用户的个人信息/Get user profile

**Description**:
# [中文]
### 用途:
- 获取用户的个人信息
### 参数:
- secUid: 用户secUid
- uniqueId: 用户uniqueId
- secUid和uniqueId至少提供一个, 优先使用uniqueId, 也就是用户主页的链接中的用户名。
### 返回:
- 用户的个人信息

# [English]
### Purpose:
- Get user profile
### Parameters:
- secUid: User secUid
- uniqueId: User uniqueId
- At least one of secUid and uniqueId is provided, and uniqueId is preferred, that is, the username in the user's homepage link.
### Return:
- User profile

# [示例/Example]
secUid = "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM"
uniqueId = "tiktok"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| uniqueId | string | 否 | 用户uniqueId/User uniqueId |
| secUid | string | 否 | 用户secUid/User secUid |


### GET /api/tiktok/web/fetch_user_post
**Summary**: 获取用户的作品列表/Get user posts

**Description**:
# [中文]
### 用途:
- 获取用户的作品列表
### 参数:
- secUid: 用户secUid
- cursor: 翻页游标
- count: 每页数量
- coverFormat: 封面格式
### 返回:
- 用户的作品列表

# [English]
### Purpose:
- Get user posts
### Parameters:
- secUid: User secUid
- cursor: Page cursor
- count: Number per page
- coverFormat: Cover format
### Return:
- User posts

# [示例/Example]
secUid = "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM"
cursor = 0
count = 35
coverFormat = 2

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| secUid | string | 是 | 用户secUid/User secUid |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |
| coverFormat | integer | 否 | 封面格式/Cover format |


### GET /api/tiktok/web/fetch_user_like
**Summary**: 获取用户的点赞列表/Get user likes

**Description**:
# [中文]
### 用途:
- 获取用户的点赞列表
- 注意: 该接口需要用户点赞列表为公开状态
### 参数:
- secUid: 用户secUid
- cursor: 翻页游标
- count: 每页数量
- coverFormat: 封面格式
### 返回:
- 用户的点赞列表

# [English]
### Purpose:
- Get user likes
- Note: This interface requires that the user's like list be public
### Parameters:
- secUid: User secUid
- cursor: Page cursor
- count: Number per page
- coverFormat: Cover format
### Return:
- User likes

# [示例/Example]
secUid = "MS4wLjABAAAAq1iRXNduFZpY301UkVpJ1eQT60_NiWS9QQSeNqmNQEDJp0pOF8cpleNEdiJx5_IU"
cursor = 0
count = 35
coverFormat = 2

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| secUid | string | 是 | 用户secUid/User secUid |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |
| coverFormat | integer | 否 | 封面格式/Cover format |


### GET /api/tiktok/web/fetch_user_collect
**Summary**: 获取用户的收藏列表/Get user favorites

**Description**:
# [中文]
### 用途:
- 获取用户的收藏列表
- 注意: 该接口目前只能获取自己的收藏列表，需要提供自己账号的cookie。
### 参数:
- cookie: 用户cookie
- secUid: 用户secUid
- cursor: 翻页游标
- count: 每页数量
- coverFormat: 封面格式
### 返回:
- 用户的收藏列表

# [English]
### Purpose:
- Get user favorites
- Note: This interface can currently only get your own favorites list, you need to provide your account cookie.
### Parameters:
- cookie: User cookie
- secUid: User secUid
- cursor: Page cursor
- count: Number per page
- coverFormat: Cover format
### Return:
- User favorites

# [示例/Example]
cookie = "Your_Cookie"
secUid = "Your_SecUid"
cursor = 0
count = 30
coverFormat = 2

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| cookie | string | 是 | 用户cookie/User cookie |
| secUid | string | 是 | 用户secUid/User secUid |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |
| coverFormat | integer | 否 | 封面格式/Cover format |


### GET /api/tiktok/web/fetch_user_play_list
**Summary**: 获取用户的播放列表/Get user play list

**Description**:
# [中文]
### 用途:
- 获取用户的播放列表
### 参数:
- secUid: 用户secUid
- cursor: 翻页游标
- count: 每页数量
### 返回:
- 用户的播放列表

# [English]
### Purpose:
- Get user play list
### Parameters:
- secUid: User secUid
- cursor: Page cursor
- count: Number per page
### Return:
- User play list

# [示例/Eample]
secUid = "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM"
cursor = 0
count = 30

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| secUid | string | 是 | 用户secUid/User secUid |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |


### GET /api/tiktok/web/fetch_user_mix
**Summary**: 获取用户的合辑列表/Get user mix list

**Description**:
# [中文]
### 用途:
- 获取用户的合辑列表
### 参数:
- mixId: 合辑id
- cursor: 翻页游标
- count: 每页数量
### 返回:
- 用户的合辑列表

# [English]
### Purpose:
- Get user mix list
### Parameters:
- mixId: Mix id
- cursor: Page cursor
- count: Number per page
### Return:
- User mix list

# [示例/Eample]
mixId = "7101538765474106158"
cursor = 0
count = 30

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| mixId | string | 是 | 合辑id/Mix id |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |


### GET /api/tiktok/web/fetch_post_comment
**Summary**: 获取作品的评论列表/Get video comments

**Description**:
# [中文]
### 用途:
- 获取作品的评论列表
### 参数:
- aweme_id: 作品id
- cursor: 翻页游标
- count: 每页数量
- current_region: 当前地区，默认为空。
### 返回:
- 作品的评论列表

# [English]
### Purpose:
- Get video comments
### Parameters:
- aweme_id: Video id
- cursor: Page cursor
- count: Number per page
- current_region: Current region, default is empty.
### Return:
- Video comments

# [示例/Eample]
aweme_id = "7304809083817774382"
cursor = 0
count = 20
current_region = ""

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| aweme_id | string | 是 | 作品id/Video id |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |
| current_region | string | 否 | 当前地区/Current region |


### GET /api/tiktok/web/fetch_post_comment_reply
**Summary**: 获取作品的评论回复列表/Get video comment replies

**Description**:
# [中文]
### 用途:
- 获取作品的评论回复列表
### 参数:
- item_id: 作品id
- comment_id: 评论id
- cursor: 翻页游标
- count: 每页数量
- current_region: 当前地区，默认为空。
### 返回:
- 作品的评论回复列表

# [English]
### Purpose:
- Get video comment replies
### Parameters:
- item_id: Video id
- comment_id: Comment id
- cursor: Page cursor
- count: Number per page
- current_region: Current region, default is empty.
### Return:
- Video comment replies

# [示例/Eample]
item_id = "7304809083817774382"
comment_id = "7304877760886588191"
cursor = 0
count = 20
current_region = ""

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| item_id | string | 是 | 作品id/Video id |
| comment_id | string | 是 | 评论id/Comment id |
| cursor | integer | 否 | 翻页游标/Page cursor |
| count | integer | 否 | 每页数量/Number per page |
| current_region | string | 否 | 当前地区/Current region |


### GET /api/tiktok/web/fetch_user_fans
**Summary**: 获取用户的粉丝列表/Get user followers

**Description**:
# [中文]
### 用途:
- 获取用户的粉丝列表
### 参数:
- secUid: 用户secUid
- count: 每页数量
- maxCursor: 最大游标
- minCursor: 最小游标
### 返回:
- 用户的粉丝列表

# [English]
### Purpose:
- Get user followers
### Parameters:
- secUid: User secUid
- count: Number per page
- maxCursor: Max cursor
- minCursor: Min cursor
### Return:
- User followers

# [示例/Example]
secUid = "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM"
count = 30
maxCursor = 0
minCursor = 0

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| secUid | string | 是 | 用户secUid/User secUid |
| count | integer | 否 | 每页数量/Number per page |
| maxCursor | integer | 否 | 最大游标/Max cursor |
| minCursor | integer | 否 | 最小游标/Min cursor |


### GET /api/tiktok/web/fetch_user_follow
**Summary**: 获取用户的关注列表/Get user followings

**Description**:
# [中文]
### 用途:
- 获取用户的关注列表
### 参数:
- secUid: 用户secUid
- count: 每页数量
- maxCursor: 最大游标
- minCursor: 最小游标
### 返回:
- 用户的关注列表

# [English]
### Purpose:
- Get user followings
### Parameters:
- secUid: User secUid
- count: Number per page
- maxCursor: Max cursor
- minCursor: Min cursor
### Return:
- User followings

# [示例/Example]
secUid = "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM"
count = 30
maxCursor = 0
minCursor = 0

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| secUid | string | 是 | 用户secUid/User secUid |
| count | integer | 否 | 每页数量/Number per page |
| maxCursor | integer | 否 | 最大游标/Max cursor |
| minCursor | integer | 否 | 最小游标/Min cursor |


### GET /api/tiktok/web/generate_real_msToken
**Summary**: 生成真实msToken/Generate real msToken

**Description**:
# [中文]
### 用途:
- 生成真实msToken
### 返回:
- 真实msToken

# [English]
### Purpose:
- Generate real msToken
### Return:
- Real msToken


### GET /api/tiktok/web/generate_ttwid
**Summary**: 生成ttwid/Generate ttwid

**Description**:
# [中文]
### 用途:
- 生成ttwid
### 参数:
- cookie: 用户cookie
### 返回:
- ttwid

# [English]
### Purpose:
- Generate ttwid
### Parameters:
- cookie: User cookie
### Return:
- ttwid

# [示例/Example]
cookie = "Your_Cookie"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| cookie | string | 是 | 用户cookie/User cookie |


### GET /api/tiktok/web/generate_xbogus
**Summary**: 生成xbogus/Generate xbogus

**Description**:
# [中文]
### 用途:
- 生成xbogus
### 参数:
- url: 未签名的API URL
- user_agent: 用户浏览器User-Agent
### 返回:
- xbogus

# [English]
### Purpose:
- Generate xbogus
### Parameters:
- url: Unsigned API URL
- user_agent: User browser User-Agent
### Return:
- xbogus

# [示例/Example]
url = "https://www.tiktok.com/api/item/detail/?WebIdLastTime=1712665533&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%29&channel=tiktok_web&cookie_enabled=true&device_id=7349090360347690538&device_platform=web_pc&focus_state=true&from_page=user&history_len=4&is_fullscreen=false&is_page_visible=true&language=en&os=windows&priority_region=US&referer=&region=US&root_referer=https%3A%2F%2Fwww.tiktok.com%2F&screen_height=1080&screen_width=1920&webcast_language=en&tz_name=America%2FTijuana&msToken=AYFCEapCLbMrS8uTLBoYdUMeeVLbCdFQ_QF_-OcjzJw1CPr4JQhWUtagy0k4a9IITAqi5Qxr2Vdh9mgCbyGxTnvWLa4ZVY6IiSf6lcST-tr0IXfl-r_ZTpzvWDoQfqOVsWCTlSNkhAwB-tap5g==&itemId=7339393672959757570"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 未签名的API URL/Unsigned API URL |
| user_agent | string | 是 | 用户浏览器User-Agent/User browser User-Agent |


### GET /api/tiktok/web/get_sec_user_id
**Summary**: 提取列表用户id/Extract list user id

**Description**:
# [中文]
### 用途:
- 提取列表用户id
### 参数:
- url: 用户主页链接
### 返回:
- 用户id

# [English]
### Purpose:
- Extract list user id
### Parameters:
- url: User homepage link
### Return:
- User id

# [示例/Example]
url = "https://www.tiktok.com/@tiktok"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 用户主页链接/User homepage link |


### POST /api/tiktok/web/get_all_sec_user_id
**Summary**: 提取列表用户id/Extract list user id

**Description**:
# [中文]
### 用途:
- 提取列表用户id
### 参数:
- url: 用户主页链接
### 返回:
- 用户id

# [English]
### Purpose:
- Extract list user id
### Parameters:
- url: User homepage link
### Return:
- User id

# [示例/Example]
url = ["https://www.tiktok.com/@tiktok"]


### GET /api/tiktok/web/get_aweme_id
**Summary**: 提取单个作品id/Extract single video id

**Description**:
# [中文]
### 用途:
- 提取单个作品id
### 参数:
- url: 作品链接
### 返回:
- 作品id

# [English]
### Purpose:
- Extract single video id
### Parameters:
- url: Video link
### Return:
- Video id

# [示例/Example]
url = "https://www.tiktok.com/@owlcitymusic/video/7218694761253735723"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 作品链接/Video link |


### POST /api/tiktok/web/get_all_aweme_id
**Summary**: 提取列表作品id/Extract list video id

**Description**:
# [中文]
### 用途:
- 提取列表作品id
### 参数:
- url: 作品链接
### 返回:
- 作品id

# [English]
### Purpose:
- Extract list video id
### Parameters:
- url: Video link
### Return:
- Video id

# [示例/Example]
url = ["https://www.tiktok.com/@owlcitymusic/video/7218694761253735723"]


### GET /api/tiktok/web/get_unique_id
**Summary**: 获取用户unique_id/Get user unique_id

**Description**:
# [中文]
### 用途:
- 获取用户unique_id
### 参数:
- url: 用户主页链接
### 返回:
- unique_id

# [English]
### Purpose:
- Get user unique_id
### Parameters:
- url: User homepage link
### Return:
- unique_id

# [示例/Example]
url = "https://www.tiktok.com/@tiktok"

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 用户主页链接/User homepage link |


### POST /api/tiktok/web/get_all_unique_id
**Summary**: 获取列表unique_id/Get list unique_id

**Description**:
# [中文]
### 用途:
- 获取列表unique_id
### 参数:
- url: 用户主页链接
### 返回:
- unique_id

# [English]
### Purpose:
- Get list unique_id
### Parameters:
- url: User homepage link
### Return:
- unique_id

# [示例/Example]
url = ["https://www.tiktok.com/@tiktok"]


## iOS-Shortcut

### GET /api/ios/shortcut
**Summary**: 用于iOS快捷指令的版本更新信息/Version update information for iOS shortcuts

