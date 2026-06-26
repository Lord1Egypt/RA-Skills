# EMO API（DashScope）

官方文档：
- EMO 检测：`https://help.aliyun.com/zh/model-studio/emo-detect-api`
- EMO 生成：`https://help.aliyun.com/zh/model-studio/emo-api`

## 鉴权与地域
- 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`
- 地域：**北京**（`dashscope.aliyuncs.com`）
- 必须设置请求头：`X-DashScope-Async: enable`

## 1) 人像检测（必须先调）
`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect`

请求体：
```json
{
  "model": "emo-detect-v1",
  "input": {"image_url": "https://.../portrait.png"},
  "parameters": {"ratio": "1:1"}
}
```

成功返回关键字段：
- `output.check_pass`
- `output.face_bbox`
- `output.ext_bbox`

## 2) 提交视频生成任务
`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

请求体：
```json
{
  "model": "emo-v1",
  "input": {
    "image_url": "https://.../portrait.png",
    "audio_url": "https://.../speech.mp3",
    "face_bbox": [302,286,610,593],
    "ext_bbox": [71,9,840,778]
  },
  "parameters": {"style_level": "normal"}
}
```

返回：`output.task_id`

## 3) 轮询任务
`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

状态流转：`PENDING -> RUNNING -> SUCCEEDED/FAILED`

成功结果路径：
- `output.results.video_url`

## 限制
- 图片：最小边 >= 400，最大边 <= 7000
- 音频：wav/mp3，<= 15MB，<= 60 秒
- URL 必须是公网 http/https
