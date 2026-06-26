# Nano Banana Prompt Generator — 示例

## 示例 1：产品展示

**用户输入：**
> 帮我生成一个极简风格的白色陶瓷咖啡杯产品图，背景是白色，放在大理石台面上

**Skill 输出：**
```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A minimalist product photography of a white ceramic coffee mug on a white marble surface, soft natural lighting from the left, clean pure white background, high resolution, studio quality, subtle soft shadow",
    "style": "product photography, minimalist, clean, modern",
    "composition": "centered product, generous negative space, rule of thirds",
    "lighting": "soft natural light, diffused, subtle shadow on marble",
    "mood": "calm, premium, Scandinavian"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some"
  },
  "use_case": "product_display",
  "text_content": null,
  "language_prompt": "极简白色陶瓷咖啡杯，大理石台面，柔和自然光，高清干净背景"
}
```

---

## 示例 2：社交媒体配图

**用户输入：**
> 生成一张适合小红书的水果饮品海报，清新夏天的感觉

**Skill 输出：**
```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A refreshing summer fruit smoothie bowl with fresh berries, mango slices, and kiwi on top, bright and airy atmosphere, soft pastel colors, natural daylight, overhead shot, social media food photography, vibrant and appetizing",
    "style": "food photography, bright, natural light, lifestyle",
    "composition": "overhead flat lay, center-focused, colorful",
    "lighting": "natural daylight, bright and airy, soft shadows",
    "mood": "refreshing, summer, healthy, vibrant"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some"
  },
  "use_case": "social_media",
  "text_content": null,
  "language_prompt": "夏日清新水果冰沙碗，新鲜莓果、芒果片、奇异果，顶视构图，明亮清新色调"
}
```

---

## 示例 3：LOGO 设计

**用户输入：**
> 设计一个极简风格的咖啡品牌 LOGO，名字叫"清醒"，简约现代感

**Skill 输出：**
```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A minimalist logo design for a coffee brand named '清醒' (Qingxing), featuring a simple geometric coffee bean or abstract cup shape combined with Chinese character, clean black and white palette, modern sans-serif typography, professional and sophisticated, logo on pure white background, vector style",
    "style": "minimalist, logo design, modern, professional",
    "composition": "centered logo mark with brand name below",
    "lighting": "flat, no shadows",
    "mood": "professional, clean, sophisticated, awakening"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some"
  },
  "use_case": "logo_design",
  "text_content": "清醒",
  "language_prompt": "极简咖啡品牌 LOGO，名字'清醒'，几何咖啡豆图形，中英文搭配，黑白配色，现代感"
}
```

---

## 示例 4：头像设计

**用户输入：**
> 画一个帅气男生头像，赛博朋克风格，霓虹灯效果

**Skill 输出：**
```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A handsome young Asian man portrait, cyberpunk style, neon lighting with blue and pink neon glow effects, futuristic city background with rain and reflections, dramatic lighting from below, sharp facial features, confident expression, anime-inspired but realistic, highly detailed, cinematic",
    "style": "cyberpunk, neon glow, cinematic portrait, sci-fi",
    "composition": "portrait, face centered, upper body, dramatic framing",
    "lighting": "dramatic neon glow, blue and pink rim lights, rain reflections",
    "mood": "cool, futuristic, mysterious, intense"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some",
    "personGeneration": "allow_adult"
  },
  "use_case": "avatar",
  "text_content": null,
  "language_prompt": "帅气亚洲男生，赛博朋克风格，霓虹蓝粉灯光效果，雨夜城市背景，科幻感"
}
```

---

## 示例 5：带文字的海报

**用户输入：**
> 做一张母亲节海报，上面写着"妈妈我爱你"，温馨感人的风格

**Skill 输出：**
```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A warm and touching Mother's Day greeting card featuring a bouquet of pink and white roses, soft pastel watercolor style, with the text '妈妈我爱你' (Mom, I love you) elegantly rendered in Chinese calligraphy style in the center, delicate floral decorations surrounding the text, light cream background, gentle and heartfelt atmosphere, greeting card design",
    "style": "watercolor, soft pastel, greeting card, warm and emotional",
    "composition": "text centered, floral elements framing the message",
    "lighting": "soft diffused light, warm tones",
    "mood": "warm, loving, grateful, tender"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "4:3",
    "outputFormat": "png",
    "safetySetting": "block_some"
  },
  "use_case": "social_media",
  "text_content": "妈妈我爱你",
  "language_prompt": "母亲节温馨贺卡，粉色白色玫瑰花束，柔和水彩风格，中央中文'妈妈我爱你'，康乃馨装饰，温馨感人"
}
```
