# Heartbeat-Memories (HBM) - OpenClaw Skill

<div align="center">

![HBM Logo](https://img.shields.io/badge/HBM-Heartbeat%20Memories-blue)
![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

**A fully local long-term memory system** that makes your OpenClaw remember important conversations, goals, experiences, and emotions.

</div>

## 🚀 Quick Answers for New Users

| Common Question | Short Answer |
|-----------------|--------------|
| **Does it conflict with existing memory systems?** | ❌ **No**, perfect collaboration: original system handles short-term memory, HBM handles long-term structured memory |
| **Is installation complex?** | 🚀 **One-click installation**, works out of the box, 90% users need no extra configuration |
| **Does it take a lot of disk space?** | 📦 **Lightweight**, about 100MB space (model 80MB + code 20MB) |
| **Is heartbeat recall annoying?** | ⚙️ **Smart triggering**, adjustable frequency, supports silent mode, auto-pauses during emergencies |
| **Is my private data safe?** | 🔒 **100% local**, zero data upload, zero API calls, all data stays on your computer |
| **What platforms are supported?** | 💻 **Cross-platform**: Windows (WSL/Git Bash), Linux, macOS |
| **Need extra API Keys?** | 🆓 **Zero cost**, completely free and open source, no API Keys needed |
| **How to uninstall?** | 🗑️ **Simple deletion**, just remove the directory, no traces left |

## 🎯 Why Heartbeat-Memories?

### Pain Point 1: Traditional Memory files are too primitive
You may have tried using `.memory` or `.txt` files to record AI conversations, but quickly found:
- **Scattered and disorganized**: Everything in one file, hard to find
- **Lack of structure**: Goals, experiences, emotions mixed together, hard to categorize
- **Cannot be contextualized**: Cannot handle different usage scenarios (project tracking, problem solving, emotion recording)

### Pain Point 2: AI always gives long responses, wasting resources and lacking emotion
Have you noticed these problems with AI assistants?
- **Long-winded responses**: Every answer is like writing a paper, wasting tokens and attention
- **Mechanical repetition**: Same technical problems need re-explaining every time
- **Lack of emotion**: AI feels like a cold database, doesn't understand your emotions and habits
- **No exclusivity**: Every conversation starts "from scratch", cannot build long-term relationships

### ✨ Solution: Fine-grained decomposition + Emotional interaction
Heartbeat-Memories solves these problems through **five specialized memory banks** + **heartbeat recall emotional interaction**:

📝 **"What was that project goal we discussed last week?"** → Goals Memory tracks progress in real time
🎯 **"I said I wanted to learn Python, what's the progress now?"** → Goals categorized P0/P1/P2 priorities, auto-reminders
🔧 **"How did we solve that server 502 error last time?"** → Experience Memory accumulates best practices, avoids repeating mistakes
💭 **"Help me recall creative ideas we discussed last month"** → Session Memory smart summaries, 10:1 compression ratio for quick search
❤️ **"How have I been feeling lately? Any habit changes?"** → Emotion Memory analyzes emotional patterns, AI understands you better

Traditional AI chatbots start "from scratch" every session. Heartbeat-Memories makes OpenClaw truly understand you, remember you, and become your exclusive intelligent assistant through **five memory banks contextual decomposition + heartbeat recall emotional connection**.

## ✨ What is Heartbeat-Memories?

**Heartbeat-Memories (HBM)** is a **fully local AI long-term memory system** including five memory banks, semantic search, and emotional interaction features.

### 🧠 Five Memory Banks System
| Memory Bank | Function | Problem Solved |
|-------------|----------|----------------|
| **Goals Memory** | Tracks user goals (P0/P1/P2 priorities) | Goals easily forgotten, lack of tracking |
| **Experience Memory** | Records technical problems and solutions | Repeated mistakes, experience cannot accumulate |
| **Emotion Memory** | Analyzes user emotions and habit preferences | AI doesn't understand your emotions and habits |
| **Session Memory** | Daily conversation summaries (10:1 compression) | Conversation history too long, hard to search |
| **Version Memory** | System change history records | Configuration changes lack records |

### 🔍 Intelligent Retrieval Capabilities
- **Semantic Search**: Based on ChromaDB vector database, natural language query of memories
- **Keyword Search**: Fast lookup from Markdown files
- **Hybrid Search**: Vector + keyword combination, improves search accuracy
- **RAG Enhancement**: Retrieval Augmented Generation, improves answer quality and relevance

### ❤️ Heartbeat Recall Emotional Interaction (Core Innovation)
**Imitates human conversation, builds long-term emotional connections**—solves AI's lengthy, emotionless responses:

#### 🎭 Highly Realistic Human Interaction
- **Smart Triggering**: AI actively recalls like a friend: "By the way, remember last week's 'seaside café' 'sunset' 'photos', did you end up going?"
- **Natural Conversation Flow**: Randomly inserts memories during daily chats (30% probability), avoiding mechanical feel
- **Emotional Intelligence**: Analyzes your emotional state (happy/calm/confused/achievement), adjusts interaction style

#### ⚙️ Flexible Configurable System
- **Configurable Probabilities**: Each trigger scene has adjustable probability (30%/50%/100%)
- **Frequency Control**: Daily limits, minimum intervals, special holiday rules
- **Scene Customization**: Supports daily conversation, task completion, forgotten goals, holiday care, etc.
- **Sensitive Day Avoidance**: Automatically avoids sensitive holidays like Qingming Festival

#### 🌱 Long-term Cultivation & Exclusivity
- **Habit Learning**: Records your work patterns, preferred topics, common keywords
- **Exclusive Memories**: Builds personalized memory bank based on your historical conversations
- **Progressive Optimization**: Continuously optimizes trigger timing and wording through silent review
- **Emotional Evolution**: AI understands you better over time, building real "long-term relationships"

#### 🔧 Fully Controllable User Experience
- **Switch Controls**: All features default ON but can be turned OFF anytime
- **Real-time Adjustment**: Can modify configuration parameters immediately based on feedback
- **Transparent Rules**: All trigger logic and frequency limits completely公开
- **Zero Interference Promise**: Auto-pauses during emergencies, late-night hours, busy states

### 🚀 Technical Advantages
- **Fully Local**: Zero API Keys, zero token consumption, completely offline operation
- **Cross-platform**: Windows (WSL/Git Bash), Linux, macOS
- **Easy Integration**: Standard OpenClaw Skill format, one-click installation
- **Highly Configurable**: All features have switch controls, enable as needed

## 📦 Installation Guide

### ⚠️ Prerequisites
1. **OpenClaw v1.0+** installed and running
2. **Python 3.8+** environment
3. **About 100MB** disk space (including vector model)

### 🚀 One-Click Installation

#### Option A: Install via Git
```bash
# Clone the repository
git clone https://github.com/JamieYang9996/Heartbeat-Memories.git

# Copy to OpenClaw skills directory
cp -r Heartbeat-Memories ~/.openclaw/skills/heartbeat-memories

# Initialize the memory system
cd ~/.openclaw/skills/heartbeat-memories && python3 scripts/hbm_init.py
```

#### Option B: Manual Installation
1. Download this skill folder
2. Place it in your OpenClaw skills directory: `~/.openclaw/skills/`
3. Run initialization: `python3 scripts/hbm_init.py`

## 🔧 Usage

### Basic Usage (Out-of-the-box)
After installation, Heartbeat-Memories automatically:
1. Records important conversations to memory banks
2. Responds to trigger words for retrieval
3. Maintains memory bank integrity

### Common Trigger Words
```
# English trigger words
"memory system", "long-term memory", "help me recall"
"save this", "check goals", "how did we solve this"

# Chinese trigger words
"记忆系统", "长期记忆", "帮我回忆"
"记下来", "查看目标", "上次怎么解决的"
```

### Usage Examples
```markdown
User: "Save this, I want to learn React framework"
AI: ✅ Recorded to Goals Memory

User: "How did we solve that server 502 error last time?"
AI: 🔍 Retrieved solution from Experience Memory...

User: "Help me recall projects we discussed last week"
AI: ❤️ Remember last week's "user dashboard design"...
```

### Heartbeat Recall Example
```
AI: ❤️ By the way, remember last Friday's "seaside café" "sunset" "photos", did you end up going?

User: "Went! So beautiful!" 
→ AI records successful recall, enhances emotional connection

User: "Seems I forgot about this..." 
→ AI补充完整细节, recovers lost memory
```

## 🏗️ System Architecture

```
heartbeat-memories/
├── SKILL.md                    # OpenClaw Skill description file
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── memory/                     # Five memory bank templates
│   ├── _templates/
│   │   ├── GOALS_template.md
│   │   ├── TIPS_template.md
│   │   └── [other templates]
│   ├── 目标记忆库/
│   ├── 经验记忆库/
│   ├── 情感记忆库/
│   ├── 会话记忆库/
│   ├── 版本记忆库/
│   └── 心跳回忆/
├── scripts/                    # Core scripts
│   ├── hbm_init.py            # Initialization script
│   └── [other scripts]
├── config/                     # Configuration files
│   └── hbm_config_template.json
└── docs/                       # Documentation
    └── [documentation files]
```

## 🛡️ Security & Privacy Statement

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

## 🤝 Contribution & Support

### GitHub Repository
- Project URL: https://github.com/JamieYang9996/Heartbeat-Memories
- Issues: Report problems or suggest features
- Pull Requests: Code contributions welcome

## 📄 License

MIT License - See LICENSE file

---

<div align="center">

**Heartbeat-Memories gives your OpenClaw true long-term memory, making it a smarter assistant that truly understands you!**

⭐ If this project helps you, please give it a Star!

</div>