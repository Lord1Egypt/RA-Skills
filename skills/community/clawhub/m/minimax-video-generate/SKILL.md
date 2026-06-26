---
name: minimax-video
description: MiniMax 视频生成技能 - 支持文生视频(Text-to-Video)、图生视频(Image-to-Video)、首尾帧视频(Frame-to-Frame)、主体参考视频(Subject-to-Video)。使用模型 MiniMax-Hailuo-2.3，默认生成 5 秒 720P MP4 视频，自动下载保存到本地。
version: 1.0.0
author: laowang
tags:
  - minimax
  - video
  - generation
  - video-generation
  - MiniMax-Hailuo-2.3
---

# MiniMax Video Skill

使用 MiniMax API 进行视频生成和视频编辑。支持文生视频、图生视频、首尾帧视频、主体参考视频。使用模型 MiniMax-Hailuo-2.3，默认生成 5 秒 720P MP4 视频，支持自动下载到本地。

## 环境配置

```json
{
  "MINIMAX_API_KEY": "your-api-key",
  "MINIMAX_REGION": "cn" | "int"
}
```

- `MINIMAX_API_KEY`: MiniMax API 密钥
- `MINIMAX_REGION`: 区域设置，`cn` 为中国，`int` 为国际（默认 `cn`）

## 可用函数

### generate_video(prompt, model)
文生视频 - 根据文本描述生成视频

**参数**:
- `prompt`: 视频描述文本
- `model`: 视频模型（默认: `MiniMax-Hailuo-2.3`）

**返回**: 任务ID列表

**示例**: `generate_video("一只猫在草地上奔跑")`

### generate_video_with_image(prompt, image_url, model)
图生视频 - 根据参考图和描述生成视频

**参数**:
- `prompt`: 视频描述文本
- `image_url`: 参考图片URL
- `model`: 视频模型

**返回**: 任务ID列表

**示例**: `generate_video_with_image("让这幅画动起来", "https://example.com/painting.jpg")`

### generate_video_with_frames(prompt, start_image_url, end_image_url, model)
首尾帧视频 - 根据起始帧和结束帧生成过渡视频

**参数**:
- `prompt`: 视频描述文本
- `start_image_url`: 起始帧图片URL
- `end_image_url`: 结束帧图片URL
- `model`: 视频模型

**返回**: 任务ID列表

**示例**: `generate_video_with_frames("花朵绽放的过程", "seed.jpg", "flower.jpg")`

### generate_video_with_subject(prompt, subject_image_url, model)
主体参考视频 - 根据主体参考图和描述生成视频

**参数**:
- `prompt`: 视频描述文本
- `subject_image_url`: 主体参考图片URL
- `model`: 视频模型

**返回**: 任务ID列表

**示例**: `generate_video_with_subject("让这个人物跳舞", "https://example.com/person.jpg")`

### query_video_task(task_id)
查询视频生成任务状态

**参数**:
- `task_id`: 任务ID

**返回**: 任务状态信息 `{status, video_url, ...}`

**状态值**: `Pending`, `Processing`, `Success`, `Fail`

### wait_for_video(task_id, poll_interval, max_wait)
等待视频生成完成（轮询）

**参数**:
- `task_id`: 任务ID
- `poll_interval`: 轮询间隔秒数（默认: 10）
- `max_wait`: 最大等待时间（默认: 600）

**返回**: 最终任务状态信息

### get_file_info(file_id)
获取文件信息

**参数**:
- `file_id`: 文件ID

**返回**: 文件信息 `{file: {file_id, status, download_url}}`

### download_video(file_id, output_path)
下载视频到本地

**参数**:
- `file_id`: 文件ID
- `output_path`: 保存路径

**返回**: 保存的文件路径

## 使用示例

### 文生视频

```
python scripts/video.py generate "日出时分的海边，海浪轻轻拍打沙滩"
```

### 图生视频

```
python scripts/video.py from-image "让这幅风景画动起来" -i https://example.com/landscape.jpg
```

### 首尾帧视频

```
python scripts/video.py frames "人物从室内走到室外" -s indoor.jpg -e outdoor.jpg
```

### 主体参考视频

```
python scripts/video.py subject "让这个人物挥手" -i https://example.com/person.jpg
```

### 查询任务状态

```
python scripts/video.py query <task_id>
```

### 等待视频完成

```
python scripts/video.py wait <task_id> -i 10
```

### 下载视频

```
python scripts/video.py download <file_id> -o video.mp4
```

## 视频规格

- 默认生成 5 秒视频
- 分辨率: 1280x720 (720P)
- 格式: MP4

## 注意事项

1. 视频生成是异步的，需要通过 task_id 查询状态
2. 建议使用 `wait_for_video` 函数自动等待完成
3. 生成的视频有效期有限，请及时下载
4. 视频生成可能需要几分钟时间，请耐心等待
