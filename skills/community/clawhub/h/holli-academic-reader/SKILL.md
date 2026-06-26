---
version: 1.0.0
name: academic-reader
description: An AI-powered academic reading assistant that helps you read, summarize, and reflect on technical books using the methodology from Qian Xuesen's "Engineering Cybernetics". Includes chapter-by-chapter analysis, critical thinking prompts, and personal integration guidance.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "install": [],
      },
    "tags": ["reading", "education", "academic", "book-notes", "learning"],
    "author": "holli",
    "version": "1.0.0",
    "homepage": "https://github.com/holli/skills",
  }
---

# Academic Reader - 学术阅读助手

An AI-powered academic reading assistant that transforms technical books into actionable knowledge.

## Features

- **Chapter-by-Chapter Analysis**: Automatically extracts core concepts from each chapter
- **Critical Thinking Prompts**: Goes beyond summaries to encourage deep reflection
- **Personal Integration**: Helps connect book's ideas to your own work and growth
- **Engineering Cybernetics Method**: Uses control theory frameworks for systematic learning

## Use Cases

1. **Reading Technical Books**: Get structured summaries and analysis of academic/technical content
2. **Self-Reflection**: Use the book's ideas to反思 your own thinking and work
3. **Knowledge Extraction**: Convert dense technical content into actionable insights
4. **Learning Acceleration**: Quickly grasp complex concepts with guided analysis

## How It Works

This skill uses a structured reading methodology inspired by Qian Xuesen's "Engineering Cybernetics":

1. **Core Concepts Extraction**: Identify the key ideas in each chapter
2. **Theoretical Framework**: Understand the theory's structure and logic
3. **Critical Analysis**: Evaluate the theory's strengths, limitations, and assumptions
4. **Personal Integration**: Connect ideas to your own context and goals

## Requirements

- OpenClaw installed and configured
- Access to Claude API (Sonnet recommended for analysis tasks)
- A technical/academic book you want to read

## Installation

```bash
clawhub install academic-reader
```

## Usage

After installation, ask the AI to help you read a book using this methodology:

```
帮我分析[书名]，用工程控制论的方法论
```

Or use the included prompts in the `prompts/` folder for specific reading tasks.

## Included Files

- `SKILL.md` - This file
- `prompts/` - Ready-made prompts for different reading tasks
- `config/` - Configuration templates
- `README.md` - Detailed usage guide

## Credits

Methodology inspired by Qian Xuesen's "Engineering Cybernetics" (1954)
Skill created by holli

## License

MIT