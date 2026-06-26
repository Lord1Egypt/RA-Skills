---
name: Image Upload to img.scdn.io
description: Upload local image to https://img.scdn.io get public permanent link
---

# Image Upload to img.scdn.io

Upload local image to https://img.scdn.io/ get permanent public URL for sharing. Simple bash script wrapper.

上传本地图片到 `https://img.scdn.io/` 获取永久公开可访问链接，用于公开分享。

## Usage

```bash
openclaw skill run image-upload-imgcdn --image /path/to/image.png
```

输出：返回公开可访问链接。

## API Documentation

- Endpoint: `https://img.scdn.io/api/v1.php`
- Method: `POST`
- Parameter: `image` (multipart/form-data)
- Response: JSON `{"url": "https://img.cdn1.vip/i/xxx.png"}`

## Notes

- 链接永久有效，用于InStreet发帖等公开分享场景

