# senseaudio-voice 技能说明

## 版本更新

### v2.1.0 (2026-03-15) - 多语言支持

**新增功能**:
- ✅ 自动语言检测（中文/英语/日语）
- ✅ Edge TTS 集成（英语/日语支持）
- ✅ 智能引擎选择（根据语言自动切换）

**使用策略**:
| 语言 | TTS 引擎 | 说明 |
|------|---------|------|
| 中文 | SenseAudio | 需要大陆手机号 + 身份认证，免费使用 |
| 英语 | Edge TTS | 海外友好，无需认证 |
| 日语 | Edge TTS | 海外友好，无需认证 |

**依赖**:
```bash
pip install edge-tts  # 英语/日语 TTS
pip install requests  # SenseAudio HTTP 调用
```

**使用示例**:
```bash
# 自动检测语言（推荐）
python tts.py --play "你好，宝贝"           # 中文 → SenseAudio
python tts.py --play "Hello, sweetheart"   # 英语 → Edge TTS
python tts.py --play "こんにちは"          # 日语 → Edge TTS

# 强制指定引擎
python tts.py --engine edge --play "English test"
python tts.py --engine senseaudio --play "中文测试"

# 指定声音
python tts.py --voice en-US-GuyNeural --play "Hello"
python tts.py --voice ja-JP-KeitaNeural --play "こんにちは"
```

---

### v2.0.0 - HTTP 接口版本

- 使用 SenseAudio HTTP API
- 支持 WAV/MP3 格式
- 自动播放器检测

---

## 配置说明

### SenseAudio API Key

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "env": {
    "SENSE_API_KEY": "your_api_key_here"
  }
}
```

**获取方式**: 
1. 访问 https://senseaudio.cn
2. 注册账号并完成身份认证（需要大陆手机号）
3. 在控制台获取 API Key

### Edge TTS

无需配置，直接可用。

---

## 技术细节

### 语言检测逻辑

```python
def detect_language(text):
    # 统计字符类型
    - 中文字符 (CJK Unified Ideographs: 0x4E00-0x9FFF)
    - 日文假名 (Hiragana + Katakana: 0x3040-0x30FF)
    - 拉丁字母 (ASCII: 0x0041-0x007A)
    
    # 判断优先级
    1. 日语（有假名且假名 >= 中文）
    2. 中文（有汉字且汉字 >= 拉丁字母）
    3. 英语（默认，拉丁字母为主）
```

### 引擎选择逻辑

```python
def select_engine(lang, force_engine):
    if force_engine != "auto":
        return force_engine
    
    if lang == "zh":
        return "senseaudio"  # 中文用 SenseAudio
    elif lang in ["en", "ja"]:
        return "edge"        # 英语/日语用 Edge TTS
    else:
        return "edge"        # 未知语言默认 Edge TTS
```

---

## 故障排除

### 中文 TTS 失败
- 检查 `SENSE_API_KEY` 是否配置
- 确认 API Key 是否有效（需要身份认证）
- 检查网络连接

### 英语/日语 TTS 失败
- 安装 `edge-tts` 库：`pip install edge-tts`
- 检查网络连接（需要访问 Microsoft 服务）

### 播放器问题
```bash
# 检查可用播放器
python tts.py --check-players

# 安装推荐播放器
sudo apt-get install alsa-utils    # aplay (WAV 原生支持)
sudo apt-get install pulseaudio    # paplay
sudo apt-get install ffmpeg        # ffplay (多格式支持)
```
