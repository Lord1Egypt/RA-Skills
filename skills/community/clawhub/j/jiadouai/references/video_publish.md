# 视频发布

> 调用方式见 SKILL.md「调用方式」
> 发布结果通过 `video_publish_status` 查询（非 `get_job_status`），见 [workflows.md](workflows.md#video_publish_status)

## 参数

```json
{
  "url": "https://cdn.example.com/video.mp4",    // 必填：待发布视频，公网URL
  "account_id": "<来自 account_page 的 _id>",     // 必填：发布账号ID，先调 account_page 获取
  "title": "我的视频标题",                         // 必填：发布标题
  "time": ""                                      // 可选，默认 null：定时发布时间，格式 "2026-05-11 11:00"，为空立即发布
}
```

## 关键约束

- ⚠️ 发布前**必须先调 `account_page`**（传 `{}`）获取已授权账号的 `_id`，见 [workflows.md](workflows.md#account_page)
- 支持的平台：抖音、百家号、西瓜、哔哩哔哩、快手、视频号、小红书、TikTok、YouTube、Threads、Facebook
