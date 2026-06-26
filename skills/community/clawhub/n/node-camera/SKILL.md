---
name: node-camera
description: >-
  控制 Node 设备的 USB 摄像头，支持单帧截图、流式推送、停止推流和关闭摄像头。使用场景：(1) 需要快速获取 Node 设备的一帧图像时，(2) 需要远程监控 Node 设备周围环境时，(3) 需要进行视觉识别或拍照截图时。
metadata:
  openclaw:
    capabilities: ["camera", "streaming", "vision"]
---

# Node Camera - Node 设备摄像头控制

本 Skill 用于控制已配对 Android Node 设备的 USB 摄像头，支持高效单帧截图、流式推送 JPEG 帧到云端、停止推流和关闭摄像头。

## 何时使用此 Skill

- **快速截图**: 需要获取 Node 设备当前画面的一帧图像（推荐使用 `camera.captureFrame`）
- **实时监控**: 需要持续查看 Node 设备周围的实时画面
- **视觉识别**: 获取视频帧用于 AI 识别分析
- **视频流处理**: 持续接收视频流数据进行后续处理

## Commands

### camera.captureFrame

**描述**: 高效单帧截图。打开摄像头 → 获取第一帧 → 自动停止推流并关闭摄像头 → 返回图片 URL。适用于只需要一张图片的场景，无需手动管理摄像头生命周期。

**参数:**
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| width | number | 否 | 设备默认 | 分辨率宽度（像素） |
| height | number | 否 | 设备默认 | 分辨率高度（像素） |

**返回:**
```json
{
  "imageUrl": "http://<设备IP>:18790/images/capture_1234567890.jpg"
}
```
图片通过 Node 设备内嵌的 HTTP 服务器（端口 18790）提供访问，可直接通过 URL 下载 JPEG 文件。

**错误码:**
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| CAPTURE_FAILED | 截图失败 | 检查摄像头连接状态 |
| TIMEOUT | 调用超时 | 检查设备网络或重试 |

### camera.open

**描述**: 打开 USB 摄像头并开始流式推送帧数据到云端。命令立即返回成功状态，帧数据通过 `camera.frame` 事件异步推送。如果指定的分辨率不支持，会自动降级到最近可用分辨率。

**参数:**
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| width | number | 否 | 设备默认 | 分辨率宽度（像素） |
| height | number | 否 | 设备默认 | 分辨率高度（像素） |

**返回:**
命令立即返回：
```json
{
  "status": "streaming_started"
}
```

帧数据通过 `camera.frame` node event 异步推送，每帧格式为：
```json
{
  "imageUrl": "http://<设备IP>:18790/images/frame_1234567890_0.jpg"
}
```

**错误码:**
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| -1 | 摄像头已在运行中 | 先调用 camera.stopStreaming 或 camera.close |
| -1 | 摄像头未初始化 | 先在 Node 设备上打开相机主界面 |
| -1 | 摄像头错误 | 重新打开 Node 设备的相机应用 |

### camera.stopStreaming

**描述**: 停止摄像头推流，但保持摄像头打开状态。如需完全关闭，请调用 camera.close。

**参数:** 无

**返回:**
```json
{
  "ok": true,
  "message": "预览数据回调已停止"
}
```

### camera.close

**描述**: 关闭并释放 USB 摄像头资源。注意：实际摄像头硬件由 Node 主界面生命周期管理，此命令仅停止流式回调。

**参数:** 无

**返回:**
```json
{
  "ok": true,
  "message": "已停止数据回调"
}
```

## 如何调用底层命令

使用 OpenClaw gateway node invoke API：

### 高效截取单帧图片（推荐）

```json
{
  "action": "invoke",
  "invokeCommand": "camera.captureFrame",
  "invokeParamsJson": {
    "width": 1280,
    "height": 720
  }
}
```

### 打开摄像头流式推送

```json
{
  "action": "invoke",
  "invokeCommand": "camera.open",
  "invokeParamsJson": {
    "width": 1280,
    "height": 720
  }
}
```

### 停止推流

```json
{
  "action": "invoke",
  "invokeCommand": "camera.stopStreaming",
  "invokeParamsJson": {}
}
```

### 关闭摄像头

```json
{
  "action": "invoke",
  "invokeCommand": "camera.close",
  "invokeParamsJson": {}
}
```

## 工作流程示例

### 场景1: 获取单张截图（推荐）

```
1. camera.captureFrame {"width": 1920, "height": 1080}
2. 从返回结果中获取 imageUrl，通过 HTTP GET 下载图片
```

> 使用 `camera.captureFrame` 无需手动管理摄像头生命周期，一条命令完成截图。

### 场景2: 持续监控

```
1. camera.open {"width": 1280, "height": 720}
2. 监听 camera.frame 事件，实时接收并处理每一帧
3. camera.stopStreaming {} (暂停推流)
4. camera.close {} (结束监控，释放资源)
```

### 场景3: 视觉识别

```
1. camera.captureFrame {"width": 640, "height": 480} (低分辨率提高性能)
2. 通过返回的 imageUrl 下载图片，送入视觉模型进行识别
3. 如需多帧，重复步骤 1
```

### 场景4: 持续视觉识别

```
1. camera.open {"width": 640, "height": 480}
2. 监听 camera.frame 事件，将每帧送入视觉模型
3. camera.stopStreaming {} (识别完成后停止推流)
4. camera.close {} (释放资源)
```

## 错误处理

### 摄像头已在运行中

如果收到错误 `"摄像头已在运行中，请先调用 stopStreaming 或 closeCamera"`：
- 先调用 `camera.stopStreaming` 停止当前推流
- 或调用 `camera.close` 完全关闭后重新打开

### 摄像头未初始化

如果收到错误 `"摄像头未初始化，请先打开 AngleCamera 主界面"`：
- 在 Node 设备上手动打开相机主界面
- 确保摄像头硬件已连接并被系统识别

### 摄像头错误

如果收到错误 `"摄像头错误: xxx，请重新打开 AngleCamera"`：
- 重新打开 Node 设备的相机应用
- 检查 USB 摄像头是否松动或故障

### 分辨率不支持

如果指定的分辨率不被支持：
- 系统会自动降级到最近可用分辨率
- 返回的实际分辨率可能与请求不同
- 建议先查询支持的分辨率列表（如设备支持）

## Node 要求

此 Skill 需要 Android Node 设备具备以下条件：

1. **USB 摄像头**: 设备已连接可用的 USB 摄像头
2. **相机应用**: 安装了 AngleCamera 或兼容的相机主界面
3. **权限**: 已授予相机和存储权限
4. **网络**: Node 与 OpenClaw Gateway 正常连接

## 注意事项

- **资源管理**: 使用流式推送时务必调用 `camera.close` 或 `camera.stopStreaming` 释放资源
- **优先使用 captureFrame**: 只需一帧图片时，使用 `camera.captureFrame` 比 open→stop→close 更高效稳定
- **电量消耗**: 持续视频流会显著增加设备电量消耗
- **带宽占用**: 高分辨率视频流会占用较多网络带宽
- **并发限制**: 同一时间只能有一个流式回调运行
- **硬件管理**: 实际摄像头硬件由 Node 主界面生命周期管理，ToolService 仅控制流传输

## 技术细节

### 图像传输

- **格式**: JPEG 文件
- **传输方式**: Node 设备内嵌 HTTP 服务器（Ktor CIO，端口 18790）提供图片文件访问
- **URL 格式**: `http://<设备IP>:18790/images/<filename>.jpg`
- **颜色空间**: YUV 转 RGB（设备自动处理）
- **帧率**: 取决于设备和分辨率，通常为 15-30 FPS
- **文件清理**: 自动保留最近 50 张图片，旧图片自动删除

### 事件机制

`camera.open` 使用 node event 推送帧数据：
- 命令立即返回 `{"status":"streaming_started"}`
- 帧通过 `camera.frame` 事件异步推送到云端
- 每帧格式: `{"imageUrl":"http://<设备IP>:18790/images/frame_xxx.jpg"}`
- 调用 `camera.stopStreaming` 或 `camera.close` 结束推送

### 状态机

摄像头内部状态：
- `Idle`: 未初始化，主界面未运行
- `Opening`: 正在打开中
- `Opened`: 已打开，可预览
- `FallingBack`: 分辨率降级中
- `Closed`: 已关闭
- `Error`: 错误状态
