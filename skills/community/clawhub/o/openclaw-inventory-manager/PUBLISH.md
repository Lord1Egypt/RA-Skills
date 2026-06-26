# Where are you from (OpenClaw Skill Inventory Manager) 📦🦀

Do you know exactly where all your AI agent skills came from? 
As we download skills from **ClawHub**, **GitHub**, **NPM**, and manual sources, managing their paths and origins becomes a chaotic task. **Where are you from** is an enterprise-grade utility that solves this by providing a unified audit trail for your OpenClaw environment.

## 🚀 Why "Where are you from"? (Motivation)

In the rapidly evolving AI ecosystem, developers frequently install third-party capabilities. However, this leads to several critical issues:
1.  **Path Confusion**: "I installed it, but I can't find it."
2.  **Ghost Skills**: "I deleted the folder, but the agent still thinks I have the skill."
3.  **Security Risks**: "Where did this code come from? Does it have my API keys?"
4.  **Origin Amnesia**: "I don't remember if I got this via NPM or a Git clone."

**Where are you from** was created to bring transparency and security to your AI workstation. By automatically identifying origins and masking secrets, it ensures you stay in control of your agent's modular capabilities.

## 🌟 Key Features

- **Source Detection**: Identify GitHub, NPM, ClawHub, or Manual origins automatically.
- **Security Scrubbing**: Detects and masks 10+ common API key patterns (OpenAI, HF, GHP, etc.).
- **Privacy Protection**: Support for `SKILL.private.md` to classify and hide sensitive instructions.
- **Git Syncing**: One-command synchronization (`sync --push`) to keep your inventory safe on GitHub.

## 🛠️ Prerequisites

This skill uses JavaScript for file scanning and Git integration.
- **Node.js (v14+) is required.**

## ⚡ Quick Start

### 1. Bootstrap (Recommended)
Set up everything (Config + Git + Initial Scan) in one go.
```bash
node .agents/skills/openclaw-inventory-manager/inventory.js bootstrap
```

### 2. Initialize
Link your local inventory directly to a remote GitHub repository.
```bash
node .agents/skills/openclaw-inventory-manager/inventory.js init https://github.com/username/my-skills.git
```

### 3. Sync & Push
Generate your `SKILLS_MANIFEST.md` report and securely sync to the cloud.
```bash
node .agents/skills/openclaw-inventory-manager/inventory.js sync --push
```

Know your AI's origins. Manage your assets. Stay secure with **Where are you from**.
