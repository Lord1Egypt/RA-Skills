# Keep Learning

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)
[![License](https://img.shields.io/badge/License-MIT--0-green.svg)](LICENSE)
[![ClawdHub](https://img.shields.io/badge/ClawdHub-available-orange)](https://clawhub.ai/)
[![Version](https://img.shields.io/badge/version-0.0.2-blue)](CHANGELOG.md)

Learn and memorize knowledge from local directories. Transform your knowledge base into agent memory.

## Features

- Multi-format Support: Markdown, Python, JavaScript, TypeScript, Java, Go, Rust, C/C++, Shell, YAML, JSON, and more
- Git Integration: Auto-pull latest changes before learning
- Incremental Learning: Only process changed files (Git-aware)
- Three-Layer Architecture: Core memory + Knowledge index + Source files
- Learning Reports: Track what was learned and updated

## Installation

### Via Skills CLI (Recommended)

    npx skills add nileader/keep-learning

Or with options:

    npx skills add nileader/keep-learning -g -y

- `-g` Install globally (available across all projects)
- `-y` Skip confirmation prompts

### Via ClawdHub

    clawdhub install keep-learning

### Manual

    git clone https://github.com/nileader/keep-learning.git ~/.openclaw/skills/keep-learning

## Usage

Simply tell your agent:

    持续学习知识

or

    keep learning

### First Time Setup

On first use, you will be asked to provide your knowledge base path:

    User: 持续学习知识
    Agent: Please provide the path to your knowledge base directory.
    User: ~/knowledge/work-assistant
    Agent: [Learning begins...]

### Subsequent Uses

The agent remembers your configuration and auto-pulls from git.

## Three-Layer Knowledge Architecture

| Layer | Storage | Content | Purpose |
|-------|---------|---------|---------|
| L1 | Agent Memory | Key insights, concepts | Auto-surfaces in conversations |
| L2 | Agent Memory | File index with summaries | Quick file lookup |
| L3 | Local Files | Full original content | Deep-dive access |

## Runtime Data

Runtime data is stored in ~/.keep-learning/:

| File | Purpose |
|------|---------|
| last-commit | Git commit hash of last learning |
| config.json | User configuration |

## Supported File Formats (v0.0.1)

| Category | Extensions |
|----------|------------|
| Documentation | .md, .markdown, .txt |
| Python | .py |
| JavaScript/TypeScript | .js, .ts, .jsx, .tsx |
| Java | .java |
| Go | .go |
| Rust | .rs |
| C/C++ | .c, .cpp, .h, .hpp |
| Shell | .sh, .bash, .zsh |
| Config | .yaml, .yml, .json, .toml |
| Data | .sql, .csv |

### Not Yet Supported

- PDF, Word, Excel, PowerPoint, Keynote
- Audio and video files

## Requirements

- Agent with filesystem access (read_file, run_in_terminal)
- Agent with memory system (update_memory, search_memory)
- Git (optional, for auto-pull and incremental learning)

## License

MIT-0 - MIT No Attribution

## Author

nileader - https://github.com/nileader
