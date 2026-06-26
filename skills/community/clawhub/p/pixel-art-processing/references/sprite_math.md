# Sprite Sheet Math / Sprite Sheet 数学

## 布局计算 / Layout Computation

给定帧数和布局模式，计算sprite sheet的行列数和最终尺寸。

```python
import math

def compute_layout(
    frame_count: int,
    frame_w: int,
    frame_h: int,
    spacing: int = 0,
    layout_mode: str = "fixed_columns",
    columns: int | None = None
) -> tuple[int, int, int, int]:
    """
    计算布局
    返回: (cols, rows, sheet_w, sheet_h)
    """
    if layout_mode == "fixed_columns" and columns:
        cols = columns
    else:
        # auto_square: 尽可能接近正方形的布局
        cols = max(1, math.ceil(math.sqrt(frame_count)))
    
    rows = math.ceil(frame_count / cols) if frame_count else 0
    
    sheet_w = cols * (frame_w + spacing) - spacing
    sheet_h = rows * (frame_h + spacing) - spacing
    
    return cols, rows, sheet_w, sheet_h
```

### 示例 / Examples

```
frame_count=12, frame_w=64, frame_h=64, spacing=4, fixed_columns, columns=4
→ cols=4, rows=3, sheet_w=252, sheet_h=192

frame_count=10, frame_w=64, frame_h=64, spacing=4, auto_square
→ cols=4, rows=3, sheet_w=252, sheet_h=192
```

## Alpha边界框计算 / Alpha Bounding Box

从PIL Image获取alpha通道的非空边界：

```python
from PIL import Image

def get_alpha_bbox(img: Image.Image) -> tuple[int, int, int, int] | None:
    """返回 (x1, y1, x2, y2)，全透明返回None"""
    if img.mode != "RGBA":
        return None
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    return bbox  # (left, upper, right, lower)
```

### 裁切模式 / Crop Modes

```python
def apply_crop(img, bbox, crop_mode, padding=0):
    if bbox is None:
        return img
    
    x1, y1, x2, y2 = bbox
    
    if crop_mode == "tight_bbox":
        # 紧贴alpha边界，无margin
        return img.crop((x1, y1, x2, y2))
    
    elif crop_mode == "safe_bbox":
        # alpha边界 + padding margin
        pad = padding
        return img.crop((
            max(0, x1 - pad),
            max(0, y1 - pad),
            min(img.width, x2 + pad),
            min(img.height, y2 + pad)
        ))
    
    elif crop_mode == "none":
        return img
```

## 缩放算法 / Scaling Algorithms

### 像素美术专用缩放 / Pixel Art Scaling

```python
from PIL import Image

def pixel_art_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """
    使用 LANCZOS (高质量) 缩放
    对于真正的像素美术缩放，应使用 nearest-neighbor
    """
    # 方法1: LANCZOS（平滑，适合有抗锯齿的图）
    resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 方法2: nearest（最近邻，适合纯像素图，避免模糊）
    resized = img.resize((target_w, target_h), Image.Resampling.NEAREST)
    
    return resized
```

### RPG Maker 144x144 硬缩放 / RPG Maker 144x144 Hard Scale

```python
def rpgmaker_hard_scale(img: Image.Image, target_w=144, target_h=144) -> Image.Image:
    """直接缩放到目标尺寸，不做任何插值平滑"""
    return img.resize((target_w, target_h), Image.Resampling.NEAREST)
```

## 序列帧帧合成 / Frame Composite

GIF帧需要按disposal类型合成：

```javascript
/**
 * 合成GIF帧到画布
 * @param prevBuf - 上一帧的像素缓冲 (RGBA Uint8ClampedArray)
 * @param frame - gifuct-js解压后的帧对象
 * @param width - 画布宽度
 * @param height - 画布高度
 * @returns 新的像素缓冲
 */
function compositeFrame(prevBuf, frame, width, height) {
  const buf = new Uint8ClampedArray(prevBuf)
  const { patch, dims, disposalType = 1 } = frame
  const { top, left, width: pw, height: ph } = dims

  // disposalType: 1=保留，2=恢复背景，3=恢复上一帧
  if (disposalType === 2) {
    // 恢复背景（清空透明）
    for (let i = 0; i < buf.length; i += 4) {
      buf[i] = buf[i+1] = buf[i+2] = buf[i+3] = 0
    }
  }

  // 将patch绘制到画布
  for (let py = 0; py < ph; py++) {
    for (let px = 0; px < pw; px++) {
      const idx = (py * pw + px) * 4
      const a = patch[idx + 3]
      const outY = top + py
      const outX = left + px
      if (outY >= 0 && outY < height && outX >= 0 && outX < width) {
        const outIdx = (outY * width + outX) * 4
        if (a === 0) {
          // 透明像素 → 清空目标
          buf[outIdx] = buf[outIdx+1] = buf[outIdx+2] = buf[outIdx+3] = 0
        } else {
          buf[outIdx] = patch[idx]
          buf[outIdx+1] = patch[idx+1]
          buf[outIdx+2] = patch[idx+2]
          buf[outIdx+3] = a
        }
      }
    }
  }
  return buf
}
```

## 透明行列检测 / Transparent Row/Col Detection

用于"超级拆分"——按透明间隔智能切割sprite sheet：

```javascript
/**
 * 找出完全透明的行
 * @param imageData - ImageData对象 (getImageData返回的)
 * @returns 透明行索引数组
 */
function findTransparentRows(imageData) {
  const { data, width, height } = imageData
  const rows = []
  for (let y = 0; y < height; y++) {
    let allTransparent = true
    for (let x = 0; x < width; x++) {
      if (data[(y * width + x) * 4 + 3] !== 0) {
        allTransparent = false
        break
      }
    }
    if (allTransparent) rows.push(y)
  }
  return rows
}

/**
 * 找出透明列（指定行范围内）
 */
function findTransparentCols(imageData, y0, y1) {
  const { data, width } = imageData
  const cols = []
  for (let x = 0; x < width; x++) {
    let allTransparent = true
    for (let y = y0; y < y1; y++) {
      if (data[(y * width + x) * 4 + 3] !== 0) {
        allTransparent = false
        break
      }
    }
    if (allTransparent) cols.push(x)
  }
  return cols
}

/**
 * 将透明索引数组转换为区间
 * runs: [[start, end], ...]
 * gaps: [[start, end], ...] 非透明区间
 */
function gapsFromRuns(runs, total) {
  if (runs.length === 0) return [[0, total - 1]]
  const regions = []
  regions.push([0, runs[0][0] - 1])
  for (let i = 0; i < runs.length - 1; i++) {
    regions.push([runs[i][1] + 1, runs[i+1][0] - 1])
  }
  regions.push([runs[runs.length-1][1] + 1, total - 1])
  return regions.filter(([a, b]) => a <= b)
}

/**
 * 将连续索引数组转换为区间
 */
function getRuns(arr) {
  if (arr.length === 0) return []
  const runs = []
  let runStart = arr[0], runEnd = runStart
  for (let i = 1; i < arr.length; i++) {
    if (arr[i] === runEnd + 1) {
      runEnd = arr[i]
    } else {
      runs.push([runStart, runEnd])
      runStart = runEnd = arr[i]
    }
  }
  runs.push([runStart, runEnd])
  return runs
}
```

## 色度键 (Chroma Key) / Chroma Key

```javascript
/**
 * 色度键抠图
 * @param imageData - 源ImageData
 * @param targetColor - {r, g, b} 要去除的颜色
 * @param tolerance - 容差 0-255
 * @param smooth - 是否平滑边缘
 */
function chromaKey(imageData, targetColor, tolerance, smooth=false) {
  const { data, width, height } = imageData
  const result = new Uint8ClampedArray(data)
  
  for (let i = 0; i < data.length; i += 4) {
    const dr = Math.abs(data[i] - targetColor.r)
    const dg = Math.abs(data[i+1] - targetColor.g)
    const db = Math.abs(data[i+2] - targetColor.b)
    
    if (Math.max(dr, dg, db) <= tolerance) {
      result[i+3] = 0  // 设为透明
    }
  }
  
  if (smooth) {
    // 边缘平滑：检测透明像素附近的不透明像素并做alpha混合
    // 简化为水平方向 3-pass 平滑
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const idx = (y * width + x) * 4
        if (result[idx+3] === 0) {
          // 检查周围像素
          let sumA = 0, cnt = 0
          for (let dy = -1; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
              const nx = x + dx, ny = y + dy
              if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                const nidx = (ny * width + nx) * 4
                if (result[nidx+3] > 0) {
                  sumA += result[nidx+3]
                  cnt++
                }
              }
            }
          }
          if (cnt > 0) {
            result[idx+3] = Math.min(255, Math.floor(sumA / cnt * 0.3))
          }
        }
      }
    }
  }
  
  return new ImageData(result, width, height)
}
```

## 水印检测 (Seedance) / Watermark Detection

```javascript
/**
 * 扫描视频帧平均帧四角，定位水印区域
 * 评分: edge_density × temporal_stability
 */
function autoDetectWatermarkCorner(framesStack, meanFrame, width, height) {
  // framesStack: [H, W, 3] × N
  // meanFrame: H, W, 3
  
  const cornerH = Math.max(60, Math.floor(height * 0.08))
  const cornerW = Math.max(120, Math.floor(width * 0.12))
  
  const corners = [
    [0, 0, cornerH, cornerW],                           // 左上
    [0, width - cornerW, cornerH, width],               // 右上
    [height - cornerH, 0, height, cornerW],             // 左下
    [height - cornerH, width - cornerW, height, width], // 右下
  ]
  
  let best = null, bestScore = 0
  for (const [r1, c1, r2, c2] of corners) {
    const roi = meanFrame[r1:r2, c1:c2]
    // 计算Canny边缘密度
    const edgeDensity = computeEdgeDensity(roi) / 255.0
    // 计算时域稳定性
    const temporalStd = computeTemporalStd(framesStack, r1, c1, r2, c2)
    const stability = 1.0 / (1.0 + temporalStd)
    
    const score = edgeDensity * stability
    if (score > bestScore && edgeDensity > 0.002) {
      bestScore = score
      // 精确定位边缘
      best = refineEdgeLocation(roi, r1, c1)
    }
  }
  return best
}
```
