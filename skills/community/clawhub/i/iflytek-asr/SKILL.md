---
name: iflytek-asr
description: 使用科大讯飞 API 将音频/视频转换为文字。支持本地音频文件转录、YouTube 视频下载并转文字。适用于会议记录、视频字幕、语音笔记等场景。当用户需要语音转文字、音频转录、YouTube 视频转文字时触发。
license: MIT
acceptLicenseTerms: yes
---

# 讯飞语音转文字 (iFlytek ASR)

使用科大讯飞语音识别 API 将音频文件转换为文本，支持中文方言识别。

## 功能特性

- ✅ 支持多种音频格式：mp3, wav, pcm, mp4, m4a, aac, ogg, flac, speex, opus, wma
- ✅ 支持 YouTube 视频下载并转文本
- ✅ 文件大小限制：≤500MB
- ✅ 时长限制：≤5小时
- ✅ 自动识别中文方言
- ✅ 自动添加标点符号

## 前置要求

### 1. 获取讯飞 API 凭证

1. 访问 [科大讯飞开放平台](https://www.xfyun.cn)
2. 注册/登录账号
3. 创建应用，选择「语音转写」服务
4. 获取凭证：
   - `XFYUN_APP_ID`
   - `XFYUN_ACCESS_KEY_ID`
   - `XFYUN_ACCESS_KEY_SECRET`

### 2. 配置环境变量

在 skill 目录下创建 `.env` 文件：

```env
XFYUN_APP_ID=your_app_id
XFYUN_ACCESS_KEY_ID=your_access_key_id
XFYUN_ACCESS_KEY_SECRET=your_access_key_secret
```

### 3. 安装依赖

```bash
pip3 install yt-dlp requests python-dotenv
```

## 使用方法

### 转录本地音频

```bash
python3 scripts/speech_to_text.py <音频文件路径> [输出文本路径]
```

示例：
```bash
python3 scripts/speech_to_text.py meeting.mp3
python3 scripts/speech_to_text.py recording.wav output.txt
```

### YouTube 视频转文字

```bash
python3 scripts/download_and_transcribe.py "YOUTUBE_URL" [保存目录]
```

示例：
```bash
python3 scripts/download_and_transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" ~/Downloads
```

### 仅下载 YouTube 音频

```bash
python3 scripts/download_audio.py "YOUTUBE_URL" [保存目录]
```

## 对比：讯飞 vs Whisper

| 特性 | 讯飞 ASR | Whisper |
|------|---------|---------|
| 成本 | API 配额（有免费额度） | 免费 |
| 离线 | ❌ 需要网络 | ✅ 本地运行 |
| 速度 | ⭐⭐⭐⭐⭐ 快 | ⭐⭐⭐ 较慢 |
| 中文准确率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 标点符号 | ✅ 自动添加 | ❌ 无 |
| 方言支持 | ✅ 支持 | ⭐⭐ 一般 |

**建议：**
- 重要会议/采访 → 讯飞（准确率高、有标点）
- 日常语音消息 → Whisper（免费、无限制）

## API 限制

讯飞免费版：
- 每日调用次数：500 次
- 单次文件大小：≤500MB
- 单次时长：≤5小时

## 文件结构

```
iflytek-asr/
├── SKILL.md           # 本文档
├── README.md          # 详细说明
├── QUICKSTART.md      # 快速开始
├── .env.example       # 配置模板
├── requirements.txt   # Python 依赖
└── scripts/
    ├── speech_to_text.py           # 音频转文字
    ├── download_audio.py           # YouTube 下载
    └── download_and_transcribe.py  # 下载+转文字
```

## 常见问题

**Q: 转录失败怎么办？**
- 检查 API 凭证是否正确
- 确认文件格式支持
- 检查网络连接

**Q: 如何提高准确率？**
- 确保音频清晰
- 选择正确的语言/方言
- 避免背景噪音

## 许可证

MIT License
