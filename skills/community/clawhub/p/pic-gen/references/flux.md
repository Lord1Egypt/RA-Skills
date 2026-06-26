# Flux 提示词格式参考

## 基本信息

Flux 是 Black Forest Labs 发布的开源图像生成模型，在 Banana、Replicate 等平台托管。

## 平台调用

Banana：
```bash
curl -X POST https://api.banana.dev/start/fetch/v4/{your-model-key} \
  -H "Content-Type: application/json" \
  -d '{
    "modelInputs": {
      "prompt": "your prompt here",
      "num_inference_steps": 50,
      "guidance": 3.5,
      "width": 1024,
      "height": 1024,
      "seed": -1
    }
  }'
```

## 提示词风格

Flux 对提示词的**理解更接近自然语言**，不需要像 Stable Diffusion 那样堆标签，但以下结构仍然最优：

```
[主体] in [场景/环境], [风格描述], [光线描述], [氛围/情绪]
```

### 推荐写法

**✅ 好的示例**：
```
A golden retriever running on a beach at sunset, warm orange light reflecting on the water, cinematic, photorealistic
```

**❌ 过度标签化的示例（Flux 不需要）**：
```
masterpiece, best quality, high quality, golden retriever, beach, sunset, warm tones, cinematic lighting, (perfect fur:1.2)
```

## 关键参数

| 参数 | 说明 | 推荐值 |
|---|---|---|
| `num_inference_steps` | 推理步数，越高质量越好 | 50（默认） |
| `guidance` | 提示词引导强度 | 3.5 |
| `seed` | 随机种子，`-1` 为随机 | -1 或固定值 |
| `width/height` | 图片尺寸 | 1024x1024 |

## Flux 特色能力

- **强提示词跟随**：提示词中写什么基本就会生成什么
- **文字渲染**：Flux-dev 支持图片内文字生成（需准确写出）
- **构图控制**：Flux 对镜头语言理解好，可以写 `wide angle lens`, `close-up on face` 等
- **长提示词**：Flux 不怕长提示词，可以写得很详细

## 镜头语言参考

```
wide shot, medium shot, close-up, extreme close-up
low angle, high angle, bird's eye view, worm's eye view
shallow depth of field, bokeh background, sharp focus
cinematic framing, film grain, vintage tone
```

## 光照描述

```
natural sunlight, golden hour, blue hour
studio lighting, soft box, rim light
neon light, volumetric lighting, god rays
backlit, silhouette, dramatic shadows
```

## 示例

**输入**：「未来城市，雨夜，霓虹灯倒映水面」

**输出（Flux）**：
```
A futuristic cyberpunk cityscape at night, heavy rain falling on the streets, neon signs with Chinese and English text reflected in puddles of water, flying vehicles in the distance, dense fog, volumetric lighting, cinematic, Blade Runner atmosphere, 8k photorealistic
```

## 分辨率建议

- `1024x1024`（方形，默认）
- `1024x768`（横向）
- `768x1024`（纵向）
- `1440x720`（宽屏）
- Banana 最高支持 `2048x2048`

## 参考

- https://blackforestlabs.ai/flux/
- https://docs.banana.dev/banana-docs
