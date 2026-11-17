# 带货口播调用示例

本文件给出两阶段契约的完整 JSON 形态，接入时照抄即可。示例只演示字段形态，方案正文按同目录 `prompt.md` 实际生成。

## 阶段一：请求生成方案

```json
{
  "imageList": ["https://cdn.example.com/product-main.jpg"],
  "customer_keywords": "便携冷萃咖啡壶，出差露营能用，30 秒出杯，免电动",
  "targetAudience": "25-35 岁户外通勤人群",
  "videoDuration": 15,
  "language": "英语",
  "salesRegion": "美国",
  "videoType": "SEED",
  "aspectRatio": "9:16",
  "resolution": "1080p"
}
```

此时 Skill 只输出 3 套方案并停止等待用户选择，**不调用任何底层视频能力**。

## 阶段一产出：schemes 结构

用户只看到方案编号，调用方必须在上下文中完整保留下面这个对象。此处只截取 1 个方案、1 个分镜示意，实际必须是 3 个方案，`shots` 数量按 `videoDuration / 3.5` 向下取整：

```json
{
  "schemes": [
    {
      "plan": "方案一：清晨出差场景",
      "language_instruction": "整个视频使用英语来进行口播",
      "negative_prompt": "无文字、无字幕、无水印、光滑肌肤、3D渲染、卡通、塑料、模糊、喷绘、影棚灯光、电影灯光、虚幻引擎、化妆滤镜、人工平滑",
      "visual_anchors": {
        "note": "以下描述将在所有分镜中强制复用以保证一致性",
        "person_anchor": "一个 30 岁的白种人男性用户，真实皮肤纹理，可见毛孔和不均匀色调，休闲连帽衫",
        "product_anchor": "一个黑色不锈钢圆柱形便携咖啡壶"
      },
      "plot": "出差早晨在酒店房间快速做一杯冷萃",
      "environment_setup": "现代美式酒店房间，大窗户自然光充足",
      "bgm": "轻快的原声吉他节奏",
      "shots": [
        {
          "meta": "0-3s | 视觉钩子",
          "camera": "手机前置 + 剧烈晃动",
          "visual": "【自拍】男子举起咖啡壶对着镜头，惊讶表情",
          "talk": "(English) Hotel coffee is terrible, so I stopped drinking it.",
          "prompt": "手机自拍角度，特写镜头，拍摄对象为白种人男性，蓝绿色眼睛，棕色头发，手持一个黑色不锈钢圆柱形便携咖啡壶，正在清晰地、不断地讲话，手持相机抖动，现代美式酒店房间背景，真实肌肤纹理，中性白平衡"
        }
      ]
    }
  ]
}
```

## 阶段二：按用户选择生成视频

写法 A，上下文保留了 `schemes`，推荐：

```json
{
  "imageList": ["https://cdn.example.com/product-main.jpg"],
  "customer_keywords": "便携冷萃咖啡壶，出差露营能用，30 秒出杯，免电动",
  "targetAudience": "25-35 岁户外通勤人群",
  "videoDuration": 15,
  "schemes": ["阶段一原样保留的 3 个方案对象"],
  "selectedSchemeNumber": 1,
  "videoType": "SEED"
}
```

写法 B，调用方无法保留上下文，直传结构化方案：

```json
{
  "imageList": ["https://cdn.example.com/product-main.jpg"],
  "customer_keywords": "便携冷萃咖啡壶，出差露营能用，30 秒出杯，免电动",
  "targetAudience": "25-35 岁户外通勤人群",
  "videoDuration": 15,
  "selectedScheme": {
    "plan": "方案一：清晨出差场景",
    "language_instruction": "整个视频使用英语来进行口播",
    "visual_anchors": {
      "person_anchor": "一个 30 岁的白种人男性用户，真实皮肤纹理，可见毛孔和不均匀色调，休闲连帽衫",
      "product_anchor": "一个黑色不锈钢圆柱形便携咖啡壶"
    },
    "shots": ["完整分镜数组，每个分镜含 visual / talk / prompt"]
  },
  "videoType": "SEED"
}
```

写法 C，显式跳过方案选择，仅当 `prompt` 已经是最终成片提示词：

```json
{
  "imageList": ["https://cdn.example.com/product-main.jpg"],
  "skipSchemeSelection": true,
  "prompt": "手机自拍角度，特写镜头，拍摄对象为白种人男性……（完整成片提示词）",
  "videoType": "SEED"
}
```

WAN 模型的图片字段不同，只能单图：

```json
{
  "imageUrl": "https://cdn.example.com/product-main.jpg",
  "customer_keywords": "便携冷萃咖啡壶，出差露营能用，30 秒出杯，免电动",
  "targetAudience": "25-35 岁户外通勤人群",
  "videoDuration": 15,
  "selectedSchemeNumber": 1,
  "schemes": ["阶段一原样保留的 3 个方案对象"],
  "videoType": "WAN"
}
```

## 会被拒绝的写法

```json
{ "selectedScheme": "方案一" }
```

静态文本冒充结构化方案，必须传对象。

```json
{ "prompt": "帮我做个咖啡壶带货视频" }
```

未传 `skipSchemeSelection: true` 就想跳过方案选择，且必填结构化字段缺失。
