<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/QiaoTuCodes/openclaw-skill-whisper-stt/main/assets/openclaw-skill-logo.png">
        <img src="https://raw.githubusercontent.com/QiaoTuCodes/openclaw-skill-whisper-stt/main/assets/openclaw-skill-logo.png" alt="OpenClaw Skill" width="500">
    </picture>
</p>

<p align="center">
  <strong>🎙️ Speech-to-Text Skill for OpenClaw</strong>
</p>

<p align="center">
  <a href="https://github.com/QiaoTuCodes/openclaw-skill-whisper-stt/releases"><img src="https://img.shields.io/github/v/release/QiaoTuCodes/openclaw-skill-whisper-stt?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://github.com/QiaoTuCodes/openclaw-skill-whisper-stt/stargazers"><img src="https://img.shields.io/github/stars/QiaoTuCodes/openclaw-skill-whisper-stt?style=for-the-badge" alt="Stars"></a>
</p>

A speech-to-text skill for OpenClaw using OpenAI's Whisper model to convert audio to text.

## ✨ Features

- 🎙️ **Speech Recognition** - Convert audio to text
- 🌍 **Multilingual** - Support for 100+ languages
- 🇨🇳 **Chinese Optimized** - Excellent Chinese recognition
- ⚡ **Multiple Models** - Choose from tiny to large models

## 📦 Installation

```bash
# Clone this skill to your OpenClaw workspace
cp -r openclaw-skill-whisper-stt ~/openclaw-workspace/skills/

# Install dependencies
pip3 install openai-whisper
brew install ffmpeg  # macOS
# or: sudo apt install ffmpeg  # Ubuntu
```

## 🚀 Quick Start

```python
import whisper

# Load model (first use downloads model)
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.mp3", language="zh")

# Get text
text = result["text"]
print(text)
```

## CLI Usage

```bash
# Basic transcription
python3 transcribe.py -i audio.mp3

# With specific model
python3 transcribe.py -i audio.mp3 -m small

# Save output to file
python3 transcribe.py -i audio.mp3 -o result.txt
```

## 📖 Documentation

- [English README](README.md)
- [中文文档](README-CN.md)
- [Skill Definition](SKILL.md)

## 🔧 Requirements

- Python 3.8+
- PyTorch
- openai-whisper
- FFmpeg

## 📂 Project Structure

```
openclaw-skill-whisper-stt/
├── SKILL.md           # OpenClaw skill definition
├── transcribe.py      # Main Python module
├── README.md          # English documentation
├── README-CN.md       # Chinese documentation
├── LICENSE            # MIT License
└── .gitignore
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 👥 Authors

- **Isaac** - [GitHub](https://github.com/QiaoTuCodes)
- **焱焱 (Yanyan)** - yanyan@3c3d77679723a2fe95d3faf9d2c2e5a65559acbc97fef1ef37783514a80ae453

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) team
- [OpenClaw](https://github.com/openclaw/openclaw) team

---

<p align="center">
  <sub>Built with ❤️ for the OpenClaw community</sub>
</p>
