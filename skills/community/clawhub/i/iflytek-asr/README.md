# 讯飞语音转文本 Skill

使用科大讯飞 API 将音频文件转换为文本，支持中文方言识别。

## 功能特性

- ✅ 支持多种音频格式：mp3, wav, pcm, mp4, m4a, aac, ogg, flac, speex, opus, wma
- ✅ 支持 YouTube 视频下载并转文本
- ✅ 文件大小限制：≤500MB
- ✅ 时长限制：≤5小时
- ✅ 自动识别中文方言

## 安装步骤

### 1. 安装依赖

```bash
pip3 install yt-dlp requests python-dotenv
```

### 2. 获取讯飞 API 凭证

1. 访问 [科大讯飞开放平台](https://www.xfyun.cn)
2. 注册/登录账号
3. 创建应用，选择"语音识别"服务
4. 获取以下凭证：
   - `XFYUN_APP_ID`
   - `XFYUN_ACCESS_KEY_ID`
   - `XFYUN_ACCESS_KEY_SECRET`

### 3. 配置凭证

复制 `.env.example` 为 `.env` 并填入你的凭证：

```bash
cp .env.example .env
# 然后编辑 .env 文件，填入你的凭证
```

`.env` 文件内容示例：
```env
XFYUN_APP_ID=your_app_id_here
XFYUN_ACCESS_KEY_ID=your_access_key_id_here
XFYUN_ACCESS_KEY_SECRET=your_access_key_secret_here
```

⚠️ **注意**：`.env` 文件包含敏感信息，不要提交到 Git 仓库！

## 使用方法

### 方式 1：转录本地音频文件

```bash
python3 scripts/speech_to_text.py <音频文件路径> [输出文本路径]
```

**示例：**
```bash
# 转录 MP3 文件，输出同名 .txt
python3 scripts/speech_to_text.py recording.mp3

# 指定输出文件
python3 scripts/speech_to_text.py meeting.wav transcript.txt
```

### 方式 2：YouTube 下载音频

```bash
python3 scripts/download_audio.py "YOUTUBE_URL" [保存目录]
```

**示例：**
```bash
# 下载到当前目录
python3 scripts/download_audio.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 下载到指定目录
python3 scripts/download_audio.py "https://www.youtube.com/watch?v=VIDEO_ID" ~/Downloads
```

### 方式 3：YouTube 下载 + 自动转文本（推荐）

```bash
python3 scripts/download_and_transcribe.py "YOUTUBE_URL" [保存目录]
```

**示例：**
```bash
python3 scripts/download_and_transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" ~/Downloads
```

输出文件：
- `VIDEO_ID.mp3` - 音频文件
- `VIDEO_ID.txt` - 转录文本

## 支持的 YouTube 链接格式

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- 纯视频 ID (11个字符)

## 常见问题

### Q: 转录失败怎么办？

**检查清单：**
1. ✅ 讯飞 API 凭证配置正确
2. ✅ 音频文件格式支持
3. ✅ 文件大小 ≤500MB
4. ✅ 时长 ≤5小时
5. ✅ 网络连接正常

### Q: YouTube 下载失败 (403 Forbidden)

**可能原因：**
- 地区限制
- YouTube 限速
- 视频已删除/私密

**解决方法：**
- 使用代理/VPN
- 稍后重试

### Q: 转录速度如何？

通常比实时播放快，具体取决于：
- 音频时长
- 网络速度
- API 服务器负载

## API 使用限制

讯飞免费版限制：
- 每日调用次数：500次
- 单次文件大小：≤500MB
- 时长：≤5小时

**需要更多配额？** 访问 [讯飞控制台](https://console.xfyun.cn) 升级套餐。

## 目录结构

```
iflytek-asr-skill/
├── README.md              # 本文档
├── .env.example           # 凭证模板
├── .env                   # 你的凭证（不要提交到Git）
└── scripts/
    ├── speech_to_text.py           # 音频转文本
    ├── download_audio.py           # YouTube下载音频
    └── download_and_transcribe.py  # YouTube下载+转文本
```

## 安全提醒

⚠️ **敏感信息保护**
- `.env` 文件包含你的 API 凭证
- 不要分享或提交到公开仓库
- 建议在 `.gitignore` 中添加 `.env`

## 许可证

MIT License

## 支持与反馈

有问题？欢迎提交 Issue 或 PR！
