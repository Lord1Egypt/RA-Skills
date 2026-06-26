# 提示词模板库 (Prompt Templates)

> 分场景模板体系 | NanobananaPro 生图 Skill 核心知识库

---

## 📖 使用说明

**模板结构：**
- 模板名称 + 适用场景
- 基础结构（主控前缀 + 核心描述 + 参数）
- 可变量标注 `[变量名]`
- 权重建议
- 示例输出

**可变量说明：**
- `[主体]` - 核心描述对象
- `[场景]` - 环境/背景
- `[动作]` - 姿态/行为
- `[风格]` - 美学风格
- `[光影]` - 光源描述
- `[色彩]` - 色彩方案
- `[比例]` - 画幅比例

---

## 👤 一、人物类模板

### 1.1 人像写真（单人）

**适用场景：** 个人写真、商业人像、社交媒体头像

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, professional portrait photography, --ar [比例] --style raw --s [强度] --q 2

【核心主体】[人物描述：年龄/性别/发型/服装/表情], [姿态描述], [拍摄角度]

【场景环境】[背景描述：室内/室外/纯色/虚化], [环境元素]

【风格&美学】[风格关键词], [美学特征], [情绪氛围]

【光影&色彩】[光源类型], 光源方向, color temperature [色温]K, [色彩方案]

【画质&细节】[相机型号], [镜头焦段]mm, f/[光圈值], [质感要求]

【负面提示词】ugly, deformed, bad anatomy, disfigured, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad art, beginner, amateur, blurry
```

**可变量默认值：**
- `[比例]` → 3:4（小红书）/ 9:16（抖音）/ 1:1（头像）
- `[强度]` → 150-250
- `[色温]` → 5500（自然光）/ 3200（暖光）/ 6500（冷光）
- `[光圈值]` → 2.8（浅景深）/ 5.6（中景深）/ 8（深景深）

**示例（职场女性形象照）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, professional portrait photography, --ar 3:4 --style raw --s 200 --q 2

【核心主体】Professional asian woman, age 28, shoulder-length black hair, wearing navy blue blazer and white shirt, confident smile, three-quarter view, eye level shot

【场景环境】Modern office background with soft bokeh, floor-to-ceiling windows, minimalist interior

【风格&美学】Corporate headshot, professional photography, approachable yet authoritative, clean composition

【光影&色彩】Softbox lighting from front-left 45°, color temperature 5500K, neutral color palette with warm skin tones

【画质&细节】Canon EOS R5, 85mm lens, f/2.8, sharp focus on eyes, smooth skin texture, professional retouching

【负面提示词】ugly, deformed, bad anatomy, disfigured, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad art, beginner, amateur, blurry
```

---

### 1.2 角色设计（游戏/动漫）

**适用场景：** 游戏角色、动漫人物、IP 形象

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, character design sheet, --ar 16:9 --style [风格] --s [强度] --q 2

【核心主体】[角色名称/类型], [年龄外貌], [发型发色], [服装细节], [配饰武器], [表情神态]

【场景环境】Character turnaround sheet, white background, multiple views (front/side/back)

【风格&美学】[风格：日漫/美漫/国漫/厚涂], [艺术特征], [色彩风格]

【光影&色彩】Even studio lighting, color temperature 5500K, [主色调], [辅色调]

【画质&细节】Clean line art, cel shaded / painterly rendering, high detail, character model sheet quality

【负面提示词】ugly, deformed, bad anatomy, extra limbs, missing limbs, asymmetric eyes, malformed hands, mutation, mutated, extra fingers, poorly drawn hands, poorly drawn face
```

**示例（仙侠游戏女主）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, character design sheet, --ar 16:9 --style expressive --s 250 --q 2

【核心主体】Female xianxia cultivator, age 20 appearance, long flowing silver hair with jade hairpins, wearing white and light blue hanfu with embroidered cloud patterns, holding celestial sword, serene expression with determined eyes

【场景环境】Character turnaround sheet, white background, multiple views (front/side/back), floating cherry blossom petals

【风格&美学】Chinese anime donghua style, ethereal fantasy aesthetic, flowing fabrics, detailed costume design

【光影&色彩】Soft volumetric lighting, color temperature 6000K, primary white and blue palette with gold accents, god rays effect

【画质&细节】Clean line art, detailed painterly rendering, high detail costume textures, character model sheet quality, octane render

【负面提示词】ugly, deformed, bad anatomy, extra limbs, missing limbs, asymmetric eyes, malformed hands, mutation, mutated, extra fingers, poorly drawn hands, poorly drawn face
```

---

### 1.3 动作姿态（动态场景）

**适用场景：** 运动场景、舞蹈、打斗、动态展示

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, dynamic action shot, --ar [比例] --style [风格] --s [强度] --q 2

【核心主体】[人物描述], [动作描述：动词 + 姿态], [服装状态：飘动/褶皱], [表情：专注/激情/张力]

【场景环境】[场景描述], [动态元素：速度线/残影/粒子], [氛围元素]

【风格&美学】[风格], dynamic composition, motion blur, action photography aesthetic

【光影&色彩】[光源], dramatic lighting, color temperature [色温]K, [色彩对比]

【画质&细节】[相机], [快门速度]s, [镜头], frozen action with motion blur background, high energy

【负面提示词】ugly, deformed, bad anatomy, static pose, stiff, rigid, blurry subject, out of focus, poorly drawn hands, extra limbs
```

**示例（街舞舞者）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, dynamic action shot, --ar 9:16 --style raw --s 200 --q 2

【核心主体】Male street dancer, age 22, wearing oversized hoodie and baggy jeans, mid-air breakdance freeze pose, one hand supporting body, legs extended dynamically, intense focused expression

【场景环境】Urban street at night, graffiti wall background, motion blur trails, floating dust particles, dramatic atmosphere

【风格&美学】Street photography, dynamic composition, motion blur, action photography aesthetic, high energy

【光影&色彩】Neon street lights from multiple directions, dramatic lighting, color temperature 4000K, high contrast with purple and cyan accents

【画质&细节】Sony A7S III, 1/500s shutter speed, 35mm lens, frozen action with motion blur background, high energy

【负面提示词】ugly, deformed, bad anatomy, static pose, stiff, rigid, blurry subject, out of focus, poorly drawn hands, extra limbs
```

---

## 🏠 二、场景类模板

### 2.1 室内场景（家居/商业/办公）

**适用场景：** 室内设计、房产展示、商业空间

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, architectural photography, --ar 16:9 --style raw --s 150 --q 2

【核心主体】[空间类型：客厅/办公室/餐厅], [风格：现代/北欧/工业/新中式], [主要家具], [材质细节]

【场景环境】[空间布局], [窗户/采光], [装饰元素], [绿植/艺术品]

【风格&美学】[风格关键词], interior design photography, spacious composition, professional staging

【光影&色彩】Natural light from [方向], color temperature [色温]K, [色彩方案], warm/cool ambient lighting

【画质&细节】[相机], [镜头]mm, f/[光圈], wide angle perspective, sharp details, HDR quality

【负面提示词】ugly, deformed, cluttered, messy, dirty, poorly lit, dark corners, low quality, amateur, blurry
```

**示例（现代客厅）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, architectural photography, --ar 16:9 --style raw --s 150 --q 2

【核心主体】Modern living room, scandinavian minimalist style, gray sectional sofa, oak coffee table, wool area rug, textured throw pillows

【场景环境】Open floor plan, floor-to-ceiling windows with sheer curtains, pendant lighting, abstract wall art, potted monstera plant

【风格&美学】Scandinavian interior design, interior design photography, spacious composition, professional staging, hygge atmosphere

【光影&色彩】Natural light from south-facing windows, color temperature 5500K, neutral palette with warm wood tones, soft ambient lighting

【画质&细节】Canon EOS R5, 16mm lens, f/8, wide angle perspective, sharp details, HDR quality

【负面提示词】ugly, deformed, cluttered, messy, dirty, poorly lit, dark corners, low quality, amateur, blurry
```

---

### 2.2 室外场景（城市/自然/建筑）

**适用场景：** 城市风光、自然景观、建筑摄影

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, landscape photography, --ar [比例] --style raw --s 150 --q 2

【核心主体】[主体：山脉/建筑/街道], [时间：日出/正午/日落/夜晚], [天气：晴朗/多云/雨/雪]

【场景环境】[前景元素], [中景主体], [背景层次], [天空状态]

【风格&美学】[风格], landscape photography, layered composition, dramatic scenery

【光影&色彩】[光源方向], golden hour / blue hour, color temperature [色温]K, [色彩特征]

【画质&细节】[相机], [镜头]mm, f/[光圈], deep depth of field, ultra sharp, large format quality

【负面提示词】ugly, deformed, flat lighting, boring composition, overexposed, underexposed, hazy, low quality, amateur
```

**示例（城市日落）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, landscape photography, --ar 21:9 --style raw --s 150 --q 2

【核心主体】Modern city skyline, sunset timing, clear sky with scattered clouds

【场景环境】Foreground: waterfront promenade, Middle: glass skyscrapers reflecting sunset, Background: distant mountains, Sky: orange and purple gradient

【风格&美学】Urban landscape photography, landscape photography, layered composition, dramatic scenery, cinematic framing

【光影&色彩】Sunset light from west, golden hour, color temperature 3500K, warm orange and purple sky, building reflections

【画质&细节】Phase One XF IQ4, 24mm lens, f/11, deep depth of field, ultra sharp, large format quality

【负面提示词】ugly, deformed, flat lighting, boring composition, overexposed, underexposed, hazy, low quality, amateur
```

---

### 2.3 幻想场景（科幻/奇幻/梦境）

**适用场景：** 概念艺术、游戏场景、创意视觉

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, concept art, --ar 16:9 --style [风格] --s [强度] --q 2

【核心主体】[幻想主体：未来城市/魔法森林/外星景观], [核心元素], [建筑风格/自然特征]

【场景环境】[大气效果：雾/云/粒子], [光源：多个太阳/霓虹/魔法光], [特殊元素]

【风格&美学】[风格：赛博朋克/奇幻/超现实], concept art, epic scale, imaginative world building

【光影&色彩】[特殊光源], dramatic atmospheric lighting, color temperature [色温]K, [独特色彩方案]

【画质&细节】Digital painting / octane render, highly detailed, matte painting quality, artstation trending

【负面提示词】ugly, deformed, realistic photo, boring, mundane, everyday, plain, low quality, amateur, blurry
```

**示例（赛博朋克城市）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, concept art, --ar 21:9 --style expressive --s 300 --q 2

【核心主体】Futuristic cyberpunk city, towering megastructures with holographic advertisements, flying vehicles between buildings, neon-lit streets below

【场景环境】Volumetric fog and rain, multiple neon light sources, holographic billboards, wet reflective surfaces, steam rising from street level

【风格&美学】Cyberpunk, blade runner aesthetic, concept art, epic scale, imaginative world building, dystopian future

【光影&色彩】Neon signs (pink, cyan, purple), dramatic atmospheric lighting, color temperature 8000K with neon accents, high contrast dark shadows

【画质&细节】Octane render, highly detailed, matte painting quality, artstation trending, ray traced reflections

【负面提示词】ugly, deformed, realistic photo, boring, mundane, everyday, plain, low quality, amateur, blurry
```

---

## 🛍️ 三、产品类模板

### 3.1 商业产品（3C/美妆/食品）

**适用场景：** 电商主图、产品广告、品牌宣传

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, commercial product photography, --ar [比例] --style raw --s 200 --q 2

【核心主体】[产品名称], [颜色], [材质], [摆放角度], [状态：打开/关闭/使用中]

【场景环境】[背景：纯色/渐变/场景], [道具元素], [装饰：花瓣/水珠/烟雾]

【风格&美学】High-end commercial photography, [品牌调性], clean composition, premium aesthetic

【光影&色彩】[布光方案], color temperature [色温]K, [色彩方案], product-focused lighting

【画质&细节】Phase One XF IQ4, [镜头]mm macro, f/[光圈], razor sharp focus, hyper-detailed texture, octane render

【负面提示词】ugly, deformed, blurry, noisy, text, watermark, logo, signature, overexposed, underexposed, plastic look, cheap appearance
```

**示例（高端手表）：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, commercial product photography, --ar 1:1 --style raw --s 200 --q 2

【核心主体】Luxury Swiss mechanical watch, silver stainless steel case, black leather strap, 45-degree angle display, watch face showing 10:10 position

【场景环境】Dark gradient background, subtle spotlight on product, floating watch particles, premium presentation

【风格&美学】High-end commercial photography, luxury brand aesthetic, clean composition, premium aesthetic, sophisticated

【光影&色彩】Three-point studio lighting with softbox, color temperature 5500K, cool metallic tones with warm leather accents, rim lighting for contour

【画质&细节】Phase One XF IQ4, 100mm macro lens, f/11, razor sharp focus on watch face, hyper-detailed texture, octane render

【负面提示词】ugly, deformed, blurry, noisy, text, watermark, logo, signature, overexposed, underexposed, plastic look, cheap appearance
```

---

### 3.2 概念设计（工业/建筑/服装）

**适用场景：** 产品设计、建筑设计、服装设计

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, concept design render, --ar 16:9 --style [风格] --s [强度] --q 2

【核心主体】[设计对象], [设计风格], [材质说明], [功能特征], [创新点]

【场景环境】[展示环境：展厅/户外/抽象], [背景处理], [辅助元素]

【风格&美学】[风格：包豪斯/未来主义/极简], industrial design, functional aesthetic, innovative

【光影&色彩】[布光], color temperature [色温]K, [色彩方案], design-focused lighting

【画质&细节】Keyshot / octane render, photorealistic, product visualization quality, technical accuracy

【负面提示词】ugly, deformed, unrealistic, impractical, poorly designed, amateur, low quality, blurry
```

---

### 3.3 品牌视觉（LOGO/海报/包装）

**适用场景：** 品牌设计、营销物料、视觉识别

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, brand visual design, --ar [比例] --style [风格] --s [强度] --q 2

【核心主体】[设计类型：LOGO/海报/包装], [品牌名称/行业], [核心图形], [文字排版]

【场景环境】[展示方式：mockup/flat/3D], [背景], [道具]

【风格&美学】[风格], brand identity design, professional, on-brand

【光影&色彩】[布光/处理], color temperature [色温]K, [品牌色], consistent color system

【画质&细节】Vector quality / high resolution, print ready, professional design standard

【负面提示词】ugly, deformed, amateur, unprofessional, clipart, generic, template, low quality, blurry
```

---

## ✨ 四、特殊类模板

### 4.1 抽象艺术

**适用场景：** 艺术创作、背景素材、创意表达

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, abstract art, --ar [比例] --style expressive --s [强度] --q 2

【核心主体】[抽象主题：情感/概念/音乐], [视觉元素：形状/线条/色彩]

【场景环境】Non-representational composition, [元素关系], [空间处理]

【风格&美学】[流派：抽象表现主义/构成主义/色域绘画], abstract art, expressive, conceptual

【光影&色彩】[色彩关系], [对比度], [色彩情绪]

【画质&细节】[技法：厚涂/泼洒/渐变], high resolution, gallery quality

【负面提示词】ugly, deformed, representational, realistic, literal, figurative, low quality, amateur
```

---

### 4.2 文字排版

**适用场景：** 海报文字、标题设计、文字效果

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, typography design, --ar [比例] --style [风格] --s [强度] --q 2

【核心主体】Text "[文字内容]", [字体风格], [文字效果：3D/金属/发光], [排版方式]

【场景环境】[背景处理], [装饰元素], [空间关系]

【风格&美学】[风格], typography design, graphic design, professional

【光影&色彩】[光源], color temperature [色温]K, [色彩方案]

【画质&细节】Vector quality, crisp edges, print ready, high resolution

【负面提示词】ugly, deformed, misspelled, distorted letters, illegible, amateur, low quality, blurry
```

---

### 4.3 特效合成

**适用场景：** 视觉特效、创意合成、超现实场景

**模板结构：**
```
NanobananaPro dedicated image generation, (ultra-high quality:1.4), (masterpiece:1.3), 8K UHD, visual effects composite, --ar [比例] --style expressive --s [强度] --q 2

【核心主体】[主体元素], [特效类型：粒子/流体/光效/爆炸], [合成方式]

【场景环境】[背景], [氛围元素], [层次关系]

【风格&美学】[风格], visual effects, cinematic composite, dramatic

【光影&色彩】[光源匹配], color temperature [色温]K, [色彩分级]

【画质&细节】Octane render / after effects quality, photorealistic composite, seamless integration

【负面提示词】ugly, deformed, poorly composited, mismatched lighting, fake looking, amateur, low quality, blurry
```

---

## 🎯 模板使用指南

### 快速选择表

| 需求类型 | 推荐模板 | 关键变量 |
|----------|----------|----------|
| 个人写真 | 1.1 人像写真 | 人物描述、光影、背景 |
| 游戏角色 | 1.2 角色设计 | 外貌、服装、风格 |
| 运动场景 | 1.3 动作姿态 | 动作、动态元素 |
| 室内设计 | 2.1 室内场景 | 空间、风格、家具 |
| 城市风光 | 2.2 室外场景 | 时间、天气、构图 |
| 概念艺术 | 2.3 幻想场景 | 世界观、特效 |
| 电商产品 | 3.1 商业产品 | 产品、材质、布光 |
| 工业设计 | 3.2 概念设计 | 设计、材质、功能 |
| 品牌设计 | 3.3 品牌视觉 | 品牌色、风格 |
| 艺术创作 | 4.1 抽象艺术 | 主题、色彩、技法 |

### 变量替换原则

1. **具体化** - 避免模糊词汇
   - ❌ "漂亮的衣服" → ✅ "红色丝绸晚礼服"
   - ❌ "好看的背景" → ✅ "渐变紫色背景"

2. **参数化** - 使用可量化描述
   - ❌ "温暖的光" → ✅ "color temperature 3200K"
   - ❌ "大光圈" → ✅ "f/2.8"

3. **专业化** - 使用行业术语
   - ❌ "侧面光" → ✅ "rim lighting from side"
   - ❌ "模糊背景" → ✅ "bokeh background"

---

**模板库版本：v1.0 | 模板数量：15+ | 更新日期：2026-04-03**
