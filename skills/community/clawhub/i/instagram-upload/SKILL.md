---
name: instagram-upload
description: 使用 EasyPost 自动填充或发布 Instagram 帖子、轮播图集或 Reels 视频。Use when 用户需要向 Instagram 发布图集或短视频。
license: MIT-0
slug: easypost-instagram-upload
displayName: Instagram 自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 会话的 Instagram 图文与 Reels 视频自动发布。
---

# Instagram 自动填充与发布 Skill

通过 EasyPost 驱动当前已登录的 `instagram.com` 执行自动填充与发布。

## 平台规格限制与最佳实践

- **内容形态**：
  - `imageText`：图片帖子或轮播图集（支持 1~10 张图片，推荐 1:1 或 4:5 比例）；
  - `shortVideo`：Reels 视频（推荐 9:16 竖版高清）。
- **字段规范**：
  - **文案**：支持文本描述与 `#hashtag`；
  - **发布模式**：默认 `easypost fill` 自动定位上传按钮并填入内容，留待创作者在网页端确认预览。

---

## 示例
```bash
printf '%s\n' '{
  "type": "imageText",
  "platforms": ["instagram"],
  "data": {
    "title": "Daily Inspiration",
    "content": "Designing with simplicity and speed. #design #creativity #inspiration"
  },
  "assets": [
    {
      "path": "/absolute/path/to/feed.jpg",
      "role": "media"
    }
  ]
}' | easypost fill
```
