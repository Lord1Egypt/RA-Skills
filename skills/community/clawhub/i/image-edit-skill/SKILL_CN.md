---
name: pillow-skill  
description: 专业的Pillow (PIL)图像处理技能，用于图像处理、操作和分析。使用此技能进行图像编辑、批量处理、水印添加、格式转换和提取图像信息。提供可执行脚本和全面的参考文档。
---

# Pillow 图像处理技能

[English](SKILL.md) | 简体中文

此技能通过可执行脚本和Pillow (PIL)参考文档提供全面的图像处理能力。

## 何时使用此技能

当用户请求以下操作时激活此技能：

- 图像编辑操作（调整大小、裁剪、旋转、颜色调整）
- 批量处理多张图像
- 添加水印（文字或图像）
- 图像格式转换
- 提取图像元数据或EXIF数据
- 应用滤镜或效果
- 创建缩略图

## 核心能力

### 1. 图像编辑器 (`scripts/image_editor.py`)

对单张图像进行各种编辑操作：

**用法：**
```bash
python scripts/image_editor.py input.jpg output.jpg [选项]
```

**选项：**
- `--width WIDTH` / `--height HEIGHT`: 调整尺寸
- `--no-aspect`: 调整大小时忽略纵横比
- `--crop X Y WIDTH HEIGHT`: 裁剪矩形区域
- `--rotate DEGREES`: 旋转图像
- `--flip {horizontal,vertical}`: 翻转图像
- `--brightness FACTOR`: 调整亮度 (0.0-2.0)
- `--contrast FACTOR`: 调整对比度 (0.0-2.0)
- `--color FACTOR`: 调整色彩饱和度 (0.0-2.0)
- `--sharpness FACTOR`: 调整锐度 (0.0-2.0)
- `--filter {blur,contour,detail,edge_enhance,emboss,sharpen,smooth}`: 应用滤镜
- `--format FORMAT`: 输出格式 (JPEG, PNG等)
- `--quality QUALITY`: JPEG质量 (1-100)

**示例：**
```bash
# 保持纵横比调整大小
python scripts/image_editor.py photo.jpg resized.jpg --width 800

# 多个操作组合
python scripts/image_editor.py input.jpg output.jpg \
    --crop 100 100 800 600 \
    --rotate 90 \
    --brightness 1.2 \
    --sharpen 1.5
```

### 2. 批量处理器 (`scripts/batch_processor.py`)

并行处理多张图像：

**用法：**
```bash
python scripts/batch_processor.py input_dir output_dir [选项]
```

**选项：**
- `--pattern PATTERN`: 文件模式 (如 *.jpg)
- `--resize WIDTH HEIGHT`: 调整所有图像大小
- `--thumbnail MAX_W MAX_H`: 创建缩略图（保持纵横比）
- `--grayscale`: 转换为灰度图
- `--brightness FACTOR`: 调整亮度
- `--format FORMAT`: 转换格式
- `--quality QUALITY`: JPEG质量
- `--workers N`: 并行工作线程数 (默认: 4)

**示例：**
```bash
# 创建缩略图
python scripts/batch_processor.py ./photos ./thumbs --thumbnail 300 300

# 批量转换和调整大小
python scripts/batch_processor.py ./raw ./processed \
    --resize 1920 1080 \
    --format JPEG \
    --quality 90
```

### 3. 水印工具 (`scripts/watermark.py`)

添加文字或图像水印：

**用法：**
```bash
python scripts/watermark.py input.jpg output.jpg --text "文字" [选项]
python scripts/watermark.py input.jpg output.jpg --image logo.png [选项]
```

**通用选项：**
- `--position {top-left,top-right,bottom-left,bottom-right,center}`: 位置
- `--opacity 0-255`: 透明度级别
- `--margin PIXELS`: 与边缘的距离

**文字选项：**
- `--font-size SIZE`: 字体大小
- `--color COLOR`: 文字颜色 (white/black/red等)

**图像选项：**
- `--scale RATIO`: 水印缩放比例 (0.0-1.0)

**示例：**
```bash
# 文字水印
python scripts/watermark.py photo.jpg marked.jpg \
    --text "© 2026 公司名称" \
    --position bottom-right \
    --opacity 128

# Logo水印
python scripts/watermark.py image.jpg output.jpg \
    --image logo.png \
    --scale 0.2 \
    --position top-left
```

### 4. 图像信息 (`scripts/image_info.py`)

提取图像元数据和属性：

**用法：**
```bash
python scripts/image_info.py image.jpg [选项]
```

**选项：**
- `--format {text,json}`: 输出格式
- `--output FILE`: 保存到文件

**提供信息：**
- 文件信息（大小、路径）
- 图像属性（尺寸、格式、模式）
- 颜色信息（通道、调色板）
- EXIF数据（如果可用）
- 元数据

**示例：**
```bash
# 显示信息
python scripts/image_info.py photo.jpg

# 保存为JSON
python scripts/image_info.py photo.jpg -o info.json --format json
```

## 参考文档

### `references/common_operations.md`

全面的Pillow参考，涵盖：
- 打开和保存图像
- 调整大小和裁剪
- 旋转和翻转
- 颜色调整和增强
- 滤镜和效果
- 在图像上绘图
- 图像合成
- 通道操作
- EXIF数据处理
- 性能提示

**使用时机：** 当Claude需要特定的Pillow语法或操作模式时。

### `references/best_practices.md`

最佳实践指南，涵盖：
- 格式选择（JPEG vs PNG vs WebP）
- 调整大小策略
- 颜色模式转换
- 内存管理
- 水印策略
- 滤镜应用
- 优化技术
- 错误处理模式
- 常见工作流

**使用时机：** 设计图像处理工作流程或优化性能时。

## 工作流指南

### 步骤1: 分析需求
- 输入图像是什么格式？
- 需要什么操作？
- 是单张图像还是批量？
- 有质量要求吗？

### 步骤2: 选择合适的工具
- 单张图像编辑 → `image_editor.py`
- 多张图像 → `batch_processor.py`
- 添加水印 → `watermark.py`
- 需要信息 → `image_info.py`

### 步骤3: 规划操作
- 按逻辑顺序应用操作
- 考虑质量与文件大小的权衡
- 验证输入要求

### 步骤4: 执行和验证
- 使用适当选项运行脚本
- 检查输出质量
- 验证文件大小和格式

## 常见模式

### 模式1: Web图像优化
```bash
# 调整大小并优化用于网页
python scripts/image_editor.py large.jpg web.jpg \
    --width 1200 \
    --quality 85 \
    --format JPEG
```

### 模式2: 创建图像画廊
```bash
# 生成缩略图
python scripts/batch_processor.py ./originals ./gallery \
    --thumbnail 400 400 \
    --format JPEG \
    --quality 90
```

### 模式3: 为图像添加品牌水印
```bash
# 添加公司logo
python scripts/watermark.py product.jpg branded.jpg \
    --image company_logo.png \
    --position bottom-right \
    --scale 0.15 \
    --opacity 180
```

### 模式4: 批量格式转换
```bash
# PNG转JPEG
python scripts/batch_processor.py ./pngs ./jpegs \
    --format JPEG \
    --quality 95
```

## 依赖

```bash
pip install Pillow
```

## 有效使用提示

1. **保留原始文件**: 永远不要覆盖源图像
2. **使用适当格式**: 照片用JPEG，图形用PNG
3. **优化质量**: 平衡质量和文件大小
4. **批量操作**: 对多张图像使用批处理器
5. **查阅参考**: 咨询参考文档了解高级操作
6. **验证输入**: 处理前检查图像格式和大小
7. **先测试**: 批量处理前先在单张图像上测试

## 局限性

- 仅限2D图像处理（不支持视频）
- 某些EXIF数据在所有格式中可能无法保留
- 字体可用性因系统而异
- 非常大的图像可能需要大量内存
- 高级照片编辑（图层、遮罩）需要专门工具

## 故障排除

**导入错误**: 确保已安装Pillow (`pip install Pillow`)
**找不到字体**: 水印脚本会回退到默认字体
**内存错误**: 以较小批次处理大图像
**格式错误**: 检查输入图像格式兼容性
**RGBA转JPEG**: 脚本自动处理RGBA→RGB转换

有关详细操作和故障排除，请始终参考 `references/common_operations.md` 和 `references/best_practices.md`。
