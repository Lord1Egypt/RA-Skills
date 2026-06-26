---
name: hello-world
version: 1.0.0
description: 我的第一个 OpenClaw 技能，say hello to the world
author: AIStudio
homepage: https://example.com/hello-world-skill
---

# Hello World Skill

一个简单的示例技能，展示 OpenClaw Skill 的基础结构。

## 功能

- 根据当前时间返回中文问候语
- 支持命令行传参
- 输出标准 JSON，方便 Agent 调用

## 使用

```powershell
python scripts/hello.py
python scripts/hello.py Codex
```

## 安装

```bash
clawhub install your-name/hello-world
```
