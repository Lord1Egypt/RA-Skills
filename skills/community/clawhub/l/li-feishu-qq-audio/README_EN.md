# li-feishu-audio Skill

Feishu (Lark) Voice Interaction Skill - Complete solution for automatic voice message recognition, AI processing, and voice reply.

**Author**: 北京老李 (BeijingLL)  
**Version**: 0.1.4  
**Release Date**: 2026-03-22  
**Update**: v0.1.4 Comprehensive log management, debug info isolation, model selection

---

## 📖 Introduction

This skill provides complete Feishu voice interaction capabilities:

```
User Voice → faster-whisper Recognition → AI Processing → Edge TTS Synthesis → OPUS Conversion → Feishu Send
```

**Core Features**:
- ✅ Automatic voice message recognition (faster-whisper 1.2.1)
- ✅ AI intelligent reply (supports major LLMs)
- ✅ Voice synthesis reply (Edge TTS 7.2.7)
- ✅ Automatic format conversion (MP3 → OPUS)
- ✅ Feishu channel integration
- ✅ Automatic temporary file cleanup
- ✅ Support custom directories
- ✅ No root privileges required

---

## 🚀 Quick Start

### Installation

```bash
# Install from clawhub
skillhub install li-feishu-audio
```

### Configure Environment Variables

**Required Environment Variables**:

| Variable | Purpose | How to Get |
|----------|---------|------------|
| `FEISHU_APP_ID` | Feishu App ID | [Feishu Open Platform](https://open.feishu.cn/) |
| `FEISHU_APP_SECRET` | Feishu App Secret | [Feishu Open Platform](https://open.feishu.cn/) |

**Optional Environment Variables**:

| Variable | Default | Description |
|----------|---------|-------------|
| `FAST_WHISPER_MODEL_DIR` | `$HOME/.fast-whisper-models` | Voice model storage directory |
| `VENV_DIR` | `skill-dir/.venv` | Python virtual environment directory |
| `TEMP_DIR` | `/tmp` | Temporary file directory |
| `LOG_DIR` | `skill-dir/logs` | Log directory |
| `OPENCLAW_CONFIG` | `$HOME/.openclaw/openclaw.json` | OpenClaw config file |
| `HF_ENDPOINT` | `https://hf-mirror.com` | HuggingFace mirror (China acceleration) |

**Configuration Method**:

```bash
# 1. Copy configuration template
cd skills/li-feishu-audio/scripts
cp .env.example .env

# 2. Edit configuration file
vi .env

# 3. Fill in actual values
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

# 4. Load environment variables
source .env
```

### Run Installation

```bash
./scripts/install.sh
```

The installation script will:
1. ✅ Check system dependencies (Python, uv, ffmpeg, jq)
2. ✅ Create Python virtual environment
3. ✅ Install Python packages (faster-whisper, edge-tts)
4. ✅ Download voice model
5. ✅ Create configuration template
6. ✅ Verify Feishu credentials

### Test

```bash
# Restart OpenClaw gateway
openclaw gateway restart

# Send voice message to Feishu
# Wait for automatic recognition and voice reply
```

---

## 📁 Directory Structure

```
li-feishu-audio/
├── SKILL.md              # Technical documentation
├── README.md             # Chinese usage guide
├── README_EN.md          # English usage guide (this file)
├── SECURITY.md           # Security guide and audit instructions
├── .gitignore            # Git ignore file
└── scripts/
    ├── .env.example      # Environment variable template
    ├── install.sh        # Auto-installation script
    ├── fast-whisper-fast.sh  # Voice recognition
    ├── tts-voice.sh      # TTS generation
    ├── feishu-tts.sh     # Feishu sending
    └── cleanup-tts.sh    # Cleanup script
```

---

## 📋 System Requirements

| Component | Requirement | Auto-install |
|-----------|-------------|--------------|
| OS | Linux (Ubuntu/Debian) | ❌ |
| Python | 3.11+ | ❌ |
| uv | Any version | ❌ |
| ffmpeg | Any version | ✅ |
| jq | Any version | ✅ |

**Privilege Requirements**: No root privileges required

---

## 🔧 Scripts

### install.sh

Automatic installation script:

```bash
./scripts/install.sh
```

**Steps**:
1. Check system dependencies
2. Create Python virtual environment
3. Install Python packages
4. Download voice model
5. Create configuration template
6. Verify Feishu credentials

### fast-whisper-fast.sh

Voice recognition script:

```bash
./scripts/fast-whisper-fast.sh <audio_file.ogg>
```

**Output**:
```
[0.00s -> 2.32s] Recognized text content
```

### tts-voice.sh

TTS voice generation script:

```bash
./scripts/tts-voice.sh "Text content" [output_file.mp3]
```

### feishu-tts.sh

Feishu voice sending script (auto OPUS conversion):

```bash
./scripts/feishu-tts.sh <audio_file.mp3> <user_open_id>
```

### cleanup-tts.sh

Temporary file cleanup script:

```bash
./scripts/cleanup-tts.sh [keep_count]

# Cron job (optional)
0 2 * * * ./scripts/cleanup-tts.sh 10
```

---

## ⚙️ Configuration

### Feishu Credentials

**Method 1: Environment Variables** (Recommended)

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**Method 2: openclaw.json**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

**⚠️ Security Tip**: Do not commit credentials to version control!

### Custom Directories (Optional)

Configure in `.env` file:

```bash
# Model directory (default: $HOME/.fast-whisper-models)
export FAST_WHISPER_MODEL_DIR="/opt/fast-whisper-models"

# Virtual environment directory (default: skill-dir/.venv)
export VENV_DIR="/path/to/venv"

# Temporary file directory (default: /tmp)
export TEMP_DIR="/tmp"

# Log directory (default: skill-dir/logs)
export LOG_DIR="/path/to/logs"
```

---

## 🔒 Security

**For detailed security information, see**: [SECURITY.md](SECURITY.md)

### Credential Management

- ✅ Use environment variables for sensitive credentials
- ✅ Do not commit `.env` to version control
- ✅ Add `.env` to `.gitignore`
- ✅ Rotate credentials regularly (recommended every 3-6 months)

### Privilege Information

- ✅ No root privileges required
- ✅ All directories use user home directory (`$HOME/`)
- ✅ Virtual environment in skill directory

### Network Access

| Service | URL | Purpose |
|---------|-----|---------|
| Feishu API | `https://open.feishu.cn/` | Send voice messages |
| HuggingFace Mirror | `https://hf-mirror.com/` | Download voice model |
| Microsoft Edge TTS | `https://speech.platform.bing.com/` | Voice synthesis |

---

## 🛠️ Troubleshooting

### Voice Recognition Failed

**Check**:
1. Model downloaded: `ls $FAST_WHISPER_MODEL_DIR/`
2. Virtual environment: `skill-dir/.venv/bin/python --version`
3. Network: `export HF_ENDPOINT=https://hf-mirror.com`

### TTS Generation Failed

**Check**:
1. edge-tts installed: `uv pip list -p skill-dir/.venv | grep edge`
2. Network connection: Edge TTS requires access to Microsoft services

### Feishu Send Failed

**Check**:
1. Credentials configured: `echo $FEISHU_APP_ID`
2. Audio format: Must be OPUS
3. User ID type: Use open_id

---

## 📊 Performance Metrics

| Operation | Duration |
|-----------|----------|
| Voice Recognition (tiny) | ~8-10 seconds |
| TTS Generation | ~3-5 seconds |
| OPUS Conversion | <1 second |
| Feishu Upload | ~2-3 seconds |
| **Total** | **~15 seconds** |

---

## 📝 Version History

### v0.1.4 (Current)

| Version | Date | Changes |
|---------|------|---------|
| **0.1.4** | **2026-03-22** | **Comprehensive Log Management**: Debug info isolated to log files, weekly auto-cleanup, model selection (tiny/base/small/medium), fixed file path leakage |

### Historical Versions

| Version | Date | Changes |
|---------|------|---------|
| **0.1.1** | **2026-03-17** | **Documentation Enhanced** (README.md and README_EN.md fully updated) |
| **0.1.0** | **2026-03-17** | **Security Enhanced** (default paths use $HOME/, env vars declared, SECURITY.md added) |

~~0.0.1 - 0.0.10: Initial development versions~~

---

## 📞 Support

- **Security Docs**: [SECURITY.md](SECURITY.md)
- **Skill Docs**: [SKILL.md](SKILL.md)
- **OpenClaw Docs**: https://docs.openclaw.ai
- **Feishu Open Platform**: https://open.feishu.cn/document

---

## 📋 Author

**北京老李 (BeijingLL)**

---

**Last Updated**: 2026-03-17  
**Version**: 0.0.9
