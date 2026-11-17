# Local Image Upscaler / 本地图像增强工具

## 中文

### 简介

Local Image Upscaler 是一个面向 macOS 和 Windows x64 的本地图像增强 Skill。它可以使用本地 AI 模型放大图片、按指定分辨率输出、将图片压缩到目标体积，并在处理前检查图片信息。图片不会上传到云端，源文件默认不会被覆盖。

### 主要功能

- AI 高保真放大，适合照片、截图和 AI 生成图片
- 根据图片自动推荐算法，也可由用户选择默认、快速、照片、人像、插画或锐利细节模式
- 每种算法在下载前说明优点、缺点和新增空间，模型按需下载
- `1K`、`2K`、`4K`、`8K` 分辨率预设
- 自定义长边尺寸，不拉伸原图
- 原生 4× 放大
- 严格控制目标体积，例如将约 1MB 图片压缩到 200KB 以内
- 压缩时优先保留尺寸和画质，必要时才等比例缩小
- 单张图片与文件夹批量处理
- 图片尺寸、比例、像素和体积检查
- macOS 与 Windows x64 支持
- 国内网络镜像回退、离线缓存和 SHA-256 完整性校验

### 支持格式

- 输入：JPG、JPEG、PNG、WebP
- 放大输出：PNG、JPG、WebP（WebP 精确尺寸存在平台限制）
- 目标体积压缩输出：JPEG

### 算法怎么选

如果用户没有指定，Skill 会先观察图片并推荐模式；用户不想选择时使用保守的默认模式。人脸生成式修复不会自动开启。

| 模式 | 适合 | 优点 | 缺点 | 首次下载 |
| --- | --- | --- | --- | ---: |
| `default` | 类型不确定或混合图片 | 均衡、保守 | 不追求最强锐度 | 约 32MB |
| `fast` | 预览、批处理、低配置设备 | 最快、最小 | 细节重建较弱 | 约 2.5MB |
| `photo` | 自然照片 | 质感和明暗过渡自然 | 硬边不如锐利模式 | 约 32MB |
| `portrait` | 有噪点、压缩或较粗糙的真实人像 | 不替换五官，过渡更柔和 | 会抹掉清晰AI人像的部分皮肤细节 | 与照片模式共用 |
| `digital-art` | 动漫、插画、图标 | 线条干净、模型小 | 可能简化照片纹理 | 约 8.6MB |
| `sharp` | 建筑、商品、游戏素材 | 视觉锐度最强 | 可能放大噪点、光晕和皮肤纹理 | 约 32MB |

查看模型、缓存状态和增量下载空间，不会安装任何内容：

```bash
python scripts/setup.py --list-models
```

不要仅因为画面中有人就选择人像模式：清晰AI人像和棚拍头像优先用 `default`；只有真实人像存在噪点、压缩或纹理粗糙时才推荐 `portrait`。

### 准备运行环境

进入 Skill 目录后运行：

```bash
python scripts/setup.py --model high-fidelity
```

快速预览或低配置设备可以使用轻量模型：

```bash
python scripts/setup.py --model lite
```

也可以只准备选中的模式：

```bash
python scripts/setup.py --profile photo
python scripts/setup.py --profile digital-art
python scripts/setup.py --profile sharp
```

首次运行会下载固定版本的 Upscayl NCNN 运行时和模型，并进行 SHA-256 校验。每次执行放大前还会重新校验缓存中的可执行文件和所选模型，后续可以安全地离线复用缓存。

### 放大到指定分辨率

```bash
python scripts/upscale.py input.png --target 1k
python scripts/upscale.py input.png --target 2k
python scripts/upscale.py input.png --target 4k
python scripts/upscale.py input.png --target 8k --tile 256
```

指定算法模式：

```bash
python scripts/upscale.py input.png --target 4k --profile portrait
python scripts/upscale.py input.png --target 4k --profile digital-art
python scripts/upscale.py input.png --target 4k --profile sharp
```

分辨率预设指图片长边：

- 1K：1920 像素
- 2K：2560 像素
- 4K：3840 像素
- 8K：7680 像素

原图比例始终保留。例如，16:9 图片输出为 4K 时是 3840×2160；正方形图片则是 3840×3840。

自定义长边：

```bash
python scripts/upscale.py input.png --max-edge 3000
```

保留模型原生 4×结果：

```bash
python scripts/upscale.py input.png --target scale4
```

### 压缩到目标体积

将图片压缩到不超过 200KB：

```bash
python scripts/compress.py input.png --output output.jpg --target-kb 200
```

将图片压缩到不超过 1.5MB：

```bash
python scripts/compress.py input.png --target-mb 1.5
```

只调整质量，不允许降低尺寸：

```bash
python scripts/compress.py input.png --target-kb 200 --keep-dimensions
```

如果保持原尺寸无法达到目标体积，命令会直接报错。

### 批量处理

批量放大：

```bash
python scripts/upscale.py input-folder --output output-folder --target 4k
```

批量压缩，包括子目录：

```bash
python scripts/compress.py input-folder --output output-folder --target-kb 200 --recursive
```

先预览批量任务，不写入文件：

```bash
python scripts/compress.py input-folder --output output-folder --target-kb 200 --recursive --dry-run
```

### 检查图片信息

```bash
python scripts/inspect.py input.png
python scripts/inspect.py input-folder --recursive --json
```

检查结果包括尺寸、宽高比、百万像素和文件体积。

### 国内镜像与离线模式

可以通过环境变量指定一个或多个镜像前缀：

```bash
IMAGE_UPSCALER_MIRRORS="https://mirror.example/proxy/" python scripts/setup.py
```

即使使用镜像或自定义缓存目录，下载以及每次执行时都必须通过固定 SHA-256 校验。请只把镜像和缓存环境变量指向可信位置。禁止网络访问时使用：

```bash
python scripts/setup.py --offline
```

### 注意事项

- AI 增强会重建纹理，不代表恢复了原始图片中不存在的真实信息。
- 8K 处理需要较多显存、内存和临时磁盘空间。
- 当前模型原生放大倍率为 4×；当目标 8K 超过原生 4×尺寸时，额外像素来自高质量缩放，不代表恢复了新的真实细节。
- 显存不足时依次尝试 `--tile 256` 和 `--tile 128`。
- JPEG 压缩不保留透明通道；如果背景颜色很重要，请先明确转换背景。
- 除非明确传入 `--overwrite`，压缩工具不会覆盖已有输出。

### 联系方式

更多 Skill 定制或功能需求，可以联系大瑜：`helloaigc2023`。

---

## English

### Overview

Local Image Upscaler is a local image-enhancement Skill for macOS and Windows x64. It uses local AI models to upscale images, export resolution presets, compress images to strict file-size targets, and inspect image properties before processing. Images are never uploaded, and source files are not overwritten by default.

### Features

- High-fidelity AI upscaling for photos, screenshots, and AI-generated artwork
- Automatic profile recommendations with user-selectable default, fast, photo, portrait, digital-art, and sharp-detail modes
- Clear advantages, limitations, and incremental storage before each optional model download
- `1K`, `2K`, `4K`, and `8K` presets
- Custom long-edge sizes without stretching
- Native 4× model output
- Strict file-size targets, such as compressing an approximately 1MB image to 200KB or less
- Quality-first compression with proportional resizing only when necessary
- Single-image and folder batch processing
- Image dimension, aspect-ratio, megapixel, and file-size inspection
- macOS and Windows x64 support
- Mirror fallback for restricted networks, offline caching, and SHA-256 verification

### Supported Formats

- Input: JPG, JPEG, PNG, WebP
- Upscale output: PNG, JPG, WebP (exact-size WebP has platform limitations)
- Target-size compression output: JPEG

### Choose an Algorithm

When the user does not specify an algorithm, the Skill visually inspects the image and recommends a profile. If the user declines to choose, it uses the conservative default. Generative face restoration is never enabled silently.

| Profile | Best for | Advantage | Limitation | First download |
| --- | --- | --- | --- | ---: |
| `default` | Unknown or mixed images | Balanced and conservative | Does not maximize sharpness | ~32MB |
| `fast` | Previews, batches, low-spec devices | Fastest and smallest | Reconstructs less detail | ~2.5MB |
| `photo` | Natural photographs | Natural texture and tonal transitions | Softer hard edges | ~32MB |
| `portrait` | Noisy, compressed, or rough natural portraits | Avoids face replacement and renders smoother transitions | Can remove fine detail from clean AI portraits | Shared with photo |
| `digital-art` | Anime, illustration, icons | Clean edges and compact model | Can simplify photographic texture | ~8.6MB |
| `sharp` | Architecture, products, game assets | Strongest apparent sharpness | Can amplify noise, halos, and skin texture | ~32MB |

List models, trade-offs, cache state, and incremental downloads without installing anything:

```bash
python scripts/setup.py --list-models
```

Do not select the portrait profile merely because a person is present. Prefer `default` for clean AI portraits and studio headshots; recommend `portrait` only when a natural portrait is noisy, compressed, or texturally rough.

### Prepare the Runtime

Run this command from the Skill directory:

```bash
python scripts/setup.py --model high-fidelity
```

Use the smaller model for previews or lower-spec devices:

```bash
python scripts/setup.py --model lite
```

Prepare only a selected profile:

```bash
python scripts/setup.py --profile photo
python scripts/setup.py --profile digital-art
python scripts/setup.py --profile sharp
```

The first setup downloads a pinned Upscayl NCNN runtime and model files and verifies every artifact with SHA-256. Every upscale also re-verifies the cached executable and selected model before execution, allowing safer offline reuse.

### Upscale to a Resolution Preset

```bash
python scripts/upscale.py input.png --target 1k
python scripts/upscale.py input.png --target 2k
python scripts/upscale.py input.png --target 4k
python scripts/upscale.py input.png --target 8k --tile 256
```

Choose an algorithm profile explicitly:

```bash
python scripts/upscale.py input.png --target 4k --profile portrait
python scripts/upscale.py input.png --target 4k --profile digital-art
python scripts/upscale.py input.png --target 4k --profile sharp
```

Presets refer to the image's long edge:

- 1K: 1920 pixels
- 2K: 2560 pixels
- 4K: 3840 pixels
- 8K: 7680 pixels

The source aspect ratio is always preserved. A 16:9 image becomes 3840×2160 at 4K, while a square image becomes 3840×3840.

Use a custom long edge:

```bash
python scripts/upscale.py input.png --max-edge 3000
```

Keep the model's native 4× output:

```bash
python scripts/upscale.py input.png --target scale4
```

### Compress to a Target File Size

Compress an image to 200KB or less:

```bash
python scripts/compress.py input.png --output output.jpg --target-kb 200
```

Compress an image to 1.5MB or less:

```bash
python scripts/compress.py input.png --target-mb 1.5
```

Adjust quality only and keep the original dimensions:

```bash
python scripts/compress.py input.png --target-kb 200 --keep-dimensions
```

The command fails clearly if the target cannot be reached at the original dimensions.

### Batch Processing

Batch upscale a folder:

```bash
python scripts/upscale.py input-folder --output output-folder --target 4k
```

Recursively compress a folder:

```bash
python scripts/compress.py input-folder --output output-folder --target-kb 200 --recursive
```

Preview a batch job without writing files:

```bash
python scripts/compress.py input-folder --output output-folder --target-kb 200 --recursive --dry-run
```

### Inspect Images

```bash
python scripts/inspect.py input.png
python scripts/inspect.py input-folder --recursive --json
```

The report includes dimensions, simplified aspect ratio, megapixels, and file size.

### Mirrors and Offline Mode

Configure one or more mirror prefixes through an environment variable:

```bash
IMAGE_UPSCALER_MIRRORS="https://mirror.example/proxy/" python scripts/setup.py
```

Artifacts from mirrors and custom cache directories must pass the same pinned SHA-256 checks both at download and execution time. Point mirror and cache environment variables only to trusted locations. To forbid network access:

```bash
python scripts/setup.py --offline
```

### Notes

- AI enhancement reconstructs texture; it cannot recover factual detail that was absent from the source.
- 8K processing requires substantial GPU memory, system memory, and temporary disk space.
- Bundled models are native 4× upscalers. When an 8K target exceeds native 4× output, the extra pixels come from high-quality resizing and are not newly recovered factual detail.
- On GPU-memory errors, try `--tile 256`, then `--tile 128`.
- JPEG compression does not preserve transparency; convert the background explicitly first when its color matters.
- Existing outputs are not overwritten unless `--overwrite` is explicitly supplied.

### Contact

For more Skill customization or feature requests, contact Dayu: `helloaigc2023`.
