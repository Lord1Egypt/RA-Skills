# MiniMax Image Generation API

## Overview

MiniMax 提供两个图像生成API：
- **文生图 (T2I)**: 根据文字描述生成图片
- **图生图 (I2I)**: 基于参考图片生成新图

Base URL: `https://api.minimaxi.com/v1/image_generation`

认证: `Authorization: Bearer {API_KEY}`

---

## Common Parameters

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | `image-01` 或 `image-01-live` |
| `prompt` | string | 图片描述，最长1500字符 |
| `aspect_ratio` | string | 宽高比，默认 `1:1` |
| `response_format` | string | `url`（默认）或 `base64` |
| `n` | int | 生成数量，1-9，默认1 |
| `prompt_optimizer` | bool | 是否开启prompt自动优化，默认false |
| `aigc_watermark` | bool | 是否添加水印，默认false |

### Aspect Ratio Options

| 值 | 尺寸 |
|---|------|
| `1:1` | 1024x1024 |
| `16:9` | 1280x720 |
| `4:3` | 1152x864 |
| `3:2` | 1248x832 |
| `2:3` | 832x1248 |
| `3:4` | 864x1152 |
| `9:16` | 720x1280 |
| `21:9` | 1344x576 (仅image-01) |

### Model Differences

**image-01**
- 支持所有宽高比
- 支持自定义 width/height [512, 2048]

**image-01-live**
- 支持画风风格（style参数）
- 可选风格：`漫画`、`元气`、`中世纪`、`水彩`

---

## T2I Request Example

```json
{
  "model": "image-01",
  "prompt": "A man in a white t-shirt, full-body, standing front view, outdoors, Venice Beach sign in background",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 3,
  "prompt_optimizer": true
}
```

## T2I Response

```json
{
  "data": {
    "image_urls": ["https://xxx.bj.bcebos.com/xxx.jpg"]
  },
  "metadata": {
    "success_count": 3,
    "failed_count": 0
  },
  "id": "03ff3cd0820949eb8a410056b5f21d38",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

> ⚠️ URL有效期24小时

---

## I2I Request Example

图生图需要在请求中添加 `subject_reference` 参数：

```json
{
  "model": "image-01",
  "prompt": "穿着中国传统服装，站在长城上",
  "aspect_ratio": "3:4",
  "subject_reference": [
    {
      "type": "character",
      "image_file": "https://example.com/reference.jpg"
    }
  ],
  "n": 2
}
```

### subject_reference

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 当前仅支持 `character` |
| `image_file` | string | 参考图URL或Base64 Data URL |

**图片要求：**
- 格式：JPG, JPEG, PNG
- 大小：小于10MB
- 建议：上传单人正面照片效果最佳

---

## Style for image-01-live

当 model 为 `image-01-live` 时，可添加 style 参数：

```json
{
  "model": "image-01-live",
  "prompt": "在海边度假",
  "style": {
    "style_type": "水彩",
    "style_weight": 0.8
  }
}
```

| style_type | 说明 |
|------------|------|
| `漫画` | Comic/ Manga style |
| `元气` | Energetic/ Youthful |
| `中世纪` | Medieval style |
| `水彩` | Watercolor |

style_weight 范围 (0, 1]，默认 0.8

---

## Error Codes

| status_code | 说明 |
|-------------|------|
| 0 | 成功 |
| 1002 | 触发限流 |
| 1004 | 账号鉴权失败 |
| 1008 | 余额不足 |
| 1026 | 内容涉及敏感 |
| 2013 | 参数异常 |
| 2049 | 无效API Key |

---

## Script Usage

```bash
# 文生图
python3 image_gen.py -p "一只猫在草地上玩耍" -r "16:9" -n 2

# 图生图（通过Python调用）
from image_gen import generate_image

result = generate_image(
    prompt="穿着西装，站在办公室里",
    model="image-01",
    aspect_ratio="3:4",
    subject_reference=[
        {
            "type": "character",
            "image_file": "https://example.com/photo.jpg"
        }
    ],
    n=1
)

# 输出结果包含本地保存路径
print(result["_local_paths"])
```

---

## Note on URLs

图片URL有效期为24小时，需要及时下载保存。

脚本会自动下载url格式的图片到 `/home/ubuntu/.openclaw/workspace/images/` 目录。
