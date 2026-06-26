---
name: mini-kitchen-video
version: 1.0.0
description: "生成迷你厨房烹饪短视频。支持文字描述直接出片，或将迷你厨具/食材图片转为真实烹饪动效。聚焦超小炊具的精致感、食材在微型锅具中的真实烹饪过程，以及反差萌带来的治愈停留效果。"

tags: [迷你厨房, 美食, 治愈, 手作, 猎奇, 短视频, video]

metadata:
  openclaw:
    emoji: "🍳"
    requires:
      bins: [node]

user-invocable: true
---

# 迷你厨房烹饪视频生成

三个方向让这类视频完播率极高：

- **反差萌**：真实灶台、真实火焰、真实油星——但全都缩到指尖大小，视觉冲击直接拉满
- **越小越精致**：迷你煎锅的油花、迷你火锅的沸腾气泡、迷你汉堡的芝士拉丝，微距下每一帧都是海报
- **治愈感强**：真实烹饪声（滋滋、沸腾、切菜）+ 暖光 + 慢动作，停留率比纯特效类高出一截

文字描述或一张厨具/食材图，直接出片。

**依赖**：本目录 `scripts/video_gen.js` + 运行环境需设置 `WERYAI_API_KEY` + Node.js 18+。不依赖其他 Cursor 技能。

---

## 默认参数

| 参数 | 值 |
|------|----|
| 模型 | KLING_V3_0_PRO（写实质感强，支持音效） |
| 比例 | 9:16（固定，抖音/快手竖版） |
| 时长 | 5s（短，爆点瞬间） |
| 风格 | 极近微距特写，温暖自然光，俯拍或 45° 斜视角，慢动作烹饪细节，精致手作感 |
| 音频 | 开启（滋滋声、沸腾声是核心爽感） |
| 循环衔接 | 否（默认；开启时在 prompt 末尾追加循环关键词） |

> **API 合法性（默认 `KLING_V3_0_PRO`）**：文生 `duration` 仅 **5 / 10 / 15**，`aspect_ratio` 仅 **9:16、1:1、16:9**；图生 `aspect_ratio` 仅 **9:16、16:9、1:1**；**无 `resolution` 字段，请求勿传**。快档若用 VEO：文生 **`VEO_3_1_FAST`**、图生 **`CHATBOT_VEO_3_1_FAST`**，且 `duration` **固定 8**，`aspect_ratio` 仅 **9:16** 或 **16:9**。完整全模型表见 [`weryai-model-capabilities.md`](../references/weryai-model-capabilities.md)。

---

## 文字描述直接出片

告诉我要做什么菜、用什么迷你炊具，以及你想强调的烹饪动作（煎/炒/涮/摆盘），我来构建 prompt 出片。适合快速测试不同菜品和烹饪手法的视觉效果。

菜品描述越具体越好：迷你铸铁锅煎单面蛋、掌心大的砂锅煮迷你拉面、指甲盖大小的汉堡胚在微型烤架上翻面……越具体，生成的细节越准。

**生成流程：**

1. 收集菜品描述和烹饪动作偏好
2. 根据食材特性和炊具类型构建 prompt，重点强化：食材在微型锅具中的真实反应（油花、气泡、颜色变化）、炊具精致质感、烹饪动作的慢动作节奏
3. 若未主动指定参数，展示本次配置并等待确认：

   > 即将使用以下参数生成，确认后开始（可直接回复"确认"或告知修改项）：
   > - model：KLING_V3_0_PRO
   > - aspect_ratio：9:16
   > - duration：5s
   > - generate_audio：true
   > - 循环衔接：否（回复"循环"可开启，将在 prompt 末尾追加 `seamless loop` 等关键词）

4. 确认后执行 `node {baseDir}/scripts/video_gen.js wait --json '…'`（文生，无 `image`），字段与参数表一致，解析 stdout 返回视频链接

**参数配置：**

| 参数 | 值 |
|------|----|
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Prompt 参考（迷你铸铁锅煎蛋）：**
> Extreme close-up macro shot, top-down overhead angle, a 3cm miniature black cast iron skillet resting on a tiny gas stove with real flickering blue flame, a single small quail egg cracked and dropped into the pan in 120fps slow motion, the egg white spreads and immediately begins to bubble and set at the edges, golden oil sizzles with tiny popping bubbles forming a ring around the still-runny yolk, warm amber side lighting from the left casts soft shadows that reveal the glossy egg surface texture, wisps of steam curl upward backlit by the warm light, cozy wooden kitchen counter surface visible in soft bokeh background, satisfying sizzle ASMR

**Prompt 参考（掌心迷你火锅沸腾）：**
> Close-up macro shot at 45-degree angle looking down slightly, a palm-sized matte black ceramic hot pot with deep crimson spicy broth at a vigorous rolling boil, miniature chopsticks no wider than a matchstick dip a 1cm wagyu beef slice into the bubbling soup in slow motion at 60fps, the meat curls immediately and transitions from raw pink to seared golden-brown, tiny dried chili rings and Sichuan peppercorns swirl in the crimson broth, warm golden backlight creates glowing caustic ripple patterns across the broth surface, dramatic steam rising against a dark moody kitchen background, deep satisfying bubbling ASMR sound

**Prompt 参考（迷你汉堡组装摆盘）：**
> Eye-level medium macro shot with a subtle upward tilt, a 4cm mini sesame-seed burger bun sits on a white marble cutting board, two tiny hands use precision tweezers to layer a 2cm beef patty, a slice of melted cheddar drooping over the edges, micro lettuce leaf and a tomato disc no bigger than a fingernail, in slow motion the top bun is pressed gently down and the cheese stretches in a thin glossy pull, warm studio key light from upper-left creates appetite-stimulating golden highlights on the toasted bun surface, shallow depth of field renders the background in buttery bokeh, the entire assembled burger fits entirely within a fingertip, charming and surreal scale contrast

**预期效果：** 微距镜头完整捕捉食材在迷你炊具中的真实烹饪细节，反差萌感突出，暖光质感治愈，烹饪音效与画面节奏配合，抖音完播率高。

---

## 迷你厨具图片转烹饪动效

上传一张迷你炊具、食材或摆盘照片，生成以该物件为主体的烹饪动效视频。适合将产品图或开箱图二次利用，快速产出对应的"动起来"内容。

提供图片 URL（必须是可公开访问的 HTTPS 地址），并告知期望的烹饪动作（开始翻炒 / 食材下锅 / 起锅摆盘 / 火锅沸腾）。我会识别图片中炊具类型和食材颜色，构建与原图视觉风格一致的烹饪动效 prompt。

**生成流程：**

1. 收集图片 URL 和期望动效描述
2. 根据图片主体（炊具类型、食材形态、光线环境）构建烹饪动效 prompt，保持与原图的色调和风格一致
3. 展示本次参数并等待确认：

   > 即将使用以下参数生成，确认后开始（可直接回复"确认"或告知修改项）：
   > - model：KLING_V3_0_PRO
   > - aspect_ratio：9:16
   > - duration：5s
   > - generate_audio：true
   > - image：（你提供的图片 URL）
   > - 循环衔接：否（回复"循环"可开启）

4. 确认后执行 `node {baseDir}/scripts/video_gen.js wait --json '…'`（含 `image`），解析 stdout 返回视频链接

**参数配置：**

| 参数 | 值 |
|------|----|
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | 用户提供的图片 URL |

**Prompt 参考（迷你厨具图转烹饪动效）：**
> Matching the angle and lighting of the provided image, animate the miniature kitchen scene coming to life: the tiny stove flame ignites with a gentle blue flicker, the miniature pan or pot begins to heat up, food ingredients inside start to sizzle or bubble responding to the heat in realistic slow motion at 60fps, the cooking process captures authentic food physics — oil shimmer, steam rising, ingredient color changing as it cooks, macro close-up perspective maintains the original image's scale and intimacy, warm natural light consistent with the source image, satisfying realistic cooking ASMR sounds of sizzle and bubbling

**预期效果：** 图片中的迷你厨具和食材自然"动起来"，烹饪动作与食材类型匹配，色调与原图一致，反差萌感保留。

---

## 使用技巧

### Prompt 强化方向

- **放大反差感**：在 prompt 中明确写出尺寸对比，如 `fits entirely within a fingertip`、`no bigger than a thumbnail`、`palm-sized`，AI 更容易生成准确的微缩比例
- **强化食材真实反应**：具体描述食物在受热时的物理变化，如 `egg white sets at the edges`、`cheese stretches in a thin glossy pull`、`meat curls immediately`，而不是泛化的"cooking"
- **慢动作参数**：在 prompt 中加入 `120fps slow motion` 或 `60fps slow motion` 让烹饪细节更清晰，是完播率的关键
- **开启循环衔接**时，在 prompt 末尾追加：`seamless loop, first and last frame identical, perfectly looping`

### 常见问题

- 图片 URL 必须是 HTTPS 公网可访问地址，本地路径无效，建议先上传到图床（如 imgbb、cloudinary）
- 迷你便当、迷你甜品等多食材场景，建议在 prompt 中逐一描述每种食材的尺寸和摆盘位置，避免 AI 忽略细节
- 若想突出精致感，在 prompt 中指定背景材质（白色大理石、原木砧板、深色石板），比直接写"漂亮背景"效果好得多

> **注意**：`aspect_ratio` 参数不是所有模型都支持，若调用时遇到参数报错，尝试去掉该参数后重试。
