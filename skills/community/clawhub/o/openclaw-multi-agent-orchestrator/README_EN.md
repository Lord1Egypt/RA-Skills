# Multi-Agent Orchestrator

Manage and coordinate multiple AI agents.

[中文版本](README.md)

---

## ✨ Features

- 🤖 Agent registration - Auto-discover agents
- 🔄 Task dispatch - Smart routing
- 📊 Load balancing - Balance agent loads
- 💬 Agent communication - Inter-agent messaging

---

## 🚀 Installation

```bash
cd ~/.openclaw/workspace/skills
# Skill installed at: ~/.openclaw/workspace/skills/multi-agent-orchestrator
chmod +x multi-agent-orchestrator/scripts/*.py
```

**That's it! All scripts included, no external cloning needed.**

---

## 📖 Usage

```bash
# Basic usage
python3 multi-agent-orchestrator/scripts/*.py

# Check help
python3 multi-agent-orchestrator/scripts/*.py --help
```

**Purpose:** Orchestrate multiple AI agents

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
multi-agent-orchestrator/
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
