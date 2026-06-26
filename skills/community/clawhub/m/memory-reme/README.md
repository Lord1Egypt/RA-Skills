# Memory-reme - ReMe Memory Management System

[![ClawdHub](https://clawdhub.com/badges/clawdhub.svg)](https://clawdhub.com)

A memory management system powered by ReMe that provides persistent cross-session memory, automatic user preference application, and intelligent context compression for OpenClaw.

---

## Features

- **Cross-Session Memory**: Persistent memory across all OpenClaw sessions
- **Automatic Preference Application**: Apply user preferences automatically
- **Intelligent Context Compression**: Compress conversation history when approaching limits
- **User Feedback Learning**: Learn from corrections and improve over time

## Installation

### Prerequisites

- Python 3.8+
- OpenClaw Gateway running
- ReMe API access (requires `reme-ai` package)

### Setup

```bash
# Clone or download this skill
cd ~/.clawdbot/skills/memory-reme

# Install dependencies
pip install reme-ai

# Initialize memory system
python3 scripts/init_reme.py
```

## Usage

### Starting a Session with Memory

```python
from reme.reme_light import ReMeLight

# Initialize ReMe
reme = ReMeLight(working_dir=".reme", language="zh")
await reme.start()

# Retrieve user preferences
prefs = await reme.memory_search(
    query="用户偏好",
    max_results=5
)

# Apply preferences
if prefs:
    auto_send_files = prefs[0].get("auto_send_files", False)
```

### Adding Memories

```python
# Add a new memory
await reme.add_memory(
    memory_content="User prefers concise code with comments",
    user_name="阿伟",
    memory_type="personal"
)
```

### Searching Memories

```python
# Search for memories
results = await reme.memory_search(
    query="代码风格",
    max_results=10,
    min_score=0.5
)

for i, result in enumerate(results, 1):
    print(f"{i}. {result['content']}")
```

## Memory Types

| Type | Description | Example |
|-------|-------------|----------|
| **Personal** | User preferences, habits | "Prefer concise code" |
| **Task** | Execution experience, patterns | "Python scripts should include error handling" |
| **Tool** | Tool usage experience | "web_fetch needs timeout 30s for this site" |

## Best Practices

1. **Always initialize ReMe at session start**
2. **Search before making assumptions**
3. **Apply preferences consistently**
4. **Learn from every correction**
5. **Update MEMORY.md regularly**

## Configuration

Memory files are stored in:
- `.reme/` - Working directory
- `memory/YYYY-MM-DD.md` - Daily session summaries
- `MEMORY.md` - Long-term memory

## Documentation

- [SKILL.md](SKILL.md) - Full skill documentation
- [memory-structure.md](references/memory-structure.md) - Memory architecture
- [best-practices.md](references/best-practices.md) - Usage guidelines

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Author**: OpenClaw Community  
**Version**: 1.0.0  
**Last Updated**: 2026-03-07
