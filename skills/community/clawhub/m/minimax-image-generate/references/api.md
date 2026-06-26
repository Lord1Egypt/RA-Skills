# MiniMax 图片 API 参考

## 基础配置

- **国内用户**: `https://api.minimaxi.com/v1`
- **国际用户**: `https://api.minimax.io/v1`
- **认证方式**: `Authorization: Bearer $MINIMAX_API_KEY`

## API 端点

### 1. 文生图 (Text to Image)

```
POST /v1/image_generation
```

**请求体**:
```json
{
  "model": "image-01",
  "prompt": "图片描述文本",
  "aspect_ratio": "1:1",
  "response_format": "url"
}
```

**aspect_ratio 可选值**:
- `1:1` - 正方形
- `16:9` - 宽屏
- `9:16` - 竖屏
- `4:3` - 标准
- `3:4` - 竖版标准

**response_format 可选值**:
- `url` - 返回图片URL
- `base64` - 返回base64编码图片

**响应**:
```json
{
  "id": "图片ID",
  "data": {
    "image_urls": ["图片URL1", "图片URL2"]
  },
  "metadata": {
    "failed_count": "0",
    "success_count": "1"
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 2. 图生图 (Image to Image)

```
POST /v1/image_generation
```

使用参考图时，在请求体中添加 `image_url` 字段:

**请求体**:
```json
{
  "model": "image-01",
  "prompt": "图片修改描述",
  "aspect_ratio": "1:1",
  "response_format": "url",
  "image_url": "参考图URL"
}
```

## 图片模型

- `image-01` - 最新一代图片生成模型，支持文生图和图生图

## 返回格式说明

当 `response_format` 为 `url` 时，返回的图片URL有效期为1小时。

当 `response_format` 为 `base64` 时，直接返回图片数据，可直接保存为文件。
