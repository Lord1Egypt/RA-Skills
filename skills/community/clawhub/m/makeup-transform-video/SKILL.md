---
name: makeup-transform-video
version: 1.0.0
description: "生成拟人动物化妆变身短视频。素颜到惊艳的快节奏卡点反差内容，支持日常妆、约会妆、舞台妆、角色仿妆等场景，一句话描述直接出片。"

tags: [化妆, 变美, 反差, 创意, 拟人, 短视频]

metadata:
  openclaw:
    emoji: "💄"
    requires:
      bins: [node]

user-invocable: true
---

# 化妆变身视频生成

素颜到惊艳的反差视频——核心是反差感和卡点节奏，适合变美赛道、创意拟人内容、节日妆容展示。拟人动物角色（小狐狸/猫咪/兔兔）完成从素颜到精致的完整变身过程，5 秒内完成情绪弧线。

**依赖**：本目录 `scripts/video_gen.js` + 运行环境需设置 `WERYAI_API_KEY` + Node.js 18+。不依赖其他 Cursor 技能。

---

## 默认参数

| 参数 | 值 |
|------|----|
| 模型 | KLING_V3_0_PRO |
| 比例 | 9:16（固定） |
| 时长 | 5 秒（duration: 5，快节奏卡点） |
| 音频 | 关闭 |
| 视觉风格 | 正面近景/特写，柔和美妆布光，妆前自然光偏冷，妆后暖光增强高光，快节奏切换 |

> **API 合法性（默认 `KLING_V3_0_PRO`）**：文生 `duration` 仅 **5 / 10 / 15**，`aspect_ratio` 仅 **9:16、1:1、16:9**；图生 `aspect_ratio` 仅 **9:16、16:9、1:1**；**无 `resolution` 字段，请求勿传**。快档若用 VEO：文生 **`VEO_3_1_FAST`**、图生 **`CHATBOT_VEO_3_1_FAST`**，且 `duration` **固定 8**，`aspect_ratio` 仅 **9:16** 或 **16:9**。完整全模型表见 [`weryai-model-capabilities.md`](../references/weryai-model-capabilities.md)。

---

## 素颜到精致变身

**使用前准备：** 确认以下三项即可生成：
- 角色类型（小狐狸 / 猫咪 / 兔兔 / 小熊 / 可自定义任何动物）
- 妆容风格（日常妆 / 约会妆 / 舞台妆 / 圣诞节日妆 / 角色仿妆 / 夸张舞台妆）
- 反差强度（自然提升感 / 巨大反差 / 夸张角色变身）

生成时构建包含「素颜→化妆过程→完妆特写」完整弧线的 prompt，强调高光、眼妆细节和完妆后的气质变化。提交前展示参数确认：

**必须以表格展示所有参数，等待用户明确确认后再提交生成：**

   > 📋 **即将生成，请确认以下参数：**
   >
   > | 参数 | 本次值 | 说明 |
   > |------|--------|------|
   > | `model` | `KLING_V3_0_PRO` | 优档默认；快档：文生 `VEO_3_1_FAST`、图生 `CHATBOT_VEO_3_1_FAST`（`duration` 固定 8）；均衡→`KLING_V3_0_STA`；可直接指定模型名 |
   > | `aspect_ratio` | `9:16` | 默认 KLING：仅 9:16、1:1、16:9；换模见 [`../references/weryai-model-capabilities.md`](../references/weryai-model-capabilities.md) |
   > | `duration` | `5s` | KLING 系：5 / 10 / 15；切 VEO 快档：duration 仅 8 |
   > | `generate_audio` | `false` | 是否自动生成音频 |
   > | `prompt` | （本次构建的描述摘要） | 如需调整请告知 |
   > | `循环衔接` | 否 | 回复"循环"可开启 seamless loop |
   >
   > 直接回复**"确认"**开始生成，或告知需要修改的项目。

**示例 Prompt：**

> A small elegant fox with amber eyes starts with a clean bare face under soft natural window light, medium close-up frontal shot, the fox applies foundation with a damp sponge blending outward, then precise liquid liner wing tips extend dramatically, rich burgundy eyeshadow blended in the crease, final glossy red lip applied in one smooth stroke, the camera slowly pushes in as the fox turns to face forward — the transformation from plain to breathtaking dinner-party queen, warm beauty ring light catches highlighter on cheekbones, fast rhythm cut at final reveal, 9:16 portrait orientation

> A white cat with blue eyes applies full Christmas holiday makeup, close-up medium shot, bare-faced start with cool neutral lighting transitions to warm sparkle as glitter is pressed onto the inner corners, red and green eyeshadow gradient applied symmetrically, tiny gold star gems placed at the outer corners, deep berry lips finished with gloss, final reveal: the cat turns forward with a slow smile, sparkles catch the warm LED ring light, festive atmosphere, soft bokeh background with blurred fairy lights

> A gray bunny transforms with an exaggerated theatrical stage look in 3 compressed minutes, starting from entirely bare, each step dramatically cuts forward: base concealing all natural features, graphic black liner extending beyond the natural eye shape, neon orange shadow blended to the brow, rhinestones scattered across the lid, the final frame catches the bunny in full drag-inspired stage makeup under pure white theater lighting, jaw-dropping before-after contrast in a single vertical frame

**预期效果：** 妆容变化过程清晰，眼影层次和高光质感在视频中可见，最终完妆帧的气质与素颜帧形成强烈反差，适合变美/创意账号的卡点剪辑素材。

---

## 分步精致妆容过程

专注于单个妆步的极致细节，适合化妆教程向内容——强调产品质地、上妆手势、每一步的即时效果变化，而非整体变身弧线。

**使用前准备：** 明确想展示的妆步类型（底妆服帖感 / 眼线精准收尾 / 口红上色瞬间 / 睫毛膏刷层叠加 / 修容阴影塑形）以及角色造型偏好。

生成流程：收集妆步类型和细节偏好 → 构建强调手势动作和产品质地的 prompt → 确认参数 → 执行 `node {baseDir}/scripts/video_gen.js wait --json '…'`（字段与确认表一致）

> 生成前会展示参数，等待确认。

**示例 Prompt：**

> Extreme macro close-up of a small fox applying a single swipe of deep cherry-red lipstick across full lips, the bullet tip glides across the lower lip first then upper, leaving a perfect saturated pigment trail, the color payoff is immediate and glossy under ring light, the fox presses lips together once — lipstick perfectly transfers both sides, warm backlight catches the gloss sheen, static locked-off shot with shallow depth of field blurring background, slow motion 120fps, ASMR application sound

**参数配置：**

| 参数 | 值 |
|------|----|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | false |

---

## 注意事项

> **妆容层次感**：在 prompt 里明确列出 2-3 个妆步，如 `applies foundation → adds eyeshadow → finishes with lip` 的顺序描述，比笼统写"化妆"生成的妆容层次感更丰富。

> **反差强化**：在 prompt 中用 `bare-faced start` + `jaw-dropping transformation` + `before-after contrast` 三段式结构，确保模型理解这是一个有戏剧性弧线的视频，而不是静态美妆展示。

> **光线切换**：妆前用 `cool natural window light`，妆后用 `warm ring light catches highlighter`，光线温度的转变会让反差感在视觉上更强烈。
