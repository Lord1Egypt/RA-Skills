# NWO Robotics Skill for OpenClaw

[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT--0-blue.svg)](LICENSE)

Control robots and IoT devices through natural language using the NWO Robotics API.

## 🚀 Quick Start

### 1. Get API Credentials

1. Visit https://nwo.capital/webapp/api-key.php
2. Create an account or log in
3. Generate your API key
4. Note your User ID

### 2. Install the Skill

```bash
# Via ClawHub
openclaw skill install nwo-robotics

# Or manually
git clone https://github.com/yourorg/nwo-robotics-openclaw.git
```

### 3. Configure Environment

```bash
export NWO_API_KEY="your_api_key_here"
export NWO_USER_ID="your_user_id_here"
```

### 4. Start Using

```
User: Check robot status
→ Robot Status:
  • robot_001: online, idle
  • robot_002: online, executing task

User: What's the temperature in the lab?
→ Sensor Readings:
  • Lab 3: 23.5°C
  • Lab 4: 24.1°C

User: Move robot_001 to position x:10, y:20
→ Command sent to robot_001. Status: pending
```

## 📋 Supported Commands

### Robot Control
- `Check robot status` - List all connected robots
- `Stop all robots` - Emergency stop
- `Move robot_X to position x:10 y:20` - Navigate to coordinates
- `Patrol mode on/off` - Enable/disable patrol behavior

### Vision Tasks
- `Scan for objects` - Object detection
- `Find the red box` - Targeted object search
- `Detect people` - People detection

### IoT Sensors
- `Temperature check` - Query temperature sensors
- `What's the humidity?` - Query humidity sensors
- `Sensor status in warehouse` - Location-based queries

### General Tasks
- `Pick up the box` - VLA task execution
- `Follow the path` - Path following
- Any natural language instruction

## 🔒 Security

- **No embedded credentials** - Users provide their own API keys
- **Input sanitization** - All user input is validated and cleaned
- **Command allowlist** - Only approved commands are processed
- **Rate limiting** - Respects API tier limits (enforced server-side)

## 📊 API Tiers

| Tier | Monthly Calls | Price |
|------|---------------|-------|
| Free | 100,000 | $0 |
| Prototype | 500,000 | $49/mo |
| Production | Unlimited | $199/mo |

Upgrade at: https://nwo.capital/webapp/api-key.php

## 🛠️ Development

### File Structure
```
nwo-robotics-openclaw/
├── SKILL.md          # Skill documentation (required)
├── skill.yaml        # Skill configuration
├── index.js          # Main implementation
├── README.md         # This file
├── examples/         # Example usage files
│   └── basic-commands.md
└── LICENSE           # MIT-0 License
```

### Testing

```bash
# Set test credentials
export NWO_API_KEY="test_key"
export NWO_USER_ID="test_user"

# Run skill locally
node -e "
  const skill = require('./index.js');
  skill.handle('Check robot status').then(console.log);
"
```

## 🐛 Troubleshooting

### "NWO_API_KEY environment variable is required"
Set your API key: `export NWO_API_KEY="your_key"`

### "API rate limit exceeded"
You've hit your monthly quota. Upgrade your plan at nwo.capital.

### "No robots currently connected"
Check that your robots are powered on and connected to the NWO Robotics platform.

## 📚 Documentation

- [NWO Robotics API Docs](https://nwo.capital/webapp/api-key.php)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/skills)
- [ClawHub](https://clawhub.ai)

## 🤝 Contributing

Contributions welcome! Please submit PRs or issues on GitHub.

## 📄 License

MIT-0 - Free to use, modify, and redistribute. No attribution required.

---

Built with 💚 by NWO Capital for the OpenClaw community.
