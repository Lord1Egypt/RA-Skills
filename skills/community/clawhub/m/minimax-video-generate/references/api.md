# MiniMax 视频 API 参考

## 基础配置

- **国内用户**: `https://api.minimaxi.com/v1`
- **国际用户**: `https://api.minimax.io/v1`
- **认证方式**: `Authorization: Bearer $MINIMAX_API_KEY`

## API 端点

### 1. 视频生成 (Video Generation)

```
POST /v1/video_generation
```

**基础请求体**:
```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "视频描述文本"
}
```

**图生视频请求体**:
```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "视频描述文本",
  "image_url": "参考图片URL"
}
```

**首尾帧视频请求体**:
```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "视频描述文本",
  "start_image_url": "起始帧图片URL",
  "end_image_url": "结束帧图片URL"
}
```

**主体参考视频请求体**:
```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "视频描述文本",
  "subject_image_url": "主体参考图片URL"
}
```

**响应**:
```json
{
  "task_id": "任务ID",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 2. 查询视频任务状态

```
GET /v1/query/video_generation?task_id=xxx
```

**响应**:
```json
{
  "task_id": "任务ID",
  "status": "Success",
  "video_url": "视频下载URL"
}
```

**任务状态值**:
- `Pending` - 等待中
- `Processing` - 处理中
- `Success` - 成功
- `Fail` - 失败

### 3. 下载视频文件

```
GET /v1/files/retrieve?file_id=xxx
```

**响应**:
```json
{
  "file": {
    "file_id": "文件ID",
    "status": "active",
    "download_url": "下载URL"
  }
}
```

## 视频模型

- `MiniMax-Hailuo-2.3` - 最新一代视频生成模型，支持多种生成模式

## 视频规格

- 默认生成 5 秒视频
- 支持分辨率: 1280x720 (720P)
- 输出格式: MP4

## 使用流程

1. 调用视频生成API获取 task_id
2. 轮询查询任务状态
3. 任务完成后使用 file_id 下载视频
