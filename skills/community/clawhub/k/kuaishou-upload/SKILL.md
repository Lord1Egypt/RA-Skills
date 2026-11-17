---
name: kuaishou-upload
description: 使用 EasyPost 自动填充或发布快手创作者服务平台的短视频或图文。Use when 用户需要向快手发布视频或图集。
license: MIT-0
slug: easypost-kuaishou-upload
displayName: 快手自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 浏览器会话的快手短视频与图文零风控自动发布。
---

# 快手自动填充与发布 Skill

通过 EasyPost 驱动当前已登录的快手创作者服务平台（`cp.kuaishou.com`）执行自动上传与填充。

## 平台规格限制与最佳实践

- **内容形态**：
  - `shortVideo`：短视频；
  - `imageText`：快手图集。
- **字段规范**：
  - **文案**：作品描述建议 300 字以内，可带 `#话题` 标签；
  - **下载权限**：支持 `data.allowDownload: true/false`；
  - **封面**：竖版 9:16（`role: "cover"`）。

---

## 示例
```bash
printf '%s\n' '{
  "type": "shortVideo",
  "platforms": ["kuaishou"],
  "data": {
    "title": "今日技能分享",
    "content": "一分钟掌握这个实用工具，效率翻倍！#实用技能 #生活小窍门"
  },
  "assets": [
    {
      "path": "/absolute/path/to/video.mp4",
      "role": "media"
    }
  ]
}' | easypost fill
```
