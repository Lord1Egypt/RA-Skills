# Stable Diffusion / ComfyUI 提示词格式参考

## 基本结构

```
正面提示词：
masterpiece, best quality, [主体], [场景], [风格], [光照], [细节], [技术参数]

负面提示词：
low quality, worst quality, blurry, watermark, text, signature, extra limbs, deformed, bad anatomy
```

## 提示词权重语法

| 语法 | 说明 | 示例 |
|---|---|---|
| `(word)` | 加权 x1.1 | `(cat)` = 猫的权重提升 |
| `(word:1.5)` | 显式权重数值 | `(cat:1.5)` |
| `[word]` | 降低权重 | `[cat]` |
| `word::0.5` | 步进衰减 | 逐步衰减效果 |

## 常用质量标签（必加）

```
masterpiece, best quality, high quality, official art, extremely detailed CG unity 8k wallpaper
```

## 常用负面提示词

```
low quality, worst quality, normal quality, blurry, watermark, text, signature
extra fingers, extra limbs, deformed, bad anatomy, mutated hands
bad proportions, gross proportions, malformed limbs
bad hands, missing fingers, fused fingers
bad teeth, bad eyes, bad face
```

## 构图与视角

```
front view, back view, side view
from above, from below, bird's eye view, worm's eye view
wide shot, medium shot, close-up, extreme close-up
dynamic angle, low angle, high angle, Dutch angle
shallow depth of field, bokeh, defocused
full body, half body, portrait, headshot
```

## 光影

```
natural lighting, cinematic lighting
sunlight, moonlight, starlight
soft lighting, hard lighting
dramatic lighting, rim lighting, backlighting
volumetric lighting, god rays
neon glow, light particles
```

## 风格标签参考

| 风格 | 正面标签 | 适用场景 |
|---|---|---|
| 写实 | `photorealistic, realistic, 8k, detailed photograph` | 人物、风景 |
| 动漫 | `anime, 2d, cel shading, vibrant colors` | 二次元 |
| 厚涂 | `oil painting, impasto, painterly` | 艺术感 |
| 赛博朋克 | `cyberpunk, neon, holographic, futuristic` | 科幻场景 |
| 水彩 | `watercolor, soft edges, delicate` | 清新风格 |
| 像素 | `pixel art, 8-bit, retro game` | 游戏风格 |
| 概念艺术 | `concept art, matte painting, artstation` | 设定、场景 |

## ComfyUI 节点建议

- `KSampler`：`denoise: 0.7~0.9`（越高细节越多）
- `KSampler Advanced`：`sigma_start, sigma_end` 控制采样范围
- `ControlNet`：可加 `canny, openpose, depth` 控制构图

## 示例

**输入**：「一只橘猫在咖啡馆窗边晒太阳」

**输出（SD）**：
```
masterpiece, best quality, high quality, an orange tabby cat sitting on a windowsill in a cozy cafe, sunlight streaming through the window, warm tones, soft bokeh background, European cafe interior, morning light, relaxing atmosphere, oil painting style, detailed fur, expressive eyes
Negative: low quality, worst quality, blurry, watermark, text, deformed, bad anatomy, extra limbs
```

## 参考网站

- https://stable-diffusion-art.com/prompts
- https://publicprompts.art
- https://arthub.ai
