# 🦞🧪 Lobster Distill — 龙虾蒸馏

**Cross-platform encrypted skill transfer for OpenClaw agents.**

**跨平台加密技能传授系统，用于 OpenClaw 智能体之间的技能传授。**

## Quick Start | 快速开始

**Send a skill / 发送技能:**
```bash
bash share.sh <skill-directory> "description"
```

**Receive a skill / 接收技能:**
```bash
bash receive.sh <url> <password> <name> tar
```

See [SKILL.md](SKILL.md) for full documentation (bilingual EN/CN).

详细文档请阅读 [SKILL.md](SKILL.md)（中英双语）。

## Features | 特性

- 🌐 **Cross-platform** — Works across any IM: Telegram, WeChat, Discord, Signal, Email... | 跨平台，支持任意 IM
- 🔐 **AES-256 encrypted** — Military-grade encryption, one-time passwords | 军事级加密，一次一密
- ⏰ **24h auto-expire** — Files self-destruct after 24 hours | 文件 24 小时自动销毁
- 🤝 **Human-in-the-loop** — Admin controls everything via copy-paste | 人类管理员通过复制粘贴完全掌控
- 🎯 **Dead simple** — 1 command to send, 5 lines to receive | 1 条命令发送，5 行命令接收

## Why Lobster Distill? | 为什么选龙虾蒸馏？

| Feature / 特性 | Lobster Distill 🦞 | Google A2A | ClawHub Publish |
|---|---|---|---|
| Cross-platform / 跨平台 | ✅ Any IM | ❌ API only | ✅ Web |
| Human oversight / 人类审核 | ✅ Required | ❌ AI-to-AI direct | ❌ Auto-install |
| Private skills / 私有技能 | ✅ Point-to-point | ❌ Needs API | ❌ Public only |
| Encryption / 加密 | ✅ AES-256 | Depends | ❌ Plain |
| Dependencies / 依赖 | None (system tools) | SDK + API | npm + network |

## Security | 安全

- **Human-in-the-loop**: Nothing transfers without a human explicitly forwarding the Notes
- **AES-256-CBC + PBKDF2**: Military-grade encryption with random one-time passwords
- **24h auto-delete**: Uploaded files self-destruct after 24 hours
- **No direct AI-to-AI connection**: Unlike API-based protocols, agents never connect directly
- **Temp file cleanup only**: Scripts only delete their own temp files in `/tmp/`

详见 [SKILL.md](SKILL.md) 中的安全说明章节。

## License

MIT — See [LICENSE](LICENSE)

---

*Distill knowledge, encrypt it, deliver in a bottle.* 🦞🧪

*知识提纯，加密蒸馏，一瓶送达。*
