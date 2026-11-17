# Douyin API

Base: `https://www.smsz.xyz/prod-api`

The CLI uses `POST` with request/query parameters for Douyin endpoints. Current no-key probes show that several public catalog paths are stale, so default execution must use the confirmed routes below.

## Confirmed executable routes

| Use case | Endpoint | Required params | Key |
| --- | --- | --- | --- |
| 视频基础信息 | `/tool/douyin/Dy_video_info` | `url` | No |
| 视频核心数据 | `/tool/douyin/Dy_video_info_VIP` | `url`, `key` | Yes |
| 视频精简信息 | `/tool/douyin/Dy_video_info_VIP2` | `url`, `key` | Yes |
| 视频全部评论 | `/tool/douyin/Dy_video_all_comments_VIP` | `video_url`, `page`, `key` | Yes |
| 达人资料 | `/tool/douyin/Dy_user_profile_VIP` | `userUrl`, `url`, `key` | Yes |
| 达人作品列表 | `/tool/douyin/Dy_user_post_videos_Vip2` | `userUrl`, `url`, `maxCursor`, `key` | Yes |
| 主页前20条视频及小程序 | `/tool/douyin/Dy_user_video_and_app` | `url` | No |
| 达人综合数据 | `/tool/douyin/Dy_user_videos_info` | `url` | No |
| 粉丝画像 | `/tool/douyin/Dy_fans_portrai_VIP` | `url`, `key` | Yes |
| 话题详情 | `/tool/douyin/Dy_hashtag_detail_VIP` | `ch_id`, `key` | Yes |
| 话题视频列表 | `/tool/douyin/Dy_hashtag_video_list_VIP` | `ch_id`, `maxCursor`, `sortType`, `key` | Yes |

Keep `Dy_fans_portrai_VIP` and `Dy_user_post_videos_Vip2` spelling unchanged.

## Public catalog routes not safe to call by default

These appeared in the public API catalog but returned `404 Not Found` in no-key backend probes on 2026-06-22:

- `/tool/douyin/Dy_convert_share_url`
- `/tool/douyin/Dy_search_video_VIP`
- `/tool/douyin/Dy_video_comments_VIP`
- `/tool/douyin/Dy_video_comments_list_VIP`
- `/tool/douyin/Dy_video_comments_reply_VIP`
- `/tool/douyin/Dy_user_info_VIP`
- `/tool/douyin/Dy_user_video_all_VIP`
- `/tool/douyin/Dy_user_video_page_VIP`

Do not select these paths unless HotBee publishes an updated contract or a fresh probe confirms they are restored.

## Examples

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call douyin --dry-run --text "解析这个视频的播放量和评论 https://v.douyin.com/xxxx/"
```

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call douyin --dry-run --text "分析这个达人主页的作品和粉丝画像 https://www.douyin.com/user/xxxx"
```
