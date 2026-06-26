# 图片风格预设库

## 风格速查表

| 风格代号 | 风格名称 | 适用场景 | 核心关键词 |
|----------|----------|----------|------------|
| flat | 扁平插画 | 科技、商业、教程 | flat illustration, minimal, vector style |
| watercolor | 水彩风格 | 情感、文艺、生活 | watercolor painting, soft edges, dreamy |
| cartoon | 卡通风格 | 轻松、幽默、儿童 | cartoon style, bold outlines, vibrant colors |
| chinese | 国风水墨 | 传统文化、古典 | Chinese ink painting, traditional, elegant |
| tech | 科技感 | AI、数据、未来 | futuristic, neon, digital art, cyberpunk |
| minimal | 极简线条 | 高端、简约、商务 | minimalist, line art, white space |

---

## 风格详细说明

### 1. 扁平插画 (flat)

**核心提示词**：
```
flat illustration, vector style, minimal design, clean lines, 
solid colors, no shadows, modern, geometric shapes
```

**色调变体**：
- 暖色调：warm color palette, orange and yellow tones
- 冷色调：cool color palette, blue and green tones
- 莫兰迪：muted colors, morandi palette, soft tones

**适用文章类型**：科技资讯、产品介绍、教程指南、商业分析

---

### 2. 水彩风格 (watercolor)

**核心提示词**：
```
watercolor painting, soft edges, flowing colors, 
paper texture, artistic, dreamy atmosphere, hand-painted feel
```

**氛围变体**：
- 清新：light watercolor, pastel colors, airy
- 浓郁：rich watercolor, deep colors, expressive
- 留白：watercolor with white space, minimal strokes

**适用文章类型**：情感散文、生活随笔、旅行游记、文艺评论

---

### 3. 卡通风格 (cartoon)

**核心提示词**：
```
cartoon style, bold outlines, vibrant colors, 
exaggerated features, playful, fun, animated look
```

**细分风格**：
- 日系：anime style, Japanese animation
- 美系：American cartoon, Disney style
- 简笔画：simple cartoon, doodle style

**适用文章类型**：趣味科普、亲子内容、轻松话题、幽默杂文

---

### 4. 国风水墨 (chinese)

**核心提示词**：
```
Chinese ink painting, traditional brush strokes, 
rice paper texture, elegant, oriental aesthetic, 
black ink with subtle colors
```

**题材变体**：
- 山水：landscape, mountains and water
- 花鸟：flowers and birds, botanical
- 人物：figure painting, traditional costume

**适用文章类型**：传统文化、历史故事、古典文学、东方美学

---

### 5. 科技感 (tech)

**核心提示词**：
```
futuristic, digital art, neon lights, 
holographic, cyber, high-tech, glowing elements
```

**氛围变体**：
- 赛博朋克：cyberpunk, dark background, neon pink and blue
- 干净科技：clean tech, white and blue, minimalist futuristic
- 数据可视化：data visualization, abstract, flowing lines

**适用文章类型**：AI科技、互联网趋势、未来展望、数字化转型

---

### 6. 极简线条 (minimal)

**核心提示词**：
```
minimalist, line art, simple strokes, 
white background, elegant, sophisticated, 
negative space, single color accent
```

**变体**：
- 单线条：single line drawing, continuous line
- 几何：geometric minimal, abstract shapes
- 留白：lots of white space, zen aesthetic

**适用文章类型**：高端品牌、设计评论、简约生活、商务内容

---

## 图片比例参考

| 用途 | 比例 | 提示词参数 |
|------|------|------------|
| 公众号封面 | 2.35:1 | --ar 2.35:1 或 aspect ratio 2.35:1 |
| 公众号内文 | 16:9 | --ar 16:9 |
| 小红书配图 | 3:4 | --ar 3:4 |
| 正方形 | 1:1 | --ar 1:1 |
| 手机壁纸 | 9:16 | --ar 9:16 |

---

## 提示词组装模板

```
[主体], [场景], [风格关键词], [色调], [光线], [比例], no text, no letters, no words
```

**必须包含**：
- `no text, no letters, no words` — 避免图片中出现文字

**完整示例**：
```
A young entrepreneur working late at night in a small office, 
warm lamplight, coffee cups on desk, 
flat illustration style, warm color palette, 
soft ambient lighting, 16:9 aspect ratio, no text, no letters, no words
```

---

## 人物一致性处理

当文章中多次出现同一人物时，需保持角色外观一致：

**方法1：详细描述锚定**
```
首次出现时详细描述人物特征：
a young woman with short black hair, wearing a blue blazer, 
round glasses, confident expression

后续图片沿用相同描述
```

**方法2：角色标签**
```
在每个提示词中使用相同的角色描述前缀：
[Character: young Asian woman, short hair, blue blazer] + [具体场景]
```

**注意**：AI生图对人物一致性支持有限，建议：
- 保持相同的服装、发型、配饰描述
- 使用相同的风格关键词
- 必要时可接受轻微差异
