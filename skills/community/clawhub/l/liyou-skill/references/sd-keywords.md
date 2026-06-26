# SD 关键词模板与优化技巧

**版本：** v0.1.0  
**最后更新：** 2026-03-11

---

## 🎨 基础关键词结构

### 标准格式

```
(质量词：权重), 
主体描述，
外貌特征，
服饰装扮，
场景背景，
光影效果，
构图风格，
额外细节
```

### 权重语法

- `(keyword:1.3)` - 增强权重（1.0 是基准）
- `(keyword:0.8)` - 降低权重
- `[keyword]` - 降低权重（等价于 :0.8）
- `keyword1 AND keyword2` - 同时强调

---

## 🌸 璃幽专属关键词包

### 完整提示词（正面）

```
(masterpiece, best quality, ultra-detailed:1.3), 
(anime style:1.2), 1girl, solo, 
(liyou:1.4), 
(deep purple hair:1.3), (long hair:1.2), (gradient hair:1.3), (silver tips:1.2), 
(heterochromia:1.4), (golden left eye:1.3), (purple-red right eye:1.3), 
(pale skin:1.1), (gentle smile:1.2), (small fangs:1.1), 
(witch outfit:1.3), (dark purple dress:1.2), (moon pattern:1.2), 
(magic pendant:1.2), 
(fantasy background:1.1), (dimensional shop:1.1), 
(soft lighting:1.2), (cinematic composition:1.2), 
(depth of field:1.1), (bokeh:1.1), 
(glowing particles:1.1), (magical aura:1.1)
```

### 负面提示词

```
(worst quality, low quality:1.4), 
(normal quality:1.3), 
bad anatomy, bad hands, bad feet, 
text, watermark, signature, username, 
blurry, jpeg artifacts, 
ugly, deformed, extra limbs, missing limbs, 
mutated hands, poorly drawn hands, 
poorly drawn face, mutation, 
disfigured, gross proportions, 
malformed limbs, fused fingers, 
too many fingers, long neck, 
cartoon, 3d, cgi, render, 
sketch, crayon, graphite, 
realistic, photorealistic
```

---

## 🎭 表情与姿态关键词

### 表情库

| 表情 | 关键词 |
|------|--------|
| 温柔微笑 | gentle smile, kind eyes, warm expression |
| 认真倾听 | focused expression, tilted head, attentive eyes |
| 小傲娇 | looking away, blushing ears, pout |
| 慵懒发呆 | lying on counter, resting chin on hand, drowsy eyes |
| 调皮眨眼 | wink, playful smile, showing fangs |
| 担忧关切 | concerned expression, furrowed brow, gentle eyes |
| 开心笑 | bright smile, sparkling eyes, happy |
| 思考状 | thinking pose, finger on chin, looking up |

### 姿态库

| 姿态 | 关键词 |
|------|--------|
| 站立接待 | standing, hands folded, slight bow |
| 吧台工作 | behind counter, mixing potion, focused |
| 慵懒趴着 | lying on counter, propped on elbow, relaxed |
| 思考 | thinking pose, hand on chin |
| 施法 | casting spell, hands raised, glowing palms |
| 行走 | walking, dynamic pose, flowing hair |
| 坐姿 | sitting, crossed legs, elegant |
| 欢迎手势 | welcoming gesture, open arms, smile |

---

## 🏰 场景关键词库

### 店内场景

```
(dimensional shop interior:1.3), 
(wooden counter:1.2), (shelves with potions:1.2), 
(floating candles:1.1), (magical items:1.1), 
(cozy atmosphere:1.2), (warm lighting:1.2), 
(cluttered but organized:1.1), (mystic ambiance:1.2)
```

### 室外场景

```
(fantasy town street:1.2), 
(cobblestone road:1.1), (medieval buildings:1.1), 
(magical marketplace:1.2), (floating lanterns:1.1), 
(twilight sky:1.2), (starlit night:1.1), 
(enchanting atmosphere:1.2)
```

### 特殊场景

```
(dimensional rift:1.3), 
(swirling colors:1.2), (portal:1.2), 
(ethereal space:1.2), (dreamlike:1.2), 
(surreal background:1.2), (abstract:1.1)
```

---

## ✨ 特效与氛围

### 魔法特效

- `glowing particles` - 发光粒子
- `magical aura` - 魔法光环
- `sparkling light` - 闪烁光芒
- `energy waves` - 能量波纹
- `runes floating` - 漂浮符文
- `potion steam` - 药水蒸汽
- `crystal shards` - 水晶碎片

### 光影效果

- `soft lighting` - 柔光
- `cinematic lighting` - 电影级布光
- `volumetric lighting` - 体积光
- `rim light` - 轮廓光
- `subsurface scattering` - 次表面散射
- `god rays` - 耶稣光
- `ambient occlusion` - 环境光遮蔽

### 氛围词

- `healing vibe` - 治愈氛围
- `mysterious` - 神秘
- `ethereal` - 空灵
- `cozy` - 温馨
- `melancholic` - 忧郁
- `hopeful` - 充满希望
- `dreamy` - 梦幻

---

## 🎨 风格关键词

### 动漫风格

- `anime style` - 动漫风格
- `cel shading` - 卡通渲染
- `vibrant colors` - 鲜艳色彩
- `clean lines` - 干净线条
- `detailed eyes` - 细节眼睛

### 艺术风格

- `digital painting` - 数字绘画
- `concept art` - 概念艺术
- `illustration` - 插画
- `character sheet` - 角色设定图
- `key visual` - 主视觉图

### 质量词

- `masterpiece` - 杰作
- `best quality` - 最佳质量
- `ultra-detailed` - 超细节
- `high resolution` - 高分辨率
- `8k` - 8K 分辨率

---

## 🔧 实用技巧

### 1. 角色一致性

使用 `(liyou:1.4)` 这样的专属标签，配合详细描述，确保多张图角色一致。

### 2. 构图控制

- `close-up` - 特写
- `upper body` - 上半身
- `full body` - 全身
- `from above` - 俯视
- `from below` - 仰视
- `dutch angle` - 倾斜角度

### 3. 色彩控制

- `purple theme` - 紫色主题
- `cool colors` - 冷色调
- `warm colors` - 暖色调
- `high contrast` - 高对比
- `pastel colors` - 柔和色彩

### 4. 迭代优化

如果生成效果不理想：
1. 增加关键特征的权重
2. 调整负面提示词
3. 简化描述，避免冲突
4. 尝试不同的 seed

---

## 📝 常用组合示例

### 示例 1：璃幽接待客人

```
(masterpiece, best quality:1.3), 
1girl, liyou, gentle smile, 
behind counter, welcoming gesture, 
customer in foreground (back view), 
dimensional shop interior, 
soft lighting, warm atmosphere
```

### 示例 2：璃幽调配药水

```
(masterpiece, best quality:1.3), 
1girl, liyou, focused expression, 
mixing potion, glowing liquid, 
test tubes, magical items, 
close-up on hands, 
magical aura, sparkling particles
```

### 示例 3：璃幽慵懒日常

```
(masterpiece, best quality:1.3), 
1girl, liyou, lying on counter, 
propped on elbow, drowsy eyes, 
relaxed pose, casual, 
cozy shop interior, 
afternoon light, peaceful
```

---

## 📚 学习资源

- **Civitai** - 模型与提示词分享
- **Danbooru** - 标签参考
- **PromptHero** - 提示词搜索引擎
- **Stable Diffusion 官方文档**

---

_「关键词就像魔法咒语，用心组合才能召唤出最美的画面～」_  
_—— 璃幽 🌸_
