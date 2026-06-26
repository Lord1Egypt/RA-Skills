# Memory Enhancer Pro for OpenClaw

**Professional memory management tool** with advanced features beyond the basic version.

**Note:** This is an enhanced version of `openclaw-memory-enhancer`, developed by @williamwg2025.

[中文版本](README.md)

---

## ✨ Features

- 🔍 Semantic search - Search all memories
- 📌 Auto-summarize - Extract key points
- 🏷️ Smart classification - Auto-categorize
- ⚡ Token optimizer - Save 30-60% tokens
- 📅 Scheduled tasks - Auto-optimize daily

---

## 🚀 Installation

```bash
cd ~/.openclaw/workspace/skills
# Skill installed at: ~/.openclaw/workspace/skills/memory-enhancer
chmod +x memory-enhancer/scripts/*.py
```

**That's it! All scripts included, no external cloning needed.**

---

## 📖 Usage

```bash
# Basic usage
python3 memory-enhancer/scripts/*.py

# Check help
python3 memory-enhancer/scripts/*.py --help
```

**Purpose:** Enhance AI memory and optimize token usage

---

## 🛠️ Scripts

| Script | Function |
|--------|----------|
| `*.py` | Main scripts (check scripts/ directory) |

---

## 🔒 Security Notes

### Code Source ✅
**All scripts included in the package:**
- ❌ No external cloning
- ❌ No downloading external code

### Network Access
- **Scripts run locally** - No network calls (unless specified)

### File Access
- **Read:** Configuration files in skill directory
- **Write:** Only when explicitly specified

### Data Security
- **Local processing** - All operations run locally
- **No upload** - No data sent to external servers

### Usage Tips
1. Check scripts/ directory for available scripts
2. Test with simple commands first
3. Don't provide sensitive information

---

**Author:** @williamwg2025  
**Version:** Check SKILL.md  
**License:** MIT-0

---

## 📁 Directory Structure

```
memory-enhancer/
├── SKILL.md          # Skill metadata and documentation
├── README.md         # Chinese documentation
├── README_EN.md      # English documentation
├── config/           # Configuration files (optional)
│   └── *.json
└── scripts/          # Script files
    ├── *.py
    └── *.sh
```

---

**Last updated:** 2026-03-13
