# p-skill

创意图片处理技能包

## 版本

1.0.0

## 安装

```bash
pip install -r requirements.txt
```

## 简介

p-skill 是一个强大的创意图片处理技能包，以 "P一下图片" 为核心理念，提供高效、精准且有趣的图片处理能力。p 字母代表 Power（强力）、Productivity（生产力）、Precision（精准）、Playful（有趣）。

## 功能特性

- **图片基础操作**: 加载、保存、调整尺寸、裁剪、格式转换
- **图片增强**: 亮度、对比度、清晰度调整，智能增强
- **创意滤镜**: 黑白、复古、模糊、轮廓、反色、像素化
- **图片拼接**: 水平拼接、垂直拼接、网格拼接
- **背景移除**: 简单背景移除、指定颜色背景移除
- **文字添加**: 支持多种位置、字体、颜色、旋转角度的文字添加

## 快速开始

### 基础使用

```python
from p_skill import (
    load_image, save_image,
    resize_image, crop_image, convert_format,
    smart_enhance,
    grayscale, sepia,
    stitch_horizontal,
    remove_background_simple,
    add_text
)

# 加载图片
image = load_image("input.jpg")

# 调整尺寸
resized = resize_image(image, scale=0.5)

# 智能增强
enhanced = smart_enhance(resized)

# 添加滤镜
filtered = sepia(enhanced)

# 添加文字
with_text = add_text(filtered, "Hello p-skill!", position="bottom-center")

# 保存图片
save_image(with_text, "output.jpg")
```

## API 文档

### 核心模块 (core)

#### load_image(file_path: str) -> Image.Image
加载图片文件。

**参数:**
- `file_path`: 图片文件路径

**返回:** PIL Image 对象

#### save_image(image: Image.Image, output_path: str, quality: int = 95) -> None
保存图片到文件。

**参数:**
- `image`: PIL Image 对象
- `output_path`: 输出文件路径
- `quality`: 图片质量 (1-100)，默认 95

#### resize_image(image: Image.Image, size: tuple[int, int] = None, scale: float = None) -> Image.Image
调整图片尺寸。

**参数:**
- `image`: PIL Image 对象
- `size`: 目标尺寸 (width, height)
- `scale`: 缩放比例

**返回:** 调整后的图片

#### crop_image(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image
裁剪图片。

**参数:**
- `image`: PIL Image 对象
- `box`: 裁剪区域 (left, upper, right, lower)

**返回:** 裁剪后的图片

#### convert_format(image: Image.Image, format: str) -> Image.Image
转换图片格式。

**参数:**
- `image`: PIL Image 对象
- `format`: 目标格式 ('JPEG', 'PNG', 'WEBP' 等)

**返回:** 格式转换后的图片

### 增强模块 (enhance)

#### adjust_brightness(image: Image.Image, factor: float) -> Image.Image
调整亮度。

**参数:**
- `image`: PIL Image 对象
- `factor`: 亮度因子 (1.0 为原始亮度)

**返回:** 调整后的图片

#### adjust_contrast(image: Image.Image, factor: float) -> Image.Image
调整对比度。

**参数:**
- `image`: PIL Image 对象
- `factor`: 对比度因子 (1.0 为原始对比度)

**返回:** 调整后的图片

#### adjust_sharpness(image: Image.Image, factor: float) -> Image.Image
调整清晰度。

**参数:**
- `image`: PIL Image 对象
- `factor`: 清晰度因子 (1.0 为原始清晰度)

**返回:** 调整后的图片

#### smart_enhance(image: Image.Image, brightness_factor: float = 1.1, contrast_factor: float = 1.1, sharpness_factor: float = 1.2) -> Image.Image
智能增强图片。

**参数:**
- `image`: PIL Image 对象
- `brightness_factor`: 亮度因子
- `contrast_factor`: 对比度因子
- `sharpness_factor`: 清晰度因子

**返回:** 增强后的图片

### 滤镜模块 (filters)

#### grayscale(image: Image.Image) -> Image.Image
转换为黑白图片。

#### sepia(image: Image.Image) -> Image.Image
应用复古滤镜。

#### blur(image: Image.Image, radius: int = 5) -> Image.Image
应用模糊滤镜。

**参数:**
- `radius`: 模糊半径，默认 5

#### contour(image: Image.Image) -> Image.Image
应用轮廓滤镜。

#### invert(image: Image.Image) -> Image.Image
反色滤镜。

#### pixelate(image: Image.Image, pixel_size: int = 10) -> Image.Image
像素化滤镜。

**参数:**
- `pixel_size`: 像素块大小，默认 10

### 拼接模块 (composite)

#### stitch_horizontal(images: List[Image.Image], align: str = 'center') -> Image.Image
水平拼接图片。

**参数:**
- `images`: 图片列表
- `align`: 对齐方式 ('top', 'center', 'bottom')

#### stitch_vertical(images: List[Image.Image], align: str = 'center') -> Image.Image
垂直拼接图片。

**参数:**
- `images`: 图片列表
- `align`: 对齐方式 ('left', 'center', 'right')

#### stitch_grid(images: List[Image.Image], cols: int, rows: int = None, align: str = 'center') -> Image.Image
网格拼接图片。

**参数:**
- `images`: 图片列表
- `cols`: 列数
- `rows`: 行数（可选，自动计算）
- `align`: 对齐方式

### 背景模块 (background)

#### remove_background_simple(image: Image.Image, threshold: int = 240, smooth_radius: int = 2) -> Image.Image
简单背景移除（基于白色阈值）。

**参数:**
- `image`: PIL Image 对象
- `threshold`: 白色阈值 (0-255)，默认 240
- `smooth_radius`: 边缘平滑半径，默认 2

#### remove_background_color(image: Image.Image, target_color: tuple[int, int, int], tolerance: int = 30, smooth_radius: int = 2) -> Image.Image
指定颜色背景移除。

**参数:**
- `image`: PIL Image 对象
- `target_color`: 目标颜色 (R, G, B)
- `tolerance`: 颜色容差，默认 30
- `smooth_radius`: 边缘平滑半径，默认 2

### 文字模块 (text)

#### add_text(image: Image.Image, text: str, position: str | tuple[int, int] = "center", font_path: str | None = None, font_size: int = 40, color: tuple[int, int, int] | tuple[int, int, int, int] = (0, 0, 0), rotation: float = 0.0, offset: tuple[int, int] = (0, 0)) -> Image.Image
在图片上添加文字。

**参数:**
- `image`: PIL Image 对象
- `text`: 要添加的文字
- `position`: 位置（可以是坐标或预设位置）
  - 预设位置: 'top-left', 'top-center', 'top-right', 'center-left', 'center', 'center-right', 'bottom-left', 'bottom-center', 'bottom-right'
- `font_path`: 字体文件路径（可选）
- `font_size`: 字体大小，默认 40
- `color`: 文字颜色 (R, G, B) 或 (R, G, B, A)
- `rotation`: 旋转角度，默认 0
- `offset`: 位置偏移 (x, y)

**返回:** 添加文字后的图片

## 完整示例

查看 `example.py` 文件获取完整的使用示例。

## 支持的格式

- 输入: JPEG, PNG, WebP, BMP, GIF 等
- 输出: JPEG, PNG, WebP

## 性能

- 单张 1080p 图片处理时间 < 5 秒

## 测试

运行所有测试：

```bash
python test_core.py
python test_enhance.py
python test_filters.py
python test_composite.py
python test_background.py
python test_text.py
```

## 许可证

MIT License
