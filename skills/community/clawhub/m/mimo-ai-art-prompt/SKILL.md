---
name: ai-art-prompt
version: 1.3.0
description: |
  你心里有一幅画，但写出来的prompt出来的图总是差强人意？把「一个女孩在雨中」变成带光影、构图、风格参数的专业提示词，适配Midjourney/Stable Diffusion/DALL-E/Flux，告别AI出图的「买家秀」时刻。
  触发词：
  - 基础词：MJ提示词、Midjourney、SD提示词、Stable Diffusion、DALL-E、Flux、AI画图、AI绘画、文生图、提示词优化、prompt优化
  - 进阶词：生成图片、帮我画、画一张、绘图、画个、照片转插画、头像生成、壁纸生成、海报设计、插画生成
  - 场景词：古风汉服、赛博朋克、二次元、动漫风、真人转动漫、油画风、水彩画、水墨画、像素风、3D渲染
  - 平台词：--ar参数、--v参数、--s参数、风格化、宽高比
  排除：实际图片生成(只生成提示词)、视频生成、纯文字任务
---

# AI绘画提示词优化器 🎨

## 触发条件判定

### ✅ 触发场景
| 场景 | 触发词示例 |
|------|-----------|
| 明确请求 | "帮我画个xxx"、"生成一张xxx图片"、"写一个MJ提示词" |
| 平台咨询 | "Midjourney怎么用"、"SD提示词怎么写"、"Flux提示词教程" |
| 风格需求 | "想要xxx风格"、"做成xxx画风"、"转成xxx效果" |
| 参数咨询 | "--ar是什么意思"、"怎么设置风格化参数"、"图片比例怎么选" |

### ❌ 排除场景
| 场景 | 排除原因 | 建议替代 |
|------|---------|---------|
| 要求实际生成图片 | 技能只生成提示词 | 建议使用图像生成工具 |
| 视频/动画制作 | 不支持动态内容 | 建议专业视频工具 |
| Logo/海报文字排版 | 纯文字任务 | 建议Canva/Figma |
| 中文描述直接生成 | 中文效果差 | 需翻译优化为英文 |

## 核心流程（8 Steps）

### Step 1: 意图解析与分类
```
输入分析：
- 主体识别：人物/动物/物品/场景/概念
- 动作状态：静态/动态/表情/情绪
- 环境背景：室内/室外/时间/天气/地点
- 风格意向：用户描述的"感觉"提取

输出：
- 主体清单（逗号分隔）
- 环境关键词（3-5个）
- 风格标签（2-3个）
```

### Step 2: 主体细节丰富
**人物类**：
- 面部：眉眼鼻嘴、下巴轮廓、肤色、表情
- 发型：长短、颜色、造型、发质
- 服装：朝代/风格/材质/配色/配饰
- 姿态：站/坐/卧/动态、视线方向

**物品类**：
- 材质：金属/木质/玻璃/布料/透明
- 质感：光滑/粗糙/做旧/全新
- 尺寸/比例

**场景类**：
- 空间：室内/室外/水下/太空
- 光照：自然光/人工光/混合光
- 天气/时间：晴天/雨/夜/晨/暮

### Step 3: 风格映射
| 用户描述 | 风格标签 |
|---------|---------|
| 真实/照片感 | photorealistic, 8k, detailed skin texture |
| 动漫/二次元 | anime style, cel shading, manga |
| 油画/艺术感 | oil painting, impressionist, brush strokes |
| 水彩/清新 | watercolor, soft edges, translucent |
| 3D/CGI | 3d render, Pixar style, octane render |
| 赛博/科技 | cyberpunk, neon, futuristic, holographic |
| 古风/国风 | Chinese hanfu, traditional Chinese art, sumi-e |
| 像素/复古 | pixel art, 8-bit, retro game style |
| 电影感 | cinematic, film grain, movie still |
| 吉卜力 | Studio Ghibli, Hayao Miyazaki |

### Step 4: 构图设计
**景别选择**：
| 景别 | 关键词 | 适用场景 |
|------|--------|---------|
| 特写 | close-up, face focus | 面部/表情/细节 |
| 胸像 | bust portrait, upper body | 上半身/服装 |
| 全身 | full body shot | 完整人物/姿态 |
| 环境人像 | environmental portrait | 人物+场景 |
| 风景 | landscape, scenery | 纯场景 |

**构图法则**：
| 类型 | 关键词 | 效果 |
|------|--------|------|
| 黄金分割 | rule of thirds, golden ratio | 平衡美感 |
| 对称 | symmetrical, centered | 庄重正式 |
| 对角线 | diagonal, leading lines | 动感张力 |
| 俯视 | bird's eye, overhead | 场景全貌 |
| 仰视 | worm's eye, low angle | 气势宏大 |

### Step 5: 光影设计
**光照类型**：
- 自然光：sunlight, golden hour, soft window light
- 人造光：studio light, neon, candle, fairy lights
- 特殊光：rim light, backlight, volumetric light

**氛围表达**：
| 氛围 | 光影关键词 |
|------|-----------|
| 温暖治愈 | warm tones, golden light, soft glow |
| 神秘阴暗 | dramatic shadows, chiaroscuro, low key |
| 梦幻唯美 | ethereal glow, bokeh, dreamy |
| 冷酷科技 | cold blue, harsh light, metallic reflections |
| 复古怀旧 | vintage tones, film grain, warm fade |

### Step 6: 平台适配
**Midjourney**：
```
格式：主体描述, 环境细节, 风格标签, 光照氛围, 构图类型 --ar 16:9 --v 6 --s 250
参数：
  --ar 宽高比：1:1/4:3/16:9/9:16/3:2
  --v 版本：5.2/6/6.1
  --s 风格化：100-1000（默认250）
  --style raw：少风格化，多真实感
  --style cute/expressive：可爱/表现力
  --q 质量：0.25/0.5/1/2
```

**Stable Diffusion**：
```
权重语法：
  (关键词:1.3)  正向权重增强
  [关键词:0.7]  负向权重减弱
  (关键词)      默认权重1.1
  [](套娃)     交替权重

示例：
1girl, long flowing hair, (beautiful face:1.2), detailed eyes:1.1, [weak hands:0.8], soft lighting, moonlight, (masterpiece:1.3), (best quality:1.2), (absurdres:1.1), (8k:1.1), <lora:hanfu_v1:0.8>
```

**DALL-E**：
```
- 自然英文描述即可
- 无需参数语法
- 支持中文但英文效果更稳定
```

**Flux**：
```
- 必须英文
- 避免过长描述（<77 tokens效果更好）
- 可添加 quality/complexity 标签
```

### Step 7: 变体生成
**变体策略**：
| 变体类型 | 策略 | 示例 |
|---------|------|------|
| 风格变体 | 换艺术风格 | 写实→动漫、写实→油画 |
| 构图变体 | 换景别/视角 | 全身→特写、正面→侧面 |
| 氛围变体 | 换光照/色调 | 暖色→冷色、明亮→阴暗 |
| 平台变体 | 适配不同平台 | MJ→SD |

### Step 8: 迭代优化建议
```
💡 迭代检查清单：
□ 主体是否清晰可辨？
□ 风格是否与需求一致？
□ 光影氛围是否到位？
□ 构图是否合理？
□ 是否需要调整权重？
□ 是否有畸形/多手指等问题？

💡 常见调整方向：
- 效果太假 → 添加 "photorealistic, raw photo"
- 风格太强 → 使用 --style raw
- 手部畸形 → 添加 "perfect hands"
- 多人失控 → 改为单人像
```

## 输出模板

````
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 AI绘画提示词 | {平台}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【需求解析】
• 主体：{提取的主体}
• 风格：{映射的风格标签}
• 氛围：{设计的光影氛围}
• 构图：{选择的构图类型}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【主提示词】
{完整优化后的英文提示词}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【参数设置】
| 参数 | 值 | 说明 |
|------|---|-----|
| --ar | {比例} | 宽高比 {比例_desc} |
| --v | {版本} | 版本 {版本_desc} |
| --s | {数值} | 风格化 {数值_desc} |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【变体推荐】

🔹 变体1 - {风格变化}
{提示词变体1}
参数：--ar {比例} --s {数值}

🔹 变体2 - {构图变化}
{提示词变体2}
参数：--ar {比例}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【负向提示词】（Stable Diffusion专用）
low quality, blurry, bad anatomy, distorted face, extra limbs, 
bad hands, missing fingers, deformed, watermark, text, logo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【迭代优化建议】
• 优先调整 {参数} 参数观察效果
• 如需更真实感，添加 {关键词}
• 如需更强风格，尝试 --s {更高数值}
• 避免常见问题：{提醒事项}
````

## 边界约束

### 输入校验
| 校验项 | 要求 | 不符处理 |
|--------|------|---------|
| 内容长度 | ≥5字（中文）或≥3词（英文） | 询问具体画什么 |
| 敏感内容 | 无色情/暴力/政治 | 礼貌拒绝，说明原因 |
| 任务类型 | 图像生成相关 | 建议使用对应工具 |

### 平台选择建议
| 需求 | 推荐平台 |
|------|---------|
| 高质量写实 | Midjourney v6 |
| 精细控制 | Stable Diffusion |
| 快速简单 | DALL-E 3 |
| 动漫风格 | Midjourney + anime风格 / SD |
| 中文优化 | Midjourney + 中文标注 |

### 不支持场景
1. ❌ 实际调用API生成图片
2. ❌ 视频/动画/GIF制作
3. ❌ 纯文字设计（Logo/海报文字排版）
4. ❌ 色情/暴力/政治敏感内容
5. ❌ 图片编辑/修图/放大

## 完整示例

### 示例1：赛博朋克风格美女
```
用户：画一个赛博朋克风格的美女黑客，站在雨夜的城市天际线上

【需求解析】
• 主体：年轻女性，赛博格风格，黑客身份
• 风格：cyberpunk, neon-lit, futuristic
• 氛围：雨夜霓虹，潮湿街道，神秘冷酷
• 构图：全身像，背景城市天际线

【主提示词】
beautiful woman hacker, cyberpunk aesthetic, augmented reality visor, 
tech-enhanced leather jacket with glowing circuit patterns, wet city 
streets reflecting neon lights, futuristic metropolis skyline at night, 
rain effect, dramatic rim lighting, cinematic composition, 8k, 
highly detailed --ar 16:9 --v 6 --s 400 --style raw

【变体1 - 动漫风格】
anime cyberpunk girl, detailed cyberpunk outfit, neon city background, 
dynamic pose, glowing eyes, holographic interface, rain and neon 
reflections, vibrant colors --ar 16:9 --v 6 --s 750

【负向提示词】
low quality, blurry, bad anatomy, distorted face, extra limbs, 
bad hands, missing fingers, deformed, watermark, text
```

### 示例2：中国古风仙侠
```
用户：生成一个白衣仙女的图片，在云雾缭绕的山巅

【需求解析】
• 主体：白衣仙女，飘逸出尘
• 风格：Chinese xianxia, traditional hanfu, ethereal
• 氛围：云雾缭绕，超凡脱俗
• 构图：全身像，仰视视角

【主提示词】
ethereal Chinese fairy, flowing white hanfu with embroidery, long 
black hair blowing in wind, standing on misty mountain peak, floating 
clouds, sunrise glow, traditional Chinese aesthetic, celestial 
atmosphere, soft sunlight, cinematic composition, traditional 
sumi-e style influence --ar 3:4 --v 6 --style raw

【变体1 - 正面特写】
beautiful Chinese goddess, white flowing dress, serene expression, 
detailed face with delicate features, morning mist, soft golden 
light, upper body portrait, traditional Chinese painting style 
--ar 4:5 --v 6 --s 200
```

## 参考资源

更多风格库、构图方案、参数详解见 references/details.md
