# WebP 参数参考

Pillow WebP 编码器参数说明，用于 `Image.save()` 和 `WebPImagePlugin.WebPEncoder` 的配置。

## 参数说明

### quality

- **范围**: 1-100
- **默认**: 90
- **说明**: 有损压缩质量，数值越高画质越好，文件越大

### lossless

- **类型**: True/False
- **默认**: False
- **说明**: 启用无损压缩，忽略 quality 参数

### method

- **范围**: 0-6
- **默认**: 4
- **说明**: 压缩方法，0=最快但压缩比低，6=最慢但压缩比最高

### subsampling

- **范围**: 0-2
- **默认**: 0
- **说明**: 色度采样
  - 0: 4:4:4 (最佳质量)
  - 1: 4:2:2 (平衡)
  - 2: 4:2:0 (最小文件)

## 使用示例

### 高质量转换（网页图片）

```python
from PIL import Image

img = Image.open("input.png")
img.save("output.webp", quality=85, method=4)
```

### 无损压缩（图标、Logo）

```python
img.save("icon.webp", lossless=True, method=6)
```

### 高压缩比（缩略图、存档）

```python
img.save("thumb.webp", quality=70, method=6, subsampling=2)
```

### 完整参数示例

```python
img.save(
    "optimized.webp",
    quality=80,
    lossless=False,
    method=4,
    subsampling=0
)
```

## 最佳实践

| 场景 | quality | lossless | method | subsampling |
|------|---------|----------|--------|-------------|
| 网页图片 | 80-90 | False | 4 | 0 |
| 图标/Logo | - | True | 4-6 | 0 |
| 照片 | 85-95 | False | 4 | 1 |
| 缩略图 | 60-75 | False | 6 | 2 |

- **method=4** 是速度与压缩比的平衡点
- **subsampling=0** 适合文字和锐边图像
- **lossless=True** 适合需要保持原始细节的图像
