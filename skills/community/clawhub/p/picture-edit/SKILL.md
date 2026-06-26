name: picture-edit
version: 1.0.0
description: 创意图片处理技能包，以"P一下图片"为核心理念，提供图片基础操作、增强、滤镜、拼接、背景移除、文字添加等强大功能

***

# picture-edit 创意图片处理技能包 🎨

强大的图片处理工具包，让你轻松 "P一下图片"！p 字母代表 Power（强力）、Productivity（生产力）、Precision（精准）、Playful（有趣）。

## 功能特性

### 核心基础操作

- **图片加载与保存**：支持 JPEG、PNG、WebP 等常见格式
- **尺寸调整**：按比例缩放或指定尺寸，保持图片质量
- **图片裁剪**：精确裁剪指定区域
- **格式转换**：多种图片格式互转

### 智能图片增强

- **亮度调整**：自由调节图片明暗
- **对比度调整**：增强画面层次感
- **清晰度增强**：让图片更锐利
- **智能增强**：一键优化，自动调整各项参数

### 创意滤镜特效

- **黑白滤镜**：经典黑白效果
- **复古滤镜**：怀旧 sepia 色调
- **模糊滤镜**：柔化画面，支持自定义模糊半径
- **轮廓滤镜**：提取边缘，艺术效果
- **反色滤镜**：颜色反转
- **像素化滤镜**：马赛克效果，支持自定义像素大小

### 图片拼接合成

- **水平拼接**：多张图片横向无缝拼接
- **垂直拼接**：多张图片纵向无缝拼接
- **网格拼接**：指定行列数，智能排列
- **智能对齐**：支持多种对齐方式（居中、左/右、上/下）

### 背景移除功能

- **简单背景移除**：自动检测白色/浅色背景并移除
- **指定颜色移除**：自定义背景颜色，支持容差调节
- **边缘平滑**：高斯模糊柔化边缘，更自然

### 文字添加功能

- **多种位置预设**：9种预设位置（左上、上中、右上、左中、居中、右中、左下、下中、右下）
- **自定义坐标**：精确 x,y 定位
- **字体样式**：支持自定义字体、字号、颜色
- **旋转效果**：任意角度旋转文字
- **中文字体**：自动检测并使用系统中文字体

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基础使用示例

```python
from p_skill import (
    load_image, save_image,
    resize_image, crop_image,
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

# 添加复古滤镜
filtered = sepia(enhanced)

# 添加文字
with_text = add_text(filtered, "Hello p-skill!", position="bottom-center")

# 保存结果
save_image(with_text, "output.jpg")
```

## API 文档

### 核心模块 (core)

#### load\_image(file\_path: str) -> Image.Image

加载图片文件。

**参数:**

- `file_path`: 图片文件路径

**返回:** PIL Image 对象

#### save\_image(image: Image.Image, output\_path: str, quality: int = 95) -> None

保存图片到文件。

**参数:**

- `image`: PIL Image 对象
- `output_path`: 输出文件路径
- `quality`: 图片质量 (1-100)，默认 95

#### resize\_image(image: Image.Image, size: tuple\[int, int] = None, scale: float = None) -> Image.Image

调整图片尺寸。

**参数:**

- `image`: PIL Image 对象
- `size`: 目标尺寸 (width, height)
- `scale`: 缩放比例

**返回:** 调整后的图片

#### crop\_image(image: Image.Image, box: tuple\[int, int, int, int]) -> Image.Image

裁剪图片。

**参数:**

- `image`: PIL Image 对象
- `box`: 裁剪区域 (left, upper, right, lower)

**返回:** 裁剪后的图片

#### convert\_format(image: Image.Image, format: str) -> Image.Image

转换图片格式。

**参数:**

- `image`: PIL Image 对象
- `format`: 目标格式 ('JPEG', 'PNG', 'WEBP' 等)

**返回:** 格式转换后的图片

### 增强模块 (enhance)

#### adjust\_brightness(image: Image.Image, factor: float) -> Image.Image

调整图片亮度。

**参数:**

- `image`: PIL Image 对象
- `factor`: 亮度因子 (1.0 为原图，<1.0 变暗，>1.0 变亮)

#### adjust\_contrast(image: Image.Image, factor: float) -> Image.Image

调整图片对比度。

**参数:**

- `image`: PIL Image 对象
- `factor`: 对比度因子 (1.0 为原图)

#### adjust\_sharpness(image: Image.Image, factor: float) -> Image.Image

调整图片清晰度。

**参数:**

- `image`: PIL Image 对象
- `factor`: 清晰度因子 (1.0 为原图，>1.0 更锐利)

#### smart\_enhance(image: Image.Image, brightness\_factor: float = 1.1, contrast\_factor: float = 1.1, sharpness\_factor: float = 1.2) -> Image.Image

智能增强，一键优化图片。

### 滤镜模块 (filters)

#### grayscale(image: Image.Image) -> Image.Image

黑白滤镜。

#### sepia(image: Image.Image) -> Image.Image

复古滤镜。

#### blur(image: Image.Image, radius: int = 2) -> Image.Image

模糊滤镜。

**参数:**

- `radius`: 模糊半径，默认 2

#### contour(image: Image.Image) -> Image.Image

轮廓滤镜。

#### invert(image: Image.Image) -> Image.Image

反色滤镜。

#### pixelate(image: Image.Image, pixel\_size: int = 10) -> Image.Image

像素化滤镜。

**参数:**

- `pixel_size`: 像素块大小，默认 10

### 拼接模块 (composite)

#### stitch\_horizontal(images: list\[Image.Image], align: str = 'center') -> Image.Image

水平拼接多张图片。

**参数:**

- `images`: 图片列表
- `align`: 对齐方式 ('top', 'bottom', 'center')

#### stitch\_vertical(images: list\[Image.Image], align: str = 'center') -> Image.Image

垂直拼接多张图片。

**参数:**

- `images`: 图片列表
- `align`: 对齐方式 ('left', 'right', 'center')

#### stitch\_grid(images: list\[Image.Image], cols: int, rows: int = None, align: str = 'center') -> Image.Image

网格拼接多张图片。

**参数:**

- `images`: 图片列表
- `cols`: 列数
- `rows`: 行数（可选，自动计算）
- `align`: 对齐方式

### 背景移除模块 (background)

#### remove\_background\_simple(image: Image.Image, threshold: int = 240, smooth\_radius: int = 2) -> Image.Image

简单背景移除（适用于白色/浅色背景）。

**参数:**

- `threshold`: 颜色阈值 (0-255)，默认 240
- `smooth_radius`: 边缘平滑半径，默认 2

**返回:** 透明背景的 RGBA 图片

#### remove\_background\_color(image: Image.Image, target\_color: tuple\[int, int, int], tolerance: int = 30, smooth\_radius: int = 2) -> Image.Image

指定颜色背景移除。

**参数:**

- `target_color`: 目标背景颜色 (R, G, B)
- `tolerance`: 颜色容差，默认 30
- `smooth_radius`: 边缘平滑半径，默认 2

**返回:** 透明背景的 RGBA 图片

### 文字添加模块 (text)

#### add\_text(image: Image.Image, text: str, position: str | tuple\[int, int] = 'center', font\_size: int = 36, color: tuple\[int, int, int] | tuple\[int, int, int, int] = (0, 0, 0), font\_path: str = None, rotation: float = 0, offset: tuple\[int, int] = (0, 0)) -> Image.Image

向图片添加文字。

**参数:**

- `image`: PIL Image 对象
- `text`: 要添加的文字内容
- `position`: 位置 ('top-left', 'top-center', 'top-right', 'center-left', 'center', 'center-right', 'bottom-left', 'bottom-center', 'bottom-right') 或 (x, y) 坐标
- `font_size`: 字体大小，默认 36
- `color`: 文字颜色 (R, G, B) 或 (R, G, B, A)
- `font_path`: 字体文件路径（可选，使用系统默认）
- `rotation`: 旋转角度，默认 0
- `offset`: 相对于位置的偏移 (x, y)，默认 (0, 0)

**返回:** 添加文字后的图片

## 性能说明

- 单张 1080p 图片处理时间通常 < 5 秒
- 支持最大分辨率取决于系统内存
- 推荐使用 PNG 格式保存需要透明背景的图片

## 依赖

- Pillow >= 10.0.0

