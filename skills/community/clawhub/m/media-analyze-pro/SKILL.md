# media-analyzer

音视频内容分析技能 - 分析本地或在线的音视频文件，提取元数据、音频特征、视频帧信息。

## 功能

- **视频分析**: 提取视频元数据（时长、分辨率、帧率、编码格式等）
- **音频分析**: 提取音频信息（采样率、声道、编码、时长等）
- **帧提取**: 从视频中提取关键帧或指定时间点的截图
- **音频波形**: 生成音频波形可视化
- **内容摘要**: 快速了解音视频文件的基本信息

## 触发词

- 内容分析
- 视频分析
- 音频分析
- 媒体信息
- 提取视频帧
- 音视频元数据

## 使用方式

```bash
# 分析视频文件
media-analyzer analyze /path/to/video.mp4

# 分析音频文件
media-analyzer analyze /path/to/audio.mp3

# 提取视频帧（第10秒）
media-analyzer frame /path/to/video.mp4 --timestamp 10

# 提取视频封面
media-analyzer cover /path/to/video.mp4

# 生成音频波形图
media-analyzer waveform /path/to/audio.mp3

# 批量分析目录
media-analyzer batch /path/to/media/folder
```

## 依赖

- ffmpeg (必须)
- ffprobe (必须，通常随ffmpeg一起安装)

## 输出格式

分析结果以结构化JSON格式返回，包含：
- 文件路径
- 媒体类型（视频/音频）
- 时长
- 分辨率（视频）
- 帧率（视频）
- 编码格式
- 比特率
- 音频轨道信息
- 创建时间

## 示例输出

```json
{
  "file": "/path/to/video.mp4",
  "type": "video",
  "duration": "00:05:30",
  "duration_seconds": 330,
  "resolution": "1920x1080",
  "width": 1920,
  "height": 1080,
  "frame_rate": "30.0",
  "video_codec": "h264",
  "audio_codec": "aac",
  "bitrate": "5000k",
  "created": "2024-01-15 10:30:00"
}
```
