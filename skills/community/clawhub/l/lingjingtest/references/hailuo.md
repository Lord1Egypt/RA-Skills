# 海螺 (Hailuo / MiniMax) API 参考

> 品牌方：MiniMax | 平台：京东云 JoyCreator

---

## apiId 速查表

| 任务类型 | 模型版本 | apiId | model 值 |
|---------|---------|-------|---------|
| 文生图 | image-01 | `456` | `image-01` |
| 文生视频 | Hailuo-02 | `458` | `MiniMax-Hailuo-02` |
| 文生视频 | Hailuo-2.3 | `460` | `MiniMax-Hailuo-2.3` |
| 图生视频 | Hailuo-02 | `457` | `MiniMax-Hailuo-02` |
| 图生视频 | Hailuo-2.3 | `461` | `MiniMax-Hailuo-2.3` |
| 图生视频（快速） | Hailuo-2.3-Fast | `462` | `MiniMax-Hailuo-2.3-Fast` |
| 参考图生视频 | S2V-01 | `459` | `S2V-01` |

---

## 文生图 (apiId: 456)

### 参数说明

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | `image-01` |
| `prompt` | string | ✅ | 图片描述词 |
| `aspect_ratio` | string | ✅ | `"16:9"` / `"9:16"` / `"1:1"` / `"4:3"` / `"3:4"` |
| `subject_reference` | string[] | ❌ | 主体参考图 URL 数组 |

### 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "456",
    "params": {
      "model": "image-01",
      "prompt": "赛博朋克风格的城市夜景，霓虹灯倒影在雨后的街道",
      "aspect_ratio": "16:9"
    }
  }'
```

---

## 视频生成通用参数（文生/图生，apiId: 457-462）

### 时长与分辨率约束 ⚠️

| duration | 允许的 resolution |
|----------|-----------------|
| `6`（秒） | `768P` 或 `1080P` |
| `10`（秒） | 仅 `768P` |

### 参数说明

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | 见 apiId 速查表 |
| `prompt` | string | ✅ | 视频描述词 |
| `duration` | int | ✅ | `6` 或 `10` |
| `resolution` | string | ✅ | `"768P"` 或 `"1080P"` |
| `aspect_ratio` | string | ✅ | `"16:9"` / `"9:16"` / `"1:1"` / `"4:3"` / `"3:4"` |
| `first_frame_image` | string | ❌ | 首帧图片 URL（图生视频时使用） |
| `last_frame_image` | string | ❌ | 尾帧图片 URL（仅 apiId 457 支持） |
| `subject_reference` | string/object | ❌ | 主体参考（仅 apiId 459 S2V-01 使用 object 类型） |

### 文生视频请求示例 (Hailuo-2.3)

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "460",
    "params": {
      "model": "MiniMax-Hailuo-2.3",
      "prompt": "一只白色的猫咪在窗台上望向远处，阳光斜射进来，画面温馨宁静",
      "duration": 6,
      "resolution": "1080P",
      "aspect_ratio": "16:9"
    }
  }'
```

### 图生视频请求示例 (Hailuo-02，含首尾帧)

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "457",
    "params": {
      "model": "MiniMax-Hailuo-02",
      "prompt": "人物转身微笑，背景光线由暗变亮",
      "first_frame_image": "https://example.com/start.jpg",
      "last_frame_image": "https://example.com/end.jpg",
      "duration": 6,
      "resolution": "1080P",
      "aspect_ratio": "9:16"
    }
  }'
```

---

## 参考图生视频 (apiId: 459，S2V-01)

S2V-01（Subject to Video）专为保持主体一致性设计。`subject_reference` 使用 **object** 类型（非数组）。

### 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "459",
    "params": {
      "model": "S2V-01",
      "prompt": "角色向镜头走来，微笑打招呼",
      "subject_reference": {
        "image_url": "https://example.com/character.jpg"
      },
      "duration": 6,
      "resolution": "1080P",
      "aspect_ratio": "16:9"
    }
  }'
```
