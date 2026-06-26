---
name: Heartbeat Memories
slug: heartbeat-memories
version: 1.0.0
author: JamieYang9996
description: >
  Heartbeat-Memories (HBM) - A fully local long-term memory system for OpenClaw.
  Features five memory banks (Goals/Experience/Emotions/Session/Version) + heartbeat recall mechanism.
  No API keys, no token consumption, 100% local operation.
triggers:
  - "memory system, long-term memory, help me recall"
  - "save this, check goals, how did we solve this"
  - "mood recording, habit observation"
  - "记忆系统, 长期记忆, 帮我回忆"
  - "记下来, 查看目标, 上次怎么解决的"
  - "心情记录, 习惯观察"
---

# Heartbeat-Memories (HBM) - OpenClaw Skill

**Solving the pain points of scattered memory files and emotionless AI responses**  
Through **five specialized memory banks** + **heartbeat recall simulation dialogue**, making your OpenClaw truly understand you, remember you, and build exclusive emotional connections.

## 🚀 One-Click Installation (Manual)

### Option 1: Install via Git
```bash
# Clone the repository
git clone https://github.com/JamieYang9996/Heartbeat-Memories.git

# Copy to OpenClaw skills directory (adjust path as needed)
cp -r Heartbeat-Memories ~/.openclaw/skills/heartbeat-memories

# Initialize the memory system
cd ~/.openclaw/skills/heartbeat-memories && python3 scripts/hbm_init.py
```

### Option 2: Manual installation
1. Download this skill folder
2. Place it in your OpenClaw skills directory: `~/.openclaw/skills/`
3. Run initialization: `python3 scripts/hbm_init.py`

### Option 3: Via ClawHub (if published)
```bash
openclaw skill install heartbeat-memories
```

## 🔄 Update

```bash
# Update from Git
cd ~/.openclaw/skills/heartbeat-memories && git pull origin main

# Re-initialize if needed
python3 scripts/hbm_init.py --upgrade
```

## 🩺 System Diagnostics

```bash
# Run diagnostic check
cd ~/.openclaw/skills/heartbeat-memories && python3 scripts/hbm_doctor.py
```

## 📁 System Architecture

```
heartbeat-memories/
├── SKILL.md                    # This file
├── README.md                   # Detailed documentation
├── memory/                     # Memory bank templates
│   ├── 目标记忆库/GOALS_template.md
│   ├── 经验记忆库/TIPS_template.md  
│   ├── 情感记忆库/DAILY_EMOTIONS_template.md
│   ├── 会话记忆库/YYYY-MM-DD_template.md
│   ├── 版本记忆库/CHANGELOG_template.md
│   └── 心跳回忆/心跳回忆机制.md
├── scripts/                    # Core scripts
│   ├── hbm_init.py            # Initialization script
│   ├── local_memory_system_v2.py
│   └── rag_system.py
├── config/                     # Configuration files
│   └── hbm_config_template.json
└── requirements.txt            # Python dependencies
```

## 🎯 Core Features

### 1. Five Memory Banks (Automatic Recording)
- **Goals Memory**: Tracks user goals with P0/P1/P2 priorities
- **Experience Memory**: Records technical problems and solutions
- **Emotion Memory**: Analyzes user emotions and habit preferences
- **Session Memory**: Daily conversation summaries (10:1 compression ratio)
- **Version Memory**: System change history records

### 2. Semantic Search (Vector Retrieval)
- Based on ChromaDB vector database
- Natural language query of memory content
- Local model: all-MiniLM-L6-v2 (80MB, auto-download from ModelScope)

### 3. Heartbeat Recall Emotional Interaction (Core Innovation)
**Solves AI's lengthy, emotionless responses by mimicking human conversation for long-term connections**

#### 🎭 Highly Realistic Human Interaction
- **Smart Triggering**: AI actively recalls like a friend (e.g., "By the way, remember last week's 'seaside café' 'sunset' 'photos', did you end up going?")
- **Natural Conversation Flow**: Randomly inserts memories during daily chats (30% probability), avoiding mechanical feel
- **Emotional Intelligence**: Analyzes user emotional state, adjusts interaction style

#### ⚙️ Flexible Configurable System
- **Configurable Probabilities**: Each trigger scene has adjustable probability (30%/50%/100%)
- **Frequency Control**: Daily limits, minimum intervals, special holiday rules
- **Scene Customization**: Supports daily conversation, task completion, forgotten goals, holiday care, etc.
- **Sensitive Day Avoidance**: Automatically avoids sensitive holidays like Qingming Festival

#### 🌱 Long-term Cultivation & Exclusivity
- **Habit Learning**: Records user work patterns, preferred topics, common keywords
- **Exclusive Memories**: Builds personalized memory bank based on historical conversations
- **Progressive Optimization**: Continuously optimizes trigger timing and wording through silent review
- **Emotional Evolution**: AI understands users better over time, building real "long-term relationships"

### 4. RAG Retrieval Augmentation (Optional)
- Improves answer accuracy and relevance
- Retrieves context from memory banks
- Configurable switch controls (default: OFF)

## 🔧 Usage

### Basic Usage (Out-of-the-box)
After installation, Heartbeat-Memories automatically:
1. Records important conversations to memory banks
2. Responds to trigger words for retrieval
3. Maintains memory bank integrity

### Common Trigger Word Examples
```
User: "Save this, I want to learn Python"
AI: ✅ Recorded to Goals Memory

User: "How did we solve that server issue last time?"
AI: 🔍 Retrieved solution from Experience Memory...

User: "Check my goals for today"
AI: 📄 Reading from Goals Memory...

User: "Help me recall things we discussed last week"
AI: ❤️ Remember last week's "seaside café"...
```

### Advanced Configuration (Optional)
```bash
# 1. Modify configuration
vim ~/.openclaw/skills/heartbeat-memories/config/hbm_config.json

# 2. Custom memory location
export HBM_MEMORY_PATH="~/my-memories"
```

## ⚙️ Technical Specifications

| Component | Specification | Description |
|-----------|---------------|-------------|
| **Vector Database** | ChromaDB + SQLite | Fully local storage |
| **Text Vectorization** | all-MiniLM-L6-v2 | 384 dimensions, 80MB |
| **Model Download Source** | ModelScope (China mirror) | Fast and stable |
| **Storage Format** | Markdown (.md) | Human readable |
| **Cross-platform Support** | Windows/Linux/macOS | Auto-adapts paths |
| **Dependencies** | Python 3.8+ | chromadb, sentence-transformers |

## 🐛 Troubleshooting

### Common Issues

**Q: No response after installation?**
A: Ensure correct directory: `~/.openclaw/skills/heartbeat-memories/`, restart OpenClaw.

**Q: Model download failed?**
A: Manual download: `python3 scripts/download_model.py`, or use mirror sources.

**Q: Insufficient storage space?**
A: Memory bank files are small, vector model 80MB, RAG logs auto-compress monthly.

**Q: Cross-platform compatibility?**
A: Adapted for Windows (WSL/Git Bash), Linux, macOS, auto-detects system.

### Diagnostic Commands
```bash
# Check Heartbeat-Memories status
cd ~/.openclaw/skills/heartbeat-memories && python3 scripts/hbm_init.py --check

# View memory banks
ls -la ~/.openclaw/skills/heartbeat-memories/memory/

# Test semantic search
python3 scripts/local_memory_system_v2.py --test
```

## 📈 Advanced Features

### RAG System Optimization (Optional)
- **Token Limit & Deduplication**: Prevents overly long answers (default: OFF)
- **Memory Cache**: Improves retrieval speed (default: OFF)
- **Log Compression**: Auto-compresses log files monthly

### Custom Extensions
```python
# Extend new memory bank types
# Add new collections in scripts/local_memory_system_v2.py

# Custom trigger logic
# Modify trigger conditions in 心跳回忆/心跳回忆机制.md
```

## 🛡️ Security & Privacy Statement (Required by ClawHub)

### ✅ 100% Local Operation
- All data stored locally on user's machine
- No data uploaded to any servers
- No API calls to external services

### ✅ No Automatic Background Processes
- **No cron jobs** - All operations are manually triggered by user or OpenClaw
- **No system services** - No daemons or background processes
- **No auto-start** - Does not run automatically on system boot

### ✅ No Privilege Escalation
- Operates only within skill directory and user workspace
- Does not access system files or other user directories
- All file operations are within permitted scope

### ✅ Transparent Installation
- All dependencies listed in requirements.txt
- No silent installation of packages
- Clear prompts for user confirmation

### ✅ Data Ownership
- Users own all their memory data
- Can export/backup memory banks at any time
- Can completely uninstall without data loss (manual backup recommended)

## 🤝 Contribution & Feedback

### GitHub Repository
- Project URL: https://github.com/JamieYang9996/Heartbeat-Memories
- Issues: Report problems or suggest features
- Pull Requests: Code contributions welcome

### Community Support
- OpenClaw Discord: https://discord.com/invite/clawd
- Chinese discussion: Telegram/WeChat groups (if available)

## 📝 License

MIT License - See LICENSE file

---

**Heartbeat-Memories gives your OpenClaw true long-term memory, making it a smarter assistant that truly understands you!**

*Last updated: 2026-03-25*