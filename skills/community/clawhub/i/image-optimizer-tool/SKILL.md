---
name: image-optimizer-tool
description: 图片批量压缩和格式转换工具，支持批量调整大小、压缩质量、转换格式，预览模式和撤销功能！
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "python": "3.7+" },
      },
  }
---

# image-optimizer - 图片批量压缩和格式转换工具

图片批量压缩和格式转换工具，支持多种操作模式，预览模式和撤销功能！

## 功能特性

- ✅ **批量调整图片大小**：按宽度、高度或最大尺寸等比例缩放
- ✅ **批量压缩图片质量**：可调节压缩级别（1-100）
- ✅ **批量转换图片格式**：PNG ↔ JPEG ↔ WebP 互转
- ✅ **预览模式**：不实际修改文件，只显示操作预览
- ✅ **撤销功能**：自动备份原始文件，支持一键撤销
- ✅ **递归处理**：支持处理子文件夹中的图片

## 安装

```bash
# 安装依赖
pip install Pillow
```

## 使用方法

### 基本用法

```bash
# 压缩当前目录下所有 JPEG 图片，质量 85
python source/image_optimizer.py --quality 85

# 调整图片宽度最大为 1920px
python source/image_optimizer.py --max-width 1920

# 转换所有图片为 WebP 格式
python source/image_optimizer.py --format webp

# 预览模式（不实际修改）
python source/image_optimizer.py --quality 80 --preview

# 撤销上次操作
python source/image_optimizer.py --undo
```

### 详细参数

```
--directory DIRECTORY, -d DIRECTORY
                        要处理的目录（默认：当前目录）
--quality QUALITY, -q QUALITY
                        压缩质量 1-100（默认：85）
--max-width MAX_WIDTH   最大宽度（像素）
--max-height MAX_HEIGHT 最大高度（像素）
--max-size MAX_SIZE     最大边长（像素，同时限制宽高）
--format {png,jpeg,webp}, -f {png,jpeg,webp}
                        输出格式
--recursive, -r         递归处理子文件夹
--preview, -p           预览模式，不实际修改文件
--undo, -u              撤销上次操作
--output-dir OUTPUT_DIR
                        输出目录（不覆盖原文件）
--extensions EXTENSIONS
                        要处理的文件扩展名，逗号分隔（默认：jpg,jpeg,png,webp）
```

### 示例

```bash
# 压缩当前目录所有图片，质量 80，最大宽度 1920px
python source/image_optimizer.py -q 80 --max-width 1920

# 转换为 WebP 格式并保存到新文件夹
python source/image_optimizer.py -f webp --output-dir ./optimized

# 递归处理所有子文件夹
python source/image_optimizer.py -q 75 -r

# 只处理 PNG 文件
python source/image_optimizer.py -q 90 --extensions png
```

## 支持的格式

- 输入：JPEG, PNG, WebP, BMP, TIFF
- 输出：JPEG, PNG, WebP

## 注意事项

- 原始文件会自动备份到 `./.image_optimizer_backup/` 目录
- 撤销功能只能撤销最近一次操作
- WebP 格式支持透明度，JPEG 不支持
- 大图片处理可能需要较长时间
