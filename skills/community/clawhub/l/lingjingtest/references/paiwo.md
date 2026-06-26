# 拍我 (PaiWo) API 参考

> 平台：京东云 JoyCreator

---

## apiId 速查表

| 任务类型 | 模型版本 | apiId | model 值 | 特有能力 |
|---------|---------|-------|---------|---------|
| 文生视频 | V5.5 | `401` | `v5.5` | 同步音频、多段视频 |
| 文生视频 | V5 | `400` | `v5` | 支持 5s/8s |
| 图生视频 | V5.5 | `402` | `v5.5` | 首尾帧控制 |
| 图生视频 | V5（多图） | `501` | `v5` | 首尾帧控制 |
| 图生视频 | V5（单图） | `502` | `v5` | `img_id` 参数（int 类型） |
| 参考图生视频 | V5 | `503` | `v5` | `image_references` 主体一致性 |

> ⚠️ 拍我暂无图像生成接口。

---

## 公共参数（所有接口通用）

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | 见上表 |
| `prompt` | string | ✅ | 视频描述词，建议描述画面动态、光影和细节 |
| `duration` | int/string | ✅ | `5` 或 `8`（秒） |
| `quality` | string | ✅ | `"360p"` / `"540p"` / `"720p"` / `"1080p"` |
| `aspect_ratio` | string | ✅ | `"16:9"` / `"9:16"` / `"1:1"` / `"4:3"` / `"3:4"` |

---

## 文生视频

### V5.5 特有参数

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `generate_audio_switch` | boolean | 是否同步生成环境音/配乐，默认 `false` |
| `generate_multi_clip_switch` | boolean | 是否生成多段视频 |

### V5.5 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "401",
    "params": {
      "model": "v5.5",
      "prompt": "一位舞者在舞台上旋转，聚光灯打在她身上，背景是星空",
      "duration": 5,
      "quality": "1080p",
      "aspect_ratio": "16:9",
      "generate_audio_switch": true,
      "generate_multi_clip_switch": false
    }
  }'
```

### V5 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "400",
    "params": {
      "model": "v5",
      "prompt": "清晨的咖啡馆，蒸汽从咖啡杯中升起，窗外阳光慢慢照进来",
      "duration": 8,
      "quality": "1080p",
      "aspect_ratio": "1:1"
    }
  }'
```

---

## 图生视频

### 特有字段

| 字段名 | 类型 | 适用 apiId | 说明 |
|--------|------|-----------|------|
| `first_frame_img` | string | 402, 501 | 首帧图片公网 URL |
| `last_frame_img` | string | 402, 501 | 尾帧图片公网 URL（可选） |
| `img_id` | int | 502 | 单图接口专用，图片 ID（int 类型，非 URL） |

### V5.5 图生视频示例（首尾帧）

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "402",
    "params": {
      "model": "v5.5",
      "prompt": "人物从远处走近镜头，表情由严肃转为微笑",
      "first_frame_img": "https://example.com/far.jpg",
      "last_frame_img": "https://example.com/close.jpg",
      "duration": 5,
      "quality": "1080p",
      "aspect_ratio": "9:16",
      "generate_audio_switch": false
    }
  }'
```

### V5 单图接口示例 (apiId: 502)

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "502",
    "params": {
      "model": "v5",
      "prompt": "人物转身，头发随之飘动",
      "img_id": 123456,
      "duration": 5,
      "quality": "720p",
      "aspect_ratio": "9:16"
    }
  }'
```

---

## 参考图生视频 (apiId: 503)

使用 `image_references` 对象数组来保持角色/主体一致性：

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "503",
    "params": {
      "model": "v5",
      "prompt": "角色在咖啡馆里翻阅书本，阳光从窗户斜射进来",
      "image_references": [
        {"image_url": "https://example.com/person_ref.jpg"}
      ],
      "duration": 5,
      "quality": "1080p",
      "aspect_ratio": "16:9"
    }
  }'
```
