---
name: image-converter
description: 使用 Pillow 支持常见图像格式（PNG、JPEG、GIF、BMP、TIFF、WebP）之间的相互转换和格式不变的压缩，支持质量控制、尺寸缩放和无损压缩模式。
---

# Image Converter Skill

支持常见图像格式相互转换或保留原格式压缩的自动化工具，使用前请确保已安装 Pillow 库：

```bash
pip install Pillow

# 或使用uv
uv add Pillow
```

## 目标格式优先级 (Target Format Precedence)

1. `--to-format` 标志（最高优先级）
2. 明确的输出文件扩展名
3. 默认行为：
   - 默认：目录转换且未明确指定格式时转换为 WebP
   - `--compress` 模式：保留输入格式

## 快速开始 / Usage Examples

### Basic Format Conversion
Convert PNG to JPEG:
```bash
python scripts/convert.py input.png output.jpg
```

Convert WebP to PNG:
```bash
python scripts/convert.py input.webp output.png
```

Convert all images in a directory to PNG:
```bash
python scripts/convert.py ./input_dir ./output_dir --to-format png
```

### Explicit Format Specification
Convert JPEG to WebP even if output has .jpg extension:
```bash
python scripts/convert.py input.jpg output.jpg --to-format webp
```

### Compression
Compress PNG with quality 75 (preserves format):
```bash
python scripts/convert.py input.png output.png --compress --compress-quality 75
```

### Batch Processing (Multiple Files)
Process multiple files using comma-separated list, glob patterns, or wildcard:
```bash
# Comma-separated files
python scripts/convert.py "img1.png,img2.jpg,img3.webp" output_dir/ --to-format png

# Glob pattern
python scripts/convert.py "*.jpg" output_dir/ --to-format webp

# Multiple patterns
python scripts/convert.py "*.png,*.jpg" output_dir/ --to-format webp

# Parallel processing (4 threads)
python scripts/convert.py "*.jpg" output_dir/ --threads 4

# Verbose output
python scripts/convert.py "*.jpg" output_dir/ -v
```

### WebP Conversion (Legacy Usage Still Works)
Convert JPEG to WebP with quality 85:
```bash
python scripts/convert.py input.jpg output.webp --quality 85
```

Convert directory to WebP (keeps original files):
```bash
python scripts/convert.py ./images/ ./webp_output/
```

Lossless compression:
```bash
python scripts/convert.py input.png output.webp --lossless
```

Scale image (longest edge 1920px):
```bash
python scripts/convert.py input.jpg output.webp --max-size 1920
```

Batch compress directory (preserves format):
```bash
python scripts/convert.py ./images/ ./compressed/ --compress
```

## 功能列表

| 功能 | 说明 |
|------|------|
| 相互转换 | 支持常见图像格式之间的相互转换 |
| 批量转换 | 支持目录、文件列表、逗号分隔、通配符输入 |
| 并行处理 | 多线程批量转换加速 |
| 质量控制 | 有损压缩质量 1-100 |
| 无损模式 | 保持原始像素质量 |
| 尺寸缩放 | 按最长边等比缩放 |
| 色彩空间 | 自动转换 CMYK→RGB，调色板→RGBA |
| 元数据 | 清除 EXIF，保留 ICC 配置文件 |
| 格式保留压缩 | 保留原格式进行压缩（PNG/JPEG/GIF/WebP/TIFF） |

## CLI 参数

### 转换参数 (Conversion Options)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--to-format` | 明确指定目标格式 (jpeg, png, webp, gif, bmp, tiff)，优先级高于输出扩展名 | 无 |
| `--quality` | 压缩质量 (1-100) | 90 |
| `--max-size` | 最长边缩放像素 | 不缩放 |
| `--lossless` | 启用无损压缩 | False |

### 压缩参数（保留原格式）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--compress` | 启用压缩模式，保留原格式 | False |
| `--compress-quality` | 压缩质量 (1-100) | 85 |
| `--compress-level` | PNG/TIFF 压缩级别 (0-9) | 6 |

### 批量处理参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--threads` | 并行处理线程数 | 1 |
| `--verbose`, `-v` | 显示详细进度信息 | False |

## 参考

详细 WebP 参数配置请查看 [webp_settings.md](./references/webp_settings.md)。
