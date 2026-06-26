# 可灵 (Kling) API 参考

> 品牌方：快手 | 平台：京东云 JoyCreator

---

## apiId 速查表

### 视频生成

| 任务类型 | 模型版本 | apiId | model_name 值 |
|---------|---------|-------|--------------|
| 文生视频 | Kling-V2.5-Turbo | `551` | `kling-v2-5-turbo` |
| 文生视频 | Kling-V2.6 | `563` | `kling-v2-6` |
| 文生视频 | Kling-V3 | `565` | `Kling-V3` |
| 文生视频 | Kling-O1 | `560` | `kling-video-o1` |
| 图生视频 | Kling-V2.1 | `550` | `kling-v2-1` |
| 图生视频 | Kling-V2.6 | `564` | `kling-v2-6` |
| 图生视频 | Kling-V3 | `566` | `Kling-V3` |
| 图生视频 | Kling-O1 | `561` | `kling-video-o1` |
| 参考图生视频 | Kling-V1.6 | `552` | `kling-v1-6` |
| 参考图生视频 | Kling-O1 | `562` | `kling-video-o1` |

### 图像生成

| 任务类型 | 模型版本 | apiId | model_name 值 |
|---------|---------|-------|--------------|
| 文生图 | Kling-V2.1 | `553` | `kling-v2-1` |
| 图生图 | Kling-V2 | `554` | `kling-v2` |

---

## 视频生成通用参数

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_name` | string | ✅ | 见上表 |
| `prompt` | string | ✅ | 视频内容描述词 |
| `duration` | string | ✅ | V2.x/O1: `"5"` 或 `"10"`；V3: `"3"` 到 `"15"` |
| `mode` | string | ✅ | `"pro"` 或 `"std"`（V2.6/O1 仅支持 `"pro"`） |
| `aspect_ratio` | string | 条件 | `"16:9"` / `"9:16"` / `"1:1"` |
| `sound` | string | ❌ | 同步音频：`"on"` / `"off"`（仅 563-566 支持） |

---

## 文生视频

### Kling-V3 请求示例（多镜头）

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "565",
    "params": {
      "model_name": "Kling-V3",
      "prompt": "一个宇航员漫步在月球表面，地球在远处缓缓升起",
      "duration": "10",
      "mode": "pro",
      "aspect_ratio": "16:9",
      "sound": "on",
      "multi_shot": "true",
      "shot_type": "intelligence"
    }
  }'
```

### Kling-V2.6 请求示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "563",
    "params": {
      "model_name": "kling-v2-6",
      "prompt": "城市延时摄影，车流如光河般涌动，夜色下的摩天大楼灯光渐次亮起",
      "duration": "10",
      "mode": "pro",
      "aspect_ratio": "16:9",
      "sound": "off"
    }
  }'
```

---

## 图生视频

### 特有字段

| 字段名 | 类型 | 适用 apiId | 说明 |
|--------|------|-----------|------|
| `image` | string | 550, 564, 566 | 首帧图片 URL |
| `image_tail` | string | 550, 564, 566 | 尾帧图片 URL（可选） |
| `image_urls` | string[] | 561 (O1) | 参考图数组 |

### Kling-V3 图生视频（首尾帧）示例

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "566",
    "params": {
      "model_name": "Kling-V3",
      "image": "https://example.com/start.jpg",
      "image_tail": "https://example.com/end.jpg",
      "prompt": "画面从静止的湖面转为微波荡漾，阳光洒落",
      "duration": "10",
      "mode": "pro",
      "sound": "on",
      "multi_shot": "true"
    }
  }'
```

---

## 参考图生视频

### Kling-V1.6 (apiId: 552)

使用 `image_references` 对象数组保持主体一致性：

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "552",
    "params": {
      "model_name": "kling-v1-6",
      "prompt": "角色在花园中奔跑，衣摆随风飘动",
      "image_references": [
        {"image_url": "https://example.com/character1.jpg"},
        {"image_url": "https://example.com/character2.jpg"}
      ],
      "duration": "5",
      "mode": "pro",
      "aspect_ratio": "16:9"
    }
  }'
```

### Kling-O1 (apiId: 562)

使用 `ref_video` + `image_list` 组合参考：

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "562",
    "params": {
      "model_name": "kling-video-o1",
      "prompt": "保持动作风格，生成角色打太极的视频",
      "ref_video": "https://example.com/reference_motion.mp4",
      "image_list": ["https://example.com/character.jpg"],
      "duration": "5",
      "mode": "pro"
    }
  }'
```

---

## 图像生成 (apiId: 553 / 554)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_name` | string | ✅ | 见上表 |
| `prompt` | string | ✅ | 描述词 |
| `aspect_ratio` | string | ✅ | `"16:9"` / `"9:16"` / `"1:1"` / `"4:3"` / `"3:4"` |
| `taskNum` | int | ✅ | 生成数量，1-4 |
| `image` | string | ❌ | 参考图 URL（仅 554 图生图支持） |

### 文生图示例 (Kling-V2.1)

```bash
curl -X POST "https://model.jdcloud.com/joycreator/openApi/submitTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JOYCREATOR_APP_KEY}" \
  -H "x-jdcloud-request-id: $(uuidgen)" \
  -d '{
    "apiId": "553",
    "params": {
      "model_name": "kling-v2-1",
      "prompt": "古风山水画，云雾缭绕的峰峦，远处一叶扁舟",
      "aspect_ratio": "16:9",
      "taskNum": 2
    }
  }'
```
