# MOSS-TTS Voice

> 🎙️ MOSS-TTS 语音合成与音色克隆工具

## 功能

- **文本转语音** - 将文本转换为自然语音
- **实时克隆** - 从音频即时克隆声音
- **预注册音色** - 保存音色供后续使用
- **格式转换** - 自动转换为各渠道格式

> ⚠️ **注意**：本工具生成音频文件，发送到各渠道需要配合其他工具

---

## 安装

### 1. 获取 API Key

访问 https://studio.mosi.cn → 注册 → API 密钥 → 创建

```bash
export MOSS_API_KEY="sk-你的密钥"
```

### 2. 安装依赖

```bash
# 系统依赖
brew install python3 ffmpeg

# Python 依赖
pip3 install -r requirements.txt
```

---

## 使用

### 实时克隆

```bash
python3 scripts/tts.py \
  --text "你好" \
  --reference_audio "voice.ogg" \
  --channel feishu \
  --json
```

### 预注册音色（推荐）

```bash
# 1. 上传音频
curl -X POST https://studio.mosi.cn/api/v1/files/upload \
  -H "Authorization: Bearer $MOSS_API_KEY" \
  -F "file=@voice.ogg"
# → {"file_id": "YOUR_FILE_ID"}

# 2. 克隆
curl -X POST https://studio.mosi.cn/api/v1/voice/clone \
  -H "Authorization: Bearer $MOSS_API_KEY" \
  -d '{"file_id": "YOUR_FILE_ID", "name": "我的声音"}'
# → {"voice_id": "YOUR_VOICE_ID"}

# 3. 使用
python3 scripts/tts.py \
  --text "你好" \
  --voice_id "YOUR_VOICE_ID" \
  --channel feishu
```

---

## 输出格式

| 渠道 | 格式 |
|------|------|
| 飞书 | ogg (opus) |
| Telegram | ogg (opus) |
| WhatsApp | ogg (opus) |
| Discord | mp3 |
| Signal | mp3 |
| Slack | mp3 |

---

## 参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `--text` | 待合成文本 | ✅ |
| `--reference_audio` | 参考音频 | 二选一 |
| `--voice_id` | 预注册音色 ID | 二选一 |
| `--channel` | 目标渠道 | ❌ |
| `--format` | 输出格式 | ❌ |
| `--output` | 输出路径 | ❌ |
| `--json` | JSON 输出 | ❌ |

---

## ⚠️ 隐私与安全

### API Key
- 不要提交到 Git
- 使用环境变量
- 定期轮换

### 语音数据
- 克隆会上传音频到 MOSS Studio
- 避免上传敏感录音
- 定期清理不需要的音色

---

## 音频要求

- **格式**: ogg, mp3, wav, m4a
- **时长**: 10-30 秒（推荐 20+ 秒）
- **音质**: 清晰人声，无噪音
- **大小**: < 10MB

---

## 更新日志

- **1.2.0** (2026-03-10) - 音色克隆、格式支持
- **1.0.0** - 初始版本

---

## License

MIT
