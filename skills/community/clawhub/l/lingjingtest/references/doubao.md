# 豆包 (Doubao / Seed 系列) API 参考

> 品牌方：字节跳动 | 平台：京东云 JoyCreator

---

## apiId 速查表

| 任务类型 | 模型版本 | apiId | model 字段名 | model 值 |
|---------|---------|-------|-------------|---------|
| 文生图 | Seedream 4.0 | `700` | `model` | `doubao-seedream-4-0-250828` |
| 文生图 | Seedream 4.5 | `701` | `model` | `doubao-seedream-4-5-251128` |
| 文生视频 | Seedance 1.5 Pro | `750` | `model_name` | `Doubao-Seedance-1.5-pro` |
| 图生视频 | Seedance 1.5 Pro | `751` | `model_name` | `Doubao-Seedance-1.5-pro` |

> ⚠️ 注意：图像生成用 `model`，视频生成用 `model_name`，字段名不同。

---

## 文生图 (apiId: 700 / 701)

### 参数说明

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | 见上表 |
| `prompt` | string | ✅ | 图片描述词 |
| `size` | string | ✅ | 见下方尺寸列表 |
| `taskNum` | int | ✅ | 生成数量，1-4 |
| `image` | string[] | ❌ | 参考图 URL 数组（图生图/风格参考） |

### 支持的 size 值

```
2048x2048  2304x1728  1728x2304
2560x1440  1440x2560
2496x1664  1664x2496
3024x1296
```

### 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "701",
    "params": {
      "model": "doubao-seedream-4-5-251128",
      "prompt": "一只在樱花树下打盹的橘猫，写实摄影风格，柔和自然光",
      "size": "2048x2048",
      "taskNum": 1
    }
  }'
```

---

## 文生视频 (apiId: 750)

### 参数说明

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_name` | string | ✅ | `Doubao-Seedance-1.5-pro` |
| `prompt` | string | ✅ | 视频内容描述词 |
| `duration` | string | ✅ | `"5"` / `"10"` / `"12"` |
| `mode` | string | ✅ | `"480p"` / `"720p"` / `"1080p"` |
| `aspect_ratio` | string | ✅ | `"16:9"` / `"9:16"` / `"4:3"` / `"1:1"` / `"4:4"` / `"21:9"` |
| `generate_audio` | boolean | ❌ | 是否同步生成音频，默认 `false` |

### 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "750",
    "params": {
      "model_name": "Doubao-Seedance-1.5-pro",
      "prompt": "夕阳下海浪轻拍沙滩，泡沫慢慢消散，镜头缓缓拉远",
      "duration": "10",
      "mode": "1080p",
      "aspect_ratio": "16:9",
      "generate_audio": true
    }
  }'
```

---

## 图生视频 (apiId: 751)

在文生视频参数基础上，**增加必填字段**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `image_urls` | string[] | ✅ | 参考图片 URL 数组，必须公网可访问 |

### 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "751",
    "params": {
      "model_name": "Doubao-Seedance-1.5-pro",
      "image_urls": ["https://example.com/cat.jpg"],
      "prompt": "猫咪伸懒腰，慢慢睁开眼睛",
      "duration": "5",
      "mode": "720p",
      "aspect_ratio": "16:9",
      "generate_audio": false
    }
  }'
```
