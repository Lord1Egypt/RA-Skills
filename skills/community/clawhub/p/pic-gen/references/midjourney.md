# Midjourney 提示词格式参考

## 基本结构

```
[主体描述], [场景], [风格], [光照], [色调], [构图], [参数]
```

## 常用参数

| 参数 | 说明 | 示例值 |
|---|---|---|
| `--ar 16:9` | 宽高比 | `--ar 16:9`, `--ar 1:1`, `--ar 9:16` |
| `--s 250` | 风格化强度 | `--s 100`（低）~ `--s 1000`（高） |
| `--q .25` | 质量（渲染时间） | `--q .25`（快）~ `--q 2`（慢） |
| `--v 6` | 版本 | `--v 6`, `--v 5.2`, `--v niji` |
| `--style` | 风格切换 | `--style raw`（原始） |
| `--no` | 负向词 | `--no people, text, watermark` |
| `--seed` | 种子数 | `--seed 12345` |
| `--tile` | 重复平铺 | `--tile` |
| `--chaos 20` | 变化程度 | `--chaos 0`~`--chaos 100` |

## 风格关键词

### 艺术家风格
- `by Greg Rutkowski`（魔幻写实）
- `by Studio Ghibli`（吉卜力）
- `by Pixar`（皮克斯）
- `by Van Gogh`（梵高）
- `by Makoto Shinkai`（新海诚）
- `by Wes Anderson`（韦斯·安德森）

### 渲染风格
- `photorealistic, 8k, high detail`
- `digital painting, concept art`
- `oil painting, masterpiece`
- `anime style, cel shading`
- `3d render, octane render`
- `watercolor style`

### 光影
- `cinematic lighting`
- `golden hour, warm tones`
- `neon lighting, cyberpunk`
- `soft diffused light`
- `dramatic rim lighting`
- `backlit, silhouette`

## 负面提示词模板

```
--no people, human, text, watermark, signature, low quality, blurry, distorted, deformed, extra limbs, bad anatomy
```

## 示例

**输入**：「赛博朋克城市，雨夜，霓虹灯」

**输出**：
```
a futuristic cyberpunk city at night, heavy rain, neon signs reflecting on wet streets, flying cars, dense fog, cinematic lighting, blade runner atmosphere, --ar 16:9 --s 400 --v 6 --no people, text, watermark
```

## 提示词顺序原则

1. 主体最先（猫、人物、风景）
2. 环境/背景其次
3. 光照和色调
4. 风格和艺术家引用
5. 技术参数最后
6. 负面词单独一行

## 参考网站

- https://docs.midjourney.com/docs/parameter-simplified
- https://promptguide.com/midjourney
