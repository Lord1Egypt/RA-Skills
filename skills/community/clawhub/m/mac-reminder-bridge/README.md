# Mac Reminder Bridge 🔔

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

> [!IMPORTANT]
> **This entire repository, including all code and documentation, was generated 100% by Claude 4.6 Sonnet.**

[**📖 中文说明文档 (Chinese README)**](./README_CN.md)

A lightweight HTTP bridge that allows Docker containers (especially AI agents like OpenClaw) to manage your native **macOS Reminders.app** using simple REST API calls.

## 🌟 Why run OpenClaw in Docker? (And why you need this bridge)

Running OpenClaw (or any AI agent) inside Docker on macOS offers significant advantages over a native installation:

1. **Security & Isolation**: AI agents frequently execute shell commands. Docker ensures that even a rogue script is trapped in a sandbox, unable to delete your personal `Documents` or access sensitive SSH keys directly.
2. **Environment Consistency**: Avoid the "it works on my machine" headache. Docker provides a clean, predictable environment with all dependencies pre-installed, regardless of your macOS Python/Node.js version drift.
3. **Dependency Management**: Native macOS environments can get "poluted" by conflicting libraries. Docker keeps your system clean.
4. **The "Air Gap" Problem**: However, Docker's isolation prevents agents from talking to native macOS features like **Apple Reminders**, **Mail**, or **iMessage**. 

**Mac Reminder Bridge** solved this final hurdle—keeping your agent safe in its sandbox while granting it a "controlled key" to your productivity ecosystem.

## 🌟 Why this exists?
AI agents running inside Docker are isolated from your host's system APIs. This bridge creates a secure "wormhole," permitting your local AI assistant to set reminders, list tasks, and mark them as complete directly in your Apple ecosystem.

## 🚀 Features
- **Full CRUD Support**: Create, Read, Update, and Delete reminders.
- **Natural Language Ready**: Designed to work seamlessly with AI agent tool-calling.
- **Smart Formatting**: Supports due dates, priorities, notes, and specific lists.
- **Security First**: 
  - IP Address allowlisting.
  - Optional Shared Secret authentication (`X-Bridge-Secret`).
  - Protection against AppleScript injection.
- **Reliable**: Uses robust AppleScript automation with locale-safe date parsing.

## 📦 Installation & Setup

### 1. Host Side (Your Mac)
Clone the repo and install dependencies:
```bash
git clone https://github.com/your-username/mac-reminder-bridge.git
cd mac-reminder-bridge
pip install -r requirements.txt
```

Run the listener:
```bash
python3 listener.py
```
*Note: On first run, macOS will prompt you to grant terminal/IDE permission to access Reminders. Please allow this.*

### 2. Client Side (Inside Docker/OpenClaw)
If you are using OpenClaw, simply install the skill:
```bash
clawhub install mac-reminder-bridge
```

## 🛠 API Usage

### Health Check
```bash
curl http://host.docker.internal:5000/health
```

### Create a Reminder
```bash
curl -X POST http://host.docker.internal:5000/add_reminder \
     -H "Content-Type: application/json" \
     -d '{
       "task": "Pick up express package",
       "due": "2026-03-14 18:00",
       "priority": "high",
       "notes": "Must arrive before 6 PM!"
     }'
```

## ⚙️ Configuration (Environment Variables)
| Variable | Description | Default |
|----------|-------------|---------|
| `BRIDGE_SECRET` | Shared secret for authentication | (None) |
| `BRIDGE_PORT` | Port to listen on | `5000` |
| `BRIDGE_ALLOWED_IPS` | Comma-separated allowlist (Cloud users see below) | `172.0.0.0/8,127.0.0.1` |

### ☁️ Note for Cloud/Tencent Cloud users
If you are running OpenClaw on a remote server (e.g., Tencent Cloud, AWS), your Docker instance will have a public IP. You **MUST** add your server's public IP to `BRIDGE_ALLOWED_IPS` or set a `BRIDGE_SECRET`:
```bash
# Example: Allow a specific Cloud Server IP
export BRIDGE_ALLOWED_IPS="1.2.3.4,127.0.0.1"
python3 listener.py
```

## 📜 License
MIT License. Feel free to use, modify, and distribute!
