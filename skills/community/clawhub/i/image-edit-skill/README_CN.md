# Pillow 图像处理技能

[English](README.md) | 简体中文

一个基于Pillow (PIL)的全面图像处理技能包。提供强大的工具用于编辑、批量处理、添加水印和分析图像。

## 功能特性

- **图像编辑**: 调整大小、裁剪、旋转、翻转、调整颜色和应用滤镜
- **批量处理**: 并行处理多个图像并应用一致的操作
- **水印添加**: 添加文本或图像水印，支持自定义位置和透明度
- **图像分析**: 提取详细信息、元数据和EXIF数据
- **格式转换**: 在JPEG、PNG、GIF、BMP、TIFF、WebP等格式间转换

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 编辑单张图像
```bash
# 按比例调整大小
python scripts/image_editor.py input.jpg output.jpg --width 800

# 裁剪和旋转
python scripts/image_editor.py photo.jpg edited.jpg \
    --crop 100 100 800 600 \
    --rotate 90

# 调整亮度和对比度
python scripts/image_editor.py dark.jpg bright.jpg \
    --brightness 1.5 \
    --contrast 1.2
```

### 批量处理多张图像
```bash
# 为所有图像创建缩略图
python scripts/batch_processor.py ./photos ./thumbnails \
    --thumbnail 300 300

# 将所有图像转换为JPEG
python scripts/batch_processor.py ./images ./output \
    --format JPEG \
    --quality 90
```

### 添加水印
```bash
# 文字水印
python scripts/watermark.py input.jpg output.jpg \
    --text "© 2026 我的公司" \
    --position bottom-right

# 图像水印
python scripts/watermark.py photo.jpg watermarked.jpg \
    --image logo.png \
    --scale 0.15 \
    --opacity 180
```

### 提取图像信息
```bash
# 显示图像信息
python scripts/image_info.py photo.jpg

# 将信息保存为JSON
python scripts/image_info.py photo.jpg -o info.json --format json
```

## 目录结构

```
pillow-skill/
├── SKILL.md                    # 主技能文档(英文)
├── SKILL_CN.md                 # 主技能文档(中文)
├── README.md                   # 英文说明
├── README_CN.md                # 本文件
├── EXAMPLES.md                 # 使用示例(英文)
├── EXAMPLES_CN.md              # 使用示例(中文)
├── requirements.txt            # Python依赖
├── scripts/
│   ├── image_editor.py        # 单张图像编辑工具
│   ├── batch_processor.py     # 批量处理工具
│   ├── watermark.py           # 水印添加工具
│   └── image_info.py          # 图像信息提取器
├── references/
│   ├── common_operations.md   # Pillow操作参考
│   └── best_practices.md      # 图像处理最佳实践
└── assets/
    └── templates/             # 模板图像和资源
```

## 文档

- **SKILL.md / SKILL_CN.md**: 完整的技能文档，包含所有功能
- **EXAMPLES.md / EXAMPLES_CN.md**: 全面的使用示例和教程
- **references/common_operations.md**: Pillow操作快速参考
- **references/best_practices.md**: 最佳实践和优化技巧

## 使用场景

- ✅ 为网页画廊创建缩略图
- ✅ 批量调整图像大小用于移动应用
- ✅ 添加水印保护版权
- ✅ 转换图像进行网页优化
- ✅ 提取和分析图像元数据
- ✅ 为照片应用滤镜和效果
- ✅ 自动化图像处理工作流

## 系统要求

- Python 3.8+
- Pillow 10.0+

## 许可证

MIT License
