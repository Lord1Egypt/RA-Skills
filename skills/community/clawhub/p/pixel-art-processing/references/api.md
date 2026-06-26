# API Reference / API 参考

> [!NOTE]
> Base URL: `http://localhost:8000` (本地部署后 / After local deployment)
> 所有API均为REST JSON格式，文件上传使用 `multipart/form-data`。

## Job System / 任务系统

### 创建视频处理任务 / Create Video Processing Job

```
POST /jobs
Content-Type: multipart/form-data
```

**参数 / Parameters:**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| file | UploadFile | 必填 | 视频文件 |
| params | string (JSON) | {} | 任务参数 |

**JobParams 结构 / Structure:**

```json
{
  "fps": 12,
  "frame_range": {
    "start_sec": 0,
    "end_sec": 5,
    "start_frame": null,
    "end_frame": null
  },
  "max_frames": 300,
  "target_size": { "w": 256, "h": 256 },
  "bg_color": "transparent",
  "transparent": true,
  "padding": 4,
  "spacing": 4,
  "layout_mode": "fixed_columns",
  "columns": 12,
  "matte_strength": 0.6,
  "crop_mode": "tight_bbox"
}
```

**响应 / Response:**

```json
{
  "job_id": "abc123def456"
}
```

---

### 查询任务状态 / Query Job Status

```
GET /jobs/{job_id}
```

**响应 / Response:**

```json
{
  "id": "abc123def456",
  "status": "completed",
  "progress": 100,
  "params": { ... },
  "result": {
    "frame_count": 60,
    "width": 1024,
    "height": 512
  },
  "error": null
}
```

**status 状态值 / Values:**
- `queued` — 排队中 / Queued
- `processing` — 处理中 / Processing
- `completed` — 已完成 / Completed
- `failed` — 失败 / Failed

---

### 下载结果 / Download Result

```
GET /jobs/{job_id}/result?format=png
GET /jobs/{job_id}/result?format=zip
```

- `format=png` → 返回sprite.png
- `format=zip` → 返回sprite.png + index.json 打包

---

### 获取索引JSON / Get Index JSON

```
GET /jobs/{job_id}/index
```

返回index.json文件，包含完整帧位置信息。

---

### 删除任务 / Delete Job

```
DELETE /jobs/{job_id}
```

---

## Image Processing / 图像处理

### AI抠图 / AI Matting

```
POST /matte
Content-Type: multipart/form-data
```

**参数:**
- file: PNG/JPG/WebP图片，最大20MB

**响应:** 透明背景PNG图片

---

## Watermark Removal / 水印去除

### 创建水印去除任务 / Create Watermark Job

```
POST /watermark
Content-Type: multipart/form-data
```

上传Seedance/即梦视频，创建去水印任务。

**响应:**

```json
{
  "job_id": "wm_abc123"
}
```

---

### 查询水印任务状态 / Query Watermark Job

```
GET /watermark/{job_id}
```

---

### 下载去水印视频 / Download Clean Video

```
GET /watermark/{job_id}/result
```

---

### 删除水印任务 / Delete Watermark Job

```
DELETE /watermark/{job_id}
```

---

## Local Processing (No Backend) / 本地处理（无需后端）

### GIF → Frames / GIF拆帧

使用 `gifuct-js` 在浏览器中直接拆帧：

```javascript
import { parseGIF, decompressFrames } from 'gifuct-js'

const buf = await gifFile.arrayBuffer()
const gif = parseGIF(buf)
const frames = decompressFrames(gif, true)

// 合成帧缓冲区（处理GIF disposal）
let prevBuf = new Uint8ClampedArray(w * h * 4)
for (const frame of frames) {
  prevBuf = compositeFrame(prevBuf, frame, w, h)
  // 保存 prevBuf 为 PNG
}
```

### Frames → GIF / 序列帧合成GIF

使用 `gifenc`:

```javascript
import { GIFEncoder, quantize, applyPalette } from 'gifenc'

const gif = GIFEncoder()
for (const imgData of frames) {
  const palette = quantize(imgData.data, 255, { format: 'rgba4444', oneBitAlpha: 128 })
  const index = applyPalette(imgData.data, palette)
  gif.writeFrame(index, width, height, { palette, delay: frameDelay })
}
gif.finish()
```

### Sprite Sheet拆分 / Sprite Sheet Split

```javascript
// cols, rows = 布局列行数
// frameW, frameH = 每帧尺寸
for (let i = 0; i < cols * rows; i++) {
  const col = i % cols
  const row = Math.floor(i / cols)
  const x = col * (frameW + spacing)
  const y = row * (frameH + spacing)
  // 从大图裁切 (x, y, frameW, frameH) 区域
}
```

---

## Index JSON Schema / 索引JSON结构

```json
{
  "version": "1.0",
  "frame_size": { "w": 64, "h": 64 },
  "sheet_size": { "w": 256, "h": 256 },
  "frames": [
    {
      "i": 0,
      "x": 0,
      "y": 0,
      "w": 64,
      "h": 64,
      "t": 0.0
    }
  ]
}
```
