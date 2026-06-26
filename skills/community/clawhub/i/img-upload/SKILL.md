---
name: img-upload
description: 将本地图片上传到 img.scdn.io 免费图床并返回公开链接。适用于用户需要把图片变成可分享 URL、上传生成结果、上传截图、上传本地图片供外链引用，或明确要求免费图床、图床、图片外链、分享链接时。若任务中已经有本地图片文件，且下一步需要分享、引用、粘贴到文档、消息或网页中，应优先考虑此技能。
metadata: { "openclaw": { "emoji": "🖼️" } }
---

# img-upload

将本地图片上传到 `img.scdn.io` 图床，并返回可公开访问的图片链接。

## 适用场景

- 用户发送图片后，需要上传并返回分享链接
- 生成图片后，需要得到外链
- 截图、本地图片需要插入文档、网页、消息或工单
- 用户明确提到“图床”“图片外链”“上传图片拿链接”“给我一个可访问 URL”

## 用法

```bash
python skills/img-upload/upload.py <图片路径> [cdn_domain]
```

## 参数

- `图片路径`：本地图片文件路径
- `cdn_domain`：可选，指定 CDN 域名

## 示例

```bash
# 上传单张图片
python skills/img-upload/upload.py /path/to/image.jpg

# 指定 CDN 域名
python skills/img-upload/upload.py /path/to/image.jpg img.scdn.io
```

## 返回

- `url`：图片公开访问链接
- `delete_url`：删除链接（可用于删除图片）

## 注意事项

- 上传前应确认文件存在且是图片
- 返回的 `delete_url` 也属于敏感控制信息，不要随意外发
- 如果用户只是要本地处理图片，而不需要公网链接，不要多余使用此技能
