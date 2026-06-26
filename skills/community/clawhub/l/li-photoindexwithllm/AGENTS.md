# li_PhotoIndexWithLLM

📸 Smart photo indexing and search system powered by VL (Vision-Language) large models.

## 🌍 Multilingual Support / 多语言支持

This skill supports 10 major languages:

| Language | 语言 | 说明 |
|----------|------|------|
| 🇨🇳 中文 | Chinese | [查看说明](README_MULTILINGUAL.md#-中文简体) |
| 🇺🇸 English | English | [View Guide](README_MULTILINGUAL.md#-english) |
| 🇯🇵 日本語 | Japanese | [表示](README_MULTILINGUAL.md#-日本語) |
| 🇰🇷 한국어 | Korean | [보기](README_MULTILINGUAL.md#-한국어) |
| 🇫🇷 Français | French | [Voir](README_MULTILINGUAL.md#-français) |
| 🇩🇪 Deutsch | German | [Ansehen](README_MULTILINGUAL.md#-deutsch) |
| 🇪🇸 Español | Spanish | [Ver](README_MULTILINGUAL.md#-español) |
| 🇷🇺 Русский | Russian | [Просмотр](README_MULTILINGUAL.md#-русский) |
| 🇸🇦 العربية | Arabic | [عرض](README_MULTILINGUAL.md#-العربية) |
| 🇧🇷 Português | Portuguese | [Ver](README_MULTILINGUAL.md#-português) |

📖 **完整多语言文档**: [README_MULTILINGUAL.md](README_MULTILINGUAL.md)

## Summary

Scan your photo directories, analyze content using local/remote VL models, build structured indexes, and search photos using natural language queries.

## Cross-Platform Support

✅ **Windows 10/11** - Full support  
✅ **Ubuntu 20.04/22.04/24.04** - Full support  
✅ **Linux** - Supported (Python 3.10+)  
✅ **macOS 12+** - Supported (Intel/Apple Silicon)

### Platform-Specific Paths

**Windows:**
```bash
python skill.py scan --dir D:\Photos
python skill.py scan --dir C:\Users\User\Pictures
```

**Ubuntu/Linux:**
```bash
python3 skill.py scan --dir /home/user/Photos
python3 skill.py scan --dir /mnt/external/Photos
```

**macOS:**
```bash
python3 skill.py scan --dir /Users/user/Photos
```

## Privacy-First Design

- **Local-only by default**: Photos NEVER leave your machine unless explicitly configured
- **User consent required**: Remote model usage requires explicit confirmation
- **No data collection**: All data stays in your local SQLite database
- **API keys local only**: Stored in `.env` file, never transmitted except to LLM endpoints you configure

## Quick Start

```bash
# Install dependencies
pip install requests  # or pip3 on Linux/macOS

# Scan photos
python skill.py scan --dir D:\Photos        # Windows
python3 skill.py scan --dir ~/Photos        # Linux/macOS

# Search photos
python skill.py search "beach sunset"

# JSON output for agents
python skill.py search "beach" --format json
```

## Requirements

- Python 3.10+
- `requests` library
- LM Studio (for local VL models, optional but recommended)

## Author

Beijing Lao Li (beijingLL)

## License

MIT
