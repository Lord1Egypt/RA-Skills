# DALL-E 3 提示词格式参考

## 基本信息

DALL-E 3 是 OpenAI 的图像生成模型，通过 ` dall-e-3` 模型名调用。仅支持英文提示词，对自然语言理解很强。

## 调用方式

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "your detailed prompt in English",
    "n": 1,
    "size": "1024x1024",
    "style": "vivid",
    "quality": "standard"
  }'
```

## 核心参数

| 参数 | 说明 | 可选值 |
|---|---|---|
| `n` | 生成数量（1~10） | 1（dall-e-3 默认） |
| `size` | 图片尺寸 | `1024x1024`, `1024x1792`, `1792x1024` |
| `style` | 风格 | `vivid`（默认）/ `natural` |
| `quality` | 质量 | `standard`（默认）/ `hd`（更高细节） |
| `response_format` | 返回格式 | `url` / `b64_json` |

## 提示词特点

DALL-E 3 **不需要负面提示词**（系统会自动避免生成不合适内容）。

### 写作原则

1. **用自然句子描述**，不需要标签堆叠
2. **场景要具体**：地点、光照、天气、情绪都要写
3. **人物要描述外貌+服装+动作**
4. **风格放在句子最后**：如 `in the style of...` 或 `photorealistic, ...`

### 结构模板

```
[主体：谁/什么] + [动作/状态] + [场景：地点/环境/背景] + [光照/时间] + [风格/媒介]
```

## 风格关键词

| 风格 | 英文表达 |
|---|---|
| 摄影 | `photorealistic`, `shot on 35mm`, `cinematic photography` |
| 插画 | `digital illustration`, `children's book illustration` |
| 油画 | `oil painting`, `impasto` |
| 水彩 | `watercolor painting` |
| 宫崎骏 | `in the style of Studio Ghibli, Hayao Miyazaki` |
| 皮克斯 | `3D render, Pixar style` |
| 电影感 | `cinematic, film still, widescreen aspect ratio` |
| 广告 | `advertising photography, commercial, product shot` |

## 分辨率选择

| 尺寸 | 比例 | 最佳用途 |
|---|---|---|
| `1024x1024` | 1:1 | 方形构图、头像、方形海报 |
| `1024x1792` | 9:16 | 手机壁纸、Instagram Stories |
| `1792x1024` | 16:9 | 横版海报、Banner、电影感场景 |

## HD 模式特点

`quality: "hd"` 会：
- 更多细节和纹理
- 更准确的构图
- 更强的光照效果
- 但生成速度更慢，成本更高

## 常见错误

1. **文字渲染**：DALL-E 3 对图片内文字支持较好，但仍然不稳定，避免长段落文字
2. **人脸**：默认已经很少出现扭曲人脸，不需要额外说明
3. **中文提示词**：不支持，请确保输入为英文

## 示例

**输入**：「咖啡馆里认真看书的女孩，窗外是巴黎街道，阳光明媚」

**输出（DALL-E 3）**：
```
A young woman reading a book in a cozy Parisian cafe, warm sunlight streaming through the window, a view of the bustling Paris street outside, brass fixtures and wooden tables, relaxed and contemplative mood, soft bokeh, cinematic composition, shot on 35mm film, natural lighting, advertisement photography style
```

**输入**：「梵高风格的星空下向日葵花田」

**输出（DALL-E 3）**：
```
A field of sunflowers under a starry night sky, swirling Milky Way galaxy visible above, thick impasto brushstrokes visible in the sky, vivid blues and yellows, Van Gogh's post-impressionist style, dramatic and emotional, oil painting texture, wide landscape composition
```

## 参考

- https://platform.openai.com/docs/guides/images
- https://platform.openai.com/docs/api-reference/images-create
