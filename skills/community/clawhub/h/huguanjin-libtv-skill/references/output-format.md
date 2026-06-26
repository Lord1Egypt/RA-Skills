# 输出格式

各脚本的标准 JSON 输出格式。

## create_session

```json
{
  "projectUuid": "aa3ba04c5044477cb7a00a9e5bf3b4d0",
  "sessionId": "90f05e0c-...",
  "projectUrl": "https://www.liblib.tv/canvas?projectId=aa3ba04c5044477cb7a00a9e5bf3b4d0"
}
```

## query_session

```json
{
  "messages": [
    {"id": "msg-xxx", "role": "user", "content": "生一个动漫视频"},
    {"id": "msg-yyy", "role": "assistant", "content": "..."}
  ],
  "projectUrl": "https://www.liblib.tv/canvas?projectId=..."
}
```
（`projectUrl` 仅在传入 `--project-id` 时存在）

## change_project

```json
{
  "projectUuid": "新项目UUID",
  "projectUrl": "https://www.liblib.tv/canvas?projectId=新项目UUID"
}
```

## upload_file

```json
{
  "url": "https://libtv-res.liblib.art/claw/{projectUuid}/{uuid}.png"
}
```

## download_results

```json
{
  "output_dir": "/Users/xxx/Downloads/libtv_results",
  "downloaded": ["/Users/xxx/Downloads/libtv_results/01.png", "..."],
  "total": 9
}
```

## gemini_generate_image

```json
{
  "model": "gemini-3-pro-image-preview",
  "output_dir": "/Users/xxx/Downloads/gemini_results",
  "saved": ["/Users/xxx/Downloads/gemini_results/gemini_20260324_120000_01.png"],
  "total": 1,
  "texts": ["...可选文本说明..."]
}
```

## sora_generate_video

```json
{
  "id": "video_4f573cf0-b4ed-405c-8900-b39a416ef60a",
  "object": "video",
  "model": "sora-2",
  "status": "queued",
  "progress": 0,
  "created_at": 1761635478,
  "seconds": 10,
  "size": "720x1280"
}
```

## sora_query_video

```json
{
  "id": "video_4f573cf0-b4ed-405c-8900-b39a416ef60a",
  "status": "completed",
  "progress": 100,
  "videoUrl": "https://.../result.mp4"
}
```
