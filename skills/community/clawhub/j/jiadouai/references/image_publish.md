# 图片发布

> 调用方式见 SKILL.md「调用方式」
> 发布结果通过 `video_publish_status` 查询（非 `get_job_status`），见 [workflows.md](workflows.md#video_publish_status)

## 参数

```json
{
  "images": ["https://cdn.example.com/photo1.jpg"],  // 必填：图片URL数组，公网可访问
  "account_id": "<来自 account_page 的 _id>",          // 必填：发布账号ID，先调 account_page 获取
  "title": "我的图文内容",                              // 必填：发布内容标题
  "time": ""                                           // 可选，默认 null：定时发布时间，格式 "2026-05-11 11:00"，为空立即发布
}
```

## 关键约束

- ⚠️ 发布前**必须先调 `account_page`**（传 `{}`）获取已授权账号的 `_id`
- `images` 是数组，不是单数 `url`
- 查询发布结果的工具叫 `video_publish_status`（名称暗示视频，但图文发布也用它）
