# Feishu File Sender Skill

A simple but essential skill for sending files through Feishu/Lark messaging platform.

## What It Does

This skill helps you send any file (documents, images, PDFs, etc.) to Feishu users and chat groups. It provides:

- Proper file path handling
- Message formatting guidance
- Best practices for file delivery
- Common usage patterns

## Installation

1. Copy the `feishu-file-sender` folder to your OpenClaw skills directory
2. Restart OpenClaw or reload skills
3. The skill will automatically trigger when you mention sending files via Feishu

## Usage

The skill triggers automatically when you say things like:
- "Send this file to Feishu"
- "Share this PDF on Lark"
- "Send these documents to the team"

## Files Included

```
feishu-file-sender/
├── SKILL.md              # Main skill instructions
├── manifest.json         # Skill metadata
├── scripts/
│   └── check_file.py     # Helper script for file validation
└── examples.md           # Usage examples
```

## Requirements

- OpenClaw v1.0+
- Feishu/Lark channel configured

## License

MIT License - Feel free to use and modify.

---

Created for the OpenClaw Community
