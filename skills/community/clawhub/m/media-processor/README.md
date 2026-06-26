# Media Processor - 音视频处理器

一站式音视频处理解决方案，支持格式转换、剪辑、转录、特效添加。

## 功能特性

- 🎬 **视频处理**：剪辑、合并、转码、压缩、提取音频
- 🎵 **音频处理**：格式转换、剪辑、混音、降噪、音量调节
- 📝 **语音识别**：支持 Whisper 语音转文字、字幕生成
- 🎨 **视频特效**：滤镜、水印、字幕叠加、转场效果
- 📊 **批量处理**：支持文件夹批量处理、进度监控
- 🔧 **格式支持**：MP4、AVI、MKV、MOV、MP3、WAV、FLAC 等

## 安装

```bash
pip install -r requirements.txt

# FFmpeg 安装 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install ffmpeg

# FFmpeg 安装 (macOS)
brew install ffmpeg

# Windows 下载
# https://ffmpeg.org/download.html
```

## 依赖要求

- Python 3.8+
- FFmpeg >= 4.0
- moviepy >= 1.0
- pydub >= 0.25
- librosa >= 0.10
- openai-whisper >= 20231117
- numpy >= 1.24
- Pillow >= 9.5

## 快速开始

### 视频转码

```python
from scripts.video_processor import VideoProcessor

processor = VideoProcessor()
processor.convert(
    input='input.mp4',
    output='output.avi',
    codec='h264',
    resolution='1920x1080'
)
```

### 视频剪辑

```python
from scripts.video_editor import VideoEditor

editor = VideoEditor('video.mp4')
editor.trim(start='00:01:30', end='00:03:00')
editor.add_text('字幕内容', position='center', duration=5)
editor.save('output.mp4')
```

### 语音转录

```python
from scripts.transcriber import Transcriber

transcriber = Transcriber(model='base')
text = transcriber.transcribe('audio.mp3')
transcriber.save_srt('subtitles.srt')
```

### 音频处理

```python
from scripts.audio_processor import AudioProcessor

audio = AudioProcessor('input.mp3')
audio.change_volume(1.5)
audio.remove_noise()
audio.export('output.wav', format='wav')
```

## API 文档

### VideoProcessor

```python
VideoProcessor(ffmpeg_path='ffmpeg')
```

| 方法 | 参数 | 说明 |
|------|------|------|
| convert | input, output, codec, resolution | 格式转换 |
| extract_audio | input, output | 提取音频 |
| get_info | input | 获取视频信息 |

### VideoEditor

```python
VideoEditor(video_path)
```

| 方法 | 说明 |
|------|------|
| trim(start, end) | 剪辑片段 |
| add_text(text, position) | 添加文字 |
| add_watermark(image) | 添加水印 |
| save(output) | 保存 |

## 示例

见 `examples/basic_usage.py`

## 测试

```bash
python -m pytest tests/ -v
```

## 许可证

MIT License
