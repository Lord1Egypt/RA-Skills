---
name: openclaw-macos-security
description: macOS security monitoring for OpenClaw
---

# 🛡️ MaclawPro Security

**Comprehensive macOS security monitoring for OpenClaw**

## What does this skill do?

This skill provides **52+ professional macOS security tasks** including:

- 📹 **Camera monitoring** - Check which apps use your camera right now
- 🎤 **Microphone monitoring** - See microphone access in real-time
- 🔥 **Firewall status** - Verify your Mac's firewall is enabled
- 🔐 **VPN checker** - Detect VPN connection status
- 📡 **WiFi scanner** - Analyze WiFi security (WPA2/WPA3)
- 🔌 **Port scanner** - List open network ports
- 🛑 **App blocker** - Block suspicious apps instantly (Pro feature)

## When to use this skill

Use this skill when you need to:
- Check if apps are secretly using your camera or microphone
- Verify your Mac's security settings (firewall, VPN)
- Scan for open ports or WiFi vulnerabilities
- Monitor system security in real-time

## Example commands

```
User: Check if anyone is using my camera
Skill: ✅ CAMERA INACTIVE - No apps currently using your camera

User: Is my firewall on?
Skill: ✅ FIREWALL ENABLED - Your Mac is protected!

User: Check VPN status
Skill: ⚠️ VPN INACTIVE - Your traffic is NOT protected
```

## Requirements

- **macOS only** (uses macOS-specific commands)
- **Permissions needed:** exec, fs.read, network
- **No API keys required** for basic features

## Installation

```bash
npm install openclaw-macos-security
```

Or via OpenClaw:
```bash
openclaw skills install openclaw-macos-security
```

## Available commands

- `camera-status` - Check camera usage
- `microphone-status` - Check microphone access
- `firewall-status` - Firewall configuration
- `vpn-checker` - VPN connection status
- `open-ports` - List listening ports
- `wifi-scanner` - WiFi security analysis
- `block-app <name>` - Block suspicious app

## Privacy & Security

✅ **All monitoring stays on your Mac** - No data sent to external servers
✅ **Open source** - Code available on GitHub
✅ **Created by certified security experts**

## Upgrade to MaclawPro Pro

This skill provides basic monitoring. For advanced features:
- Real-time alerts (Telegram, Email, Slack)
- Web dashboard with analytics
- Automated threat blocking
- 24/7 background monitoring

👉 [maclawpro.com/pricing](https://maclawpro.com/pricing)

## Support

- 📦 npm: [openclaw-macos-security](https://www.npmjs.com/package/openclaw-macos-security)
- 💻 GitHub: [drg3nz0/maclaw-openclaw-skill](https://github.com/drg3nz0/maclaw-openclaw-skill)
- 🌐 Website: [maclawpro.com](https://maclawpro.com)

---

**Professional macOS security monitoring**
