# 配置参数详解

## extract_original.py（原始高清模式）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `pdf_folder` | `r"E:\AI家具链\家具素材库"` | PDF文件夹路径 |
| `output_folder` | `pdf_folder + "extract_original"` | 输出路径 |
| `min_size` | `10000` | 最小文件大小(字节)，小于此值跳过 |

```python
# ============ 配置区域 ============
pdf_folder = r"E:\你的PDF文件夹"
output_folder = os.path.join(pdf_folder, "extract_original")
# =================================
```

## extract_standard.py（标准尺寸模式）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `pdf_folder` | `r"E:\AI家具链\家具素材库"` | PDF文件夹路径 |
| `output_folder` | `pdf_folder + "extract_standard_800"` | 输出路径 |
| `target_size` | `800` | 输出图片最大边像素(可选: 600/800/1000) |

```python
# ============ 配置区域 ============
pdf_folder = r"E:\你的PDF文件夹"
output_folder = os.path.join(pdf_folder, "extract_standard_800")
target_size = 800  # 可选: 600, 800, 1000
# =================================
```

## extract_compress.py（压缩优化模式）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `pdf_folder` | `r"E:\AI家具链\家具素材库"` | PDF文件夹路径 |
| `output_folder` | `pdf_folder + "extract_compress_share"` | 输出路径 |
| `max_size` | `400` | 最大边像素 |
| `max_kb` | `50` | 最大文件大小(KB) |

```python
# ============ 配置区域 ============
pdf_folder = r"E:\你的PDF文件夹"
output_folder = os.path.join(pdf_folder, "extract_compress_share")
max_size = 400      # 最大边像素
max_kb = 50         # 最大文件大小(KB)
# =================================
```

## 输出示例

### 原始高清模式
- 文件名: `page001_img01.jpg`
- 尺寸: 原始分辨率（可能5MB+）
- 质量: 100%无损

### 标准尺寸模式
- 文件名: `PDF名_0001.jpg`
- 尺寸: 800x800正方形
- 质量: ~100KB JPG

### 压缩优化模式
- 文件名: `分享图_0001.jpg`
- 尺寸: 最大边400px
- 质量: ~30KB JPG
