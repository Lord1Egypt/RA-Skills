# li_PhotoIndexWithLLM

📸 Smart photo indexing and search system powered by VL (Vision-Language) large models.

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
