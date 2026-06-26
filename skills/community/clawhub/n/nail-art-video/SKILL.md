---
name: nail-art-video
version: 1.0.0
description: "生成美甲制作过程短视频。猫眼、流沙、星空、奶油胶、微缩立体美甲——小尺寸极高细节，近景治愈感强，支持节日主题，一句话出片。"

tags: [美甲, 精致, asmr, 变美, 手作, 短视频]

metadata:
  openclaw:
    emoji: "💅"
    requires:
      bins: [node]

user-invocable: true
---

# 美甲制作视频生成

涂胶的弧线感、猫眼粉在磁石下瞬间汇聚成线、封层灯照后的镜面光泽——美甲视频的爆点全在这几秒里。小兔/猫咪给爪爪做精致美甲，每个细节都是治愈素材，配合后期的 ASMR 刷甲声效，完播率不需要担心。

**依赖**：本目录 `scripts/video_gen.js` + 运行环境需设置 `WERYAI_API_KEY` + Node.js 18+。不依赖其他 Cursor 技能。

---

## 默认参数

| 参数 | 值 |
|------|----|
| 模型 | KLING_V3_0_PRO |
| 比例 | 9:16（固定，竖版手部近景） |
| 时长 | 5 秒（duration: 5，细节爆点聚焦） |
| 音频 | 开启（涂胶声、UV灯滴滴声是美甲视频核心 ASMR 体验） |
| 视觉风格 | 极近微距，手部特写，白色背景，柔和漫射光，光泽质感优先，颜色饱和度高 |

> **API 合法性（默认 `KLING_V3_0_PRO`）**：文生 `duration` 仅 **5 / 10 / 15**，`aspect_ratio` 仅 **9:16、1:1、16:9**；图生 `aspect_ratio` 仅 **9:16、16:9、1:1**；**无 `resolution` 字段，请求勿传**。快档若用 VEO：文生 **`VEO_3_1_FAST`**、图生 **`CHATBOT_VEO_3_1_FAST`**，且 `duration` **固定 8**，`aspect_ratio` 仅 **9:16** 或 **16:9**。完整全模型表见 [`weryai-model-capabilities.md`](../references/weryai-model-capabilities.md)。

---

## 拟人角色美甲制作

小动物爪爪做精致美甲，是这个赛道的专属内容形式。爪爪尺寸小、动作轻柔、指甲形状圆润——天然适合美甲近景治愈内容。

描述角色和想做的甲款，剩下的由 prompt 填充：

**生成流程：**

收集角色描述 + 美甲款式 → 构建强调涂胶光泽、猫眼线条、封层镜面等视觉爆点的 prompt → 展示参数确认 → 执行 `node {baseDir}/scripts/video_gen.js wait --json '…'`（字段与确认表一致）

> 即将使用以下参数生成，确认后开始：
> - model：KLING_V3_0_PRO
> - aspect_ratio：9:16
> - duration：5
> - generate_audio：true
> - 循环衔接：否（回复"循环"可开启）

**示例 Prompt：**

> Extreme macro close-up of a small bunny's delicate paws, a nail technician applies deep navy cat-eye gel in a single smooth arcing stroke, immediately a slender magnetic wand sweeps slowly across the nail surface — fine metalite particles drift and gather in a perfect luminous line running from cuticle to tip, the nail is cured under UV light for 30 seconds, final reveal: three perfectly finished cat-eye nails with a moving aurora-like shimmer line visible in different angles, soft diffused white backlight, ASMR gel application and magnet sweep sound, minimal cream background

> A small cat's round paws receive cherry blossom gel nails, medium macro shot, each nail gets a thin base of sheer pink gel, then a fine nail art brush places delicate three-petal sakura designs in white and pale rose, tiny yellow dot stamens added with a dotting tool, translucent overlay encases each flower, UV cure flash, final close-up pans across five perfectly finished nails with dimensional flowers visible under the gel surface, warm diffused salon light, ASMR brush stroke sound, white cotton pad background

> A hamster's tiny paws get ultra-detailed Christmas theme nails, extreme close-up overhead, nail art pen draws miniature candy canes on alternating nails, one nail receives a tiny Christmas tree built up in green gel layers with sparkle top coat, red glitter gel sweeps a single accent nail, matte topcoat applied last for contrast, the final reveal shows five nails telling a tiny holiday story under warm macro ring light, ASMR application sounds, white ceramic nail rest surface

**参数配置：**

| 参数 | 值 |
|------|----|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

---

## 材质特写 ASMR 版本

不需要角色，纯聚焦美甲材料的质感瞬间：流沙粉在指甲盖上流动、奶油胶被刮刀抹开的绵软感、凝胶被灯光从半透明变成完全固化——材质本身就是内容。

说明想展示的材质类型，直接生成：

**必须以表格展示所有参数，等待用户明确确认后再提交生成：**

   > 📋 **即将生成，请确认以下参数：**
   >
   > | 参数 | 本次值 | 说明 |
   > |------|--------|------|
   > | `model` | `KLING_V3_0_PRO` | 优档默认；快档：文生 `VEO_3_1_FAST`、图生 `CHATBOT_VEO_3_1_FAST`（`duration` 固定 8）；均衡→`KLING_V3_0_STA`；可直接指定模型名 |
   > | `aspect_ratio` | `9:16` | 默认 KLING：仅 9:16、1:1、16:9；换模见 [`../references/weryai-model-capabilities.md`](../references/weryai-model-capabilities.md) |
   > | `duration` | `5s` | KLING 系：5 / 10 / 15；切 VEO 快档：duration 仅 8 |
   > | `generate_audio` | `true` | 是否自动生成音频 |
   > | `prompt` | （本次构建的描述摘要） | 如需调整请告知 |
   > | `循环衔接` | 否 | 回复"循环"可开启 seamless loop |
   >
   > 直接回复**"确认"**开始生成，或告知需要修改的项目。

**示例 Prompt：**

> Extreme close-up macro shot of quicksand nail art being manipulated, a nail's surface shimmers with ultrafine copper and gold sand particles that shift and flow in a liquid-like wave as the hand tilts slowly, microscopic metallic particles catch a focused spot light and scatter rainbow micro-glints, the sand settles into a new pattern with each movement, slow motion 120fps, ASMR dry sand whisper sound, black velvet background to maximize sparkle contrast, static locked-off macro lens

---

## ASMR 和质感关键词

**猫眼线条感**：`magnetic cat-eye line gathers precisely`, `aurora shimmer streak`, `luminous moving line under light`, `metalite particles align in perfect gradient`

**封层镜面感**：`mirror topcoat reflects surroundings`, `glossy gel surface catches every light`, `depth illusion under clear gel encapsulation`, `3D dimensional effect preserved under dome coat`

**涂胶 ASMR 声**：`ASMR gel brush stroke sound`, `UV lamp cure beep`, `nail file grit sound`, `cap click of gel bottle`

> **提示**：美甲视频的光线设置非常关键。`soft diffused white backlight` 让甲面反光柔和，`focused spot light from above` 让猫眼线和闪粉更凸显。在 prompt 中明确光源角度，视觉爆点会更稳定。
