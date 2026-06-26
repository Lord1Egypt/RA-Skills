# Seedance 2.0 API 参考文档

## 接口地址

- **提交任务**: `POST {ARK_API_URL}/api/v3/contents/generations/tasks`
- **查询任务**: `GET {ARK_API_URL}/api/v3/contents/generations/tasks/{task_id}`

## 认证方式

```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

## 提交生成请求 (POST)

### Request Body

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，如 `doubao-seedance-2-0-260128` 或 `doubao-seedance-2-0-fast-260128` |
| `content` | array | 是 | 多模态内容数组，见下方详细说明 |
| `generate_audio` | boolean | 否 | 是否同步生成音频，默认 false |
| `ratio` | string | 否 | 视频比例，支持 `"16:9"` / `"9:16"` / `"1:1"`，默认 `"16:9"` |
| `duration` | integer | 否 | 视频时长（秒），范围 5-11，默认 10 |
| `watermark` | boolean | 否 | 是否添加水印，默认 false |

### content 数组元素类型

#### type: "text" (文本提示词)
```json
{ "type": "text", "text": "视频描述内容" }
```

#### type: "image_url" (参考图片)
```json
{
  "type": "image_url",
  "image_url": { "url": "https://example.com/image.jpg" },
  "role": "reference_image"
}
```

#### type: "video_url" (参考视频)
```json
{
  "type": "video_url",
  "video_url": { "url": "https://example.com/video.mp4" },
  "role": "reference_video"
}
```

#### type: "audio_url" (参考音频)
```json
{
  "type": "audio_url",
  "audio_url": { "url": "https://example.com/audio.mp3" },
  "role": "reference_audio"
}
```

### Response (成功)

```json
{
  "id": "cgt-20260410162021-xxxxx"
}
```

返回任务 ID，用于后续状态查询。

## 查询任务状态 (GET)

### Path Parameters

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | 任务 ID |

### Response - 处理中

```json
{
  "id": "cgt-20260410162021-xxxxx",
  "model": "doubao-seedance-2-0-fast-260128",
  "status": "running",       // pending / running
  "created_at": 1775809241,
  "updated_at": 1775809241,
  "service_tier": "default",
  "execution_expires_after": 172800,
  "generate_audio": true,
  "draft": false
}
```

### Response - 完成

```json
{
  "id": "cgt-20260410162021-xxxxx",
  "status": "completed",
  "video_result": {
    "video_url": "https://xxx/output.mp4",
    "cover_image_url": "https://xxx/cover.jpg"
  }
}
```

### Response - 失败

```json
{
  "id": "cgt-20260410162021-xxxxx",
  "status": "failed",
  "error": {
    "code": "error_code",
    "message": "错误描述"
  }
}
```

## 错误码说明

常见错误：
- 认证失败：检查 API Key 是否正确
- 参数校验失败：检查 content 数组格式、duration/ratio 范围
- 资源不可用：检查参考图片/视频/音频 URL 是否公网可访问
- 额度不足：检查账户余额或调用配额
