# 阶段一：意图路由规则 (Router Rules)

本文档定义如何将用户自然语言输入解析为结构化意图 JSON，供阶段二模型推荐使用。

---

## 输出 Schema（严格遵循）

```json
{
  "intent_type": "IMAGE_GENERATION" | "VIDEO_GENERATION" | "UNKNOWN",
  "core_prompt": "string",
  "base_params": {
    "aspect_ratio": "16:9" | "9:16" | "1:1" | "4:3" | "3:4",
    "has_reference": boolean,
    "brand_preference": "Kling" | "Vidu" | "Doubao" | "Hailuo" | null
  },
  "video_features": {
    "needs_audio": boolean,
    "camera_movement": "string" | null,
    "duration": number
  },
  "image_features": {
    "task_num": number,
    "high_quality_req": boolean
  }
}
```

---

## 一、基础意图识别 (intent_type)

### IMAGE_GENERATION（生图）触发词
包含以下关键词时判定为图像生成：
- 画、生成图片、生成图像、照片、海报、壁纸、插图、概念图、设计稿
- 头像、封面、banner、缩略图、产品图、商品图

### VIDEO_GENERATION（生视频）触发词
包含以下关键词时判定为视频生成：
- 视频、短片、动画、动图、生成视频、做视频
- 航拍、推镜头、运镜、转场、延时摄影
- 短剧、MV、广告片、宣传片

### UNKNOWN
无法归类到上述任意意图时返回。

---

## 二、Prompt 优化 (core_prompt)

**处理规则：**
1. 剔除口语化表达（"帮我"、"能不能"、"我想要"等）
2. 补全隐含的主体、动作、光影、视角等细节
3. 保留用户的核心创意意图
4. 中文 prompt 保持中文，无需强制翻译为英文

**示例：**
- 输入：`帮我画一张很漂亮的女孩在海边的图`
- 输出：`一位年轻女性站在海边，夕阳余晖，海浪轻抚沙滩，逆光人像，写实摄影风格`

---

## 三、通用参数提取 (base_params)

### aspect_ratio（画幅比例）

| 用户表述 | 推断值 |
|---------|--------|
| 横屏、电脑壁纸、宽屏、16:9 | `16:9` |
| 竖屏、手机壁纸、竖版、9:16 | `9:16` |
| 头像、正方形、1:1 | `1:1` |
| 封面、4:3 | `4:3` |
| 竖版封面、3:4 | `3:4` |
| 未提及 | 默认 `16:9` |

### has_reference
- `true`：用户上传了图片，或提到"参考图"、"按照这张图"、"图生图"、"图生视频"
- `false`：纯文字描述，无参考图

### brand_preference
用户明确提到品牌名时提取：

| 用户提到 | 输出值 |
|---------|--------|
| 可灵、Kling | `Kling` |
| Vidu | `Vidu` |
| 豆包、Seedream、Seedance | `Doubao` |
| 海螺、Hailuo、MiniMax | `Hailuo` |
| 拍我 | `Paiwo` |
| 未提及 | `null` |

---

## 四、视频专属特征 (video_features)

> 仅 `intent_type == VIDEO_GENERATION` 时填写，否则返回默认值

### needs_audio
- `true`：用户提到"有声音"、"配乐"、"配音"、"同步音频"、"对口型"、"有台词"、"方言"
- `false`：未提及音频需求

### camera_movement
提取运镜关键词（如有）：
- 推镜头、拉镜头、平移、旋转、航拍、跟拍、环绕、快速运镜、慢镜头
- 无运镜描述时返回 `null`

### duration
- 用户明确提到秒数时提取（如"5秒视频"→ `5`）
- 未提及时默认返回 `5`

---

## 五、图像专属特征 (image_features)

> 仅 `intent_type == IMAGE_GENERATION` 时填写，否则返回默认值

### task_num
- 用户提到"画4张"、"生成3张"时提取数量
- 未提及时默认 `1`，最大不超过 `4`

### high_quality_req
- `true`：用户提到 2K、4K、8K、超高清、极致清晰、高分辨率
- `false`：未提及特殊分辨率要求

---

## 六、Few-Shot 示例

### 示例 1：文生图
**输入**：`帮我画一张横版电商产品图，一个护肤品瓶子，简洁背景`

**输出**：
```json
{
  "intent_type": "IMAGE_GENERATION",
  "core_prompt": "护肤品瓶子产品展示图，极简白色背景，柔和散射光，高端商业摄影风格",
  "base_params": {
    "aspect_ratio": "16:9",
    "has_reference": false,
    "brand_preference": null
  },
  "video_features": { "needs_audio": false, "camera_movement": null, "duration": 5 },
  "image_features": { "task_num": 1, "high_quality_req": false }
}
```

### 示例 2：文生视频（含音频+运镜）
**输入**：`做一个10秒竖版视频，两个武侠人物在竹林打斗，要有音效`

**输出**：
```json
{
  "intent_type": "VIDEO_GENERATION",
  "core_prompt": "两名武侠在茂密竹林中激烈对决，刀光剑影，竹叶飞舞，快速运镜，写实武侠风格",
  "base_params": {
    "aspect_ratio": "9:16",
    "has_reference": false,
    "brand_preference": null
  },
  "video_features": { "needs_audio": true, "camera_movement": "快速运镜", "duration": 10 },
  "image_features": { "task_num": 1, "high_quality_req": false }
}
```

### 示例 3：图生视频（含参考图+品牌偏好）
**输入**：`用可灵把这张图做成视频，人物走向镜头`

**输出**：
```json
{
  "intent_type": "VIDEO_GENERATION",
  "core_prompt": "人物从画面远端缓缓走向镜头，步伐自然，背景保持原图场景",
  "base_params": {
    "aspect_ratio": "16:9",
    "has_reference": true,
    "brand_preference": "Kling"
  },
  "video_features": { "needs_audio": false, "camera_movement": "推镜头", "duration": 5 },
  "image_features": { "task_num": 1, "high_quality_req": false }
}
```

### 示例 4：方言短剧
**输入**：`做一段四川方言搞笑短剧，两个角色在对话，要有声音`

**输出**：
```json
{
  "intent_type": "VIDEO_GENERATION",
  "core_prompt": "四川方言搞笑对话短剧，两名角色面对面交流，轻松幽默场景，室内环境",
  "base_params": {
    "aspect_ratio": "9:16",
    "has_reference": false,
    "brand_preference": null
  },
  "video_features": { "needs_audio": true, "camera_movement": null, "duration": 5 },
  "image_features": { "task_num": 1, "high_quality_req": false }
}
```
