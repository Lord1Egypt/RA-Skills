# 反馈调整指南

> 当生成结果不满意时，快速定位问题并修复

---

## 快速问题 → 快速修复对照表

### 皮肤/人物问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 皮肤太假/像塑料 | 过度美颜词 | 去掉 "flawless" → 加 "realistic skin texture, visible pores, natural imperfection" |
| 皮肤太油/反光 | 光线过强 | 加 "soft diffused lighting" → 去掉 "specular highlights" |
| 皮肤太干/质感差 | 缺少质感描述 | 加 "natural skin texture, subtle pores, healthy glow" |
| 人物太丑/畸形 | 缺少正向引导 | 加 "beautiful, elegant, refined features" + "anatomically correct" |
| 人物不够真实 | 缺少摄影术语 | 加 "photorealistic, authentic, true-to-life" |
| 表情僵硬 | 缺少表情描述 | 替换为 "natural smile, genuine expression, relaxed face" |

### 光线/曝光问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 太暗/看不清 | 光线不足 | 加 "bright, well-lit, naturally illuminated, even lighting" |
| 太亮/过曝 | 光线过强 | 加 "soft lighting, muted tones" → 去掉 "harsh light" |
| 光影不自然 | 光线描述冲突 | 统一为单一光源描述："single key light from [方向]" |
| 缺少氛围感 | 光线太平 | 加 "dramatic lighting, volumetric light rays, rim light" |
| 影子奇怪 | 光源混乱 | 明确光源："sunlight from upper left" |

### 风格/效果问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 风格不对 | 风格词不准确 | 替换整个风格块（见下方风格替换表） |
| 不够艺术 | 缺少艺术术语 | 加 "artistic, fine art, museum quality, gallery style" |
| 太艺术/不够真实 | 艺术词太多 | 改为 "photorealistic, authentic, documentary style" |
| 不够二次元 | 动漫词不足 | 加 "anime style, cel-shaded, bold outlines, vibrant anime colors" |
| 太卡通/低幼 | 动漫词太多 | 加 "mature, sophisticated, realistic proportions" |

### 风格替换表

| 目标风格 | 替换为 |
|---------|--------|
| 更写实 | "photorealistic, authentic, true-to-life, realistic lighting, documentary style" |
| 更插画 | "digital illustration, clean lines, professional illustration style" |
| 更动漫 | "anime style, cel-shaded, bold black outlines, vibrant anime colors" |
| 更电影感 | "cinematic, film still, anamorphic lens, cinematic color grading, film grain" |
| 更复古 | "vintage, retro, film grain, nostalgic, faded color grading" |
| 更极简 | "minimalist, clean, simple, generous white space, understated" |

### 构图问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 主体太小 | 缺少特写词 | 加 "close-up, tight framing, subject fills frame" |
| 主体太大/截断 | 缺少景别词 | 改为 "medium shot, full body visible, [X] proportion" |
| 构图呆板 | 缺少构图词 | 加 "dynamic composition, leading lines, rule of thirds" |
| 背景太乱 | 缺少背景虚化 | 加 "bokeh background, shallow depth of field, background in soft focus" |
| 缺少层次 | 缺少景深描述 | 加 "foreground, midground, background with distinct layers" |
| 角度不对 | 缺少视角词 | 改为 "low angle looking up" / "top-down view" / "eye level" |

### 颜色/色调问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 颜色太艳 | 饱和度过高 | 加 "muted tones, desaturated, soft colors" |
| 颜色太灰 | 饱和度过低 | 加 "vibrant colors, saturated, bold colors" |
| 色调偏暖 | 暖色过多 | 加 "cool tones, blue ambient, neutral color temperature" |
| 色调偏冷 | 冷色过多 | 加 "warm tones, golden light, amber accents" |
| 不够通透 | 缺少通透感 | 加 "clean, crisp, clear, fresh, bright highlights" |

### 细节/质量问庺

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 细节不够 | 缺少细节词 | 加 "ultra-detailed, intricate, high detail, elaborate" |
| 细节太多/太乱 | 细节词过多 | 减少复杂描述，改为 "simple, clean, minimal details" |
| 模糊/不清晰 | 缺少清晰词 | 加 "sharp focus, crystal clear, high resolution" |
| 有伪影/奇怪物 | AI 伪影 | 加 "clean, no artifacts, anatomically correct, no distortions" |
| 有水印/文字 | 未设置排除 | 加 "no watermark, no text, no logos" |

### 文字渲染问题

| 问题 | 原因 | 调整关键词 |
|------|------|-----------|
| 文字模糊 | 缺少文字清晰词 | 加 "crisp text, sharp typography, clear legible letters" |
| 文字位置不对 | 缺少位置描述 | 加 "bold text centered at top/bottom, text in [位置]" |
| 文字颜色看不清 | 缺少对比描述 | 加 "white text on dark background, high contrast typography" |

---

## 调整流程

### 步骤 1：定位问题类型

从上方表格中找到匹配的问题类型

### 步骤 2：应用调整关键词

替换或添加对应的调整关键词

### 步骤 3：生成调整版

```
基于你的反馈，调整了以下内容：

问题：「[原问题描述]」
调整：「[调整说明]」

调整后提示词：
[新提示词]

先试这个版本，如果还需要微调，告诉我具体哪里不满意。
```

---

## 常见场景的调整建议

### 人像摄影类

**问题：太假 →**
```
去掉：flawless, perfect, porcelain, airbrushed
加上：realistic skin texture, visible pores, natural imperfection,
      authentic, true-to-life, candid
```

**问题：氛围不够 →**
```
加上：cinematic lighting, dramatic shadows, volumetric light,
      moody atmosphere, film grain, cinematic color grading
```

### 插画/艺术类

**问题：不够艺术 →**
```
加上：fine art quality, gallery-worthy, artistic interpretation,
      expressive, masterful brushwork
```

**问题：太乱/太满 →**
```
去掉复杂描述
加上：minimalist composition, clean layout, breathing room,
      simple background, focused on subject
```

### 动漫/二次元类

**问题：不够二次元 →**
```
加上：anime style, cel-shaded, bold black outlines, anime eyes,
      vibrant saturated colors, manga-inspired
```

**问题：太卡通/低龄 →**
```
加上：mature anime, sophisticated character design,
      realistic anime proportions, detailed background
```

---

## 调整优先级

当有多个问题时，按以下优先级调整：

1. **核心主体** - 人物/物体本身是否正确
2. **风格定位** - 风格是否符合预期
3. **光线氛围** - 光线和情绪是否到位
4. **构图布局** - 画面是否舒适
5. **细节质量** - 清晰度、细节是否足够

先解决优先级高的问题，再逐步调整其他细节。
