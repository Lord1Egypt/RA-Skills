# 🦞 OpenClaw Unity Skill

> **TL;DR:** Vibe-code your game development remotely from anywhere! 🌍
> 
> **한줄요약:** 이제 집밖에서도 원격으로 바이브코딩으로 게임 개발 가능합니다! 🎮

Companion skill for the [OpenClaw Unity Plugin](https://github.com/TomLeeLive/openclaw-unity-plugin). Provides AI workflow patterns and gateway extension for Unity Editor control.

## ⚠️ Disclaimer

This software is in **beta**. Use at your own risk.

- Always backup your project before using
- Test in a separate project first
- The authors are not responsible for any data loss or project corruption

See [LICENSE](LICENSE.md) for full terms.

## Installation

```bash
# Clone to OpenClaw workspace
git clone https://github.com/TomLeeLive/openclaw-unity-skill.git ~/.openclaw/workspace/skills/unity-plugin

# Install gateway extension
cd ~/.openclaw/workspace/skills/unity-plugin
./scripts/install-extension.sh

# Restart gateway
openclaw gateway restart
```

## What's Included

```
unity-plugin/
├── SKILL.md           # AI workflow guide (~82 tools)
├── extension/         # Gateway extension (for OpenClaw channels)
│   ├── index.ts
│   ├── openclaw.plugin.json
│   └── package.json
├── scripts/
│   └── install-extension.sh
└── references/
    └── tools.md       # Detailed tool documentation
```

## Connection Modes

| Mode | Use Case | Setup |
|------|----------|-------|
| **Gateway** | Telegram, Discord, OpenClaw channels | Extension install + Gateway restart |
| **MCP Bridge** | Claude Code, Cursor, local AI | Unity: Window → OpenClaw Plugin → MCP Bridge → Start |

### MCP Setup (for Claude Code)

```bash
# Add to Claude Code
claude mcp add unity -- node /path/to/unity-plugin/MCP~/index.js

# Verify connection
curl http://127.0.0.1:27182/status
```

## Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Gateway Extension** | Enables `unity_execute` tool | `~/.openclaw/extensions/unity/` |
| **Skill** | AI workflow patterns | `~/.openclaw/workspace/skills/unity-plugin/` |
| **Unity Package** | Unity Editor plugin + MCP Bridge | [openclaw-unity-plugin](https://github.com/TomLeeLive/openclaw-unity-plugin) |
| **MCP Server** | Local stdio server for Claude Code | Plugin's `MCP~/index.js` |

## Quick Verify

```bash
# Check extension loaded
openclaw unity status

# Check skill available
ls ~/.openclaw/workspace/skills/unity-plugin/SKILL.md
```

## 🔐 Security: disableModelInvocation Setting

이 스킬은 기본적으로 `disableModelInvocation: true`로 설정되어 있습니다.

| Setting | AI Auto-Invoke | User Explicit Request |
|---------|---------------|----------------------|
| `false` | ✅ Allowed | ✅ Allowed |
| `true` (기본값) | ❌ Blocked | ✅ Allowed |

### `disableModelInvocation: true` (기본값)

**장점:**
- 사용자가 명시적으로 요청한 작업만 실행
- 예측 가능한 동작 - AI가 임의로 도구 호출 안함
- 민감한 환경에서 안전
- 토큰 사용량 절약

**단점:**
- 매번 도구 사용을 명시적으로 요청해야 함
- 워크플로우가 덜 자연스러움
- AI의 자율적 보조 기능 제한

**적합한 경우:** 프로덕션 환경, 민감한 데이터, 엄격한 제어 필요시

---

### `disableModelInvocation: false`

**장점:**
- AI가 자율적으로 보조 작업 수행 (hierarchy 검사, 스크린샷, 컴포넌트 확인)
- 대화 중 맥락에 맞게 자동으로 필요한 도구 호출
- 개발 워크플로우가 더 자연스럽고 빠름
- "씬 구조 보여줘" → AI가 바로 `debug.hierarchy` 실행

**단점:**
- AI가 의도치 않은 작업을 수행할 가능성
- 토큰 사용량 증가 (자동 도구 호출)
- 민감한 작업에는 부적합

**적합한 경우:** 개발/디버깅, 프로토타이핑, 학습 목적

---

### 설정 변경 방법

SKILL.md의 frontmatter에서 변경:

```yaml
---
name: unity-plugin
disableModelInvocation: false  # AI 자동 호출 허용
---
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) 2026.2.3+
- [OpenClaw Unity Plugin](https://github.com/TomLeeLive/openclaw-unity-plugin) in Unity

## License

MIT License - See [LICENSE](LICENSE.md)
