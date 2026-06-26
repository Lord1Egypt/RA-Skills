# Everything Openclaw (EO) Plugin for OpenClaw

> Multi-Expert Collaboration Plugin - Transform OpenClaw from single Agent to expert team

## Overview

This plugin extends OpenClaw with multi-expert collaboration capabilities, inspired by Claude Code's multi-agent architecture.

## Features

### 🤖 141 Expert Library
Access to 141 pre-configured experts across 8 major roles:
- **Architect** - System architecture & tech stack
- **Planner** - Project planning & task breakdown
- **Frontend** - UI/UX & frontend development
- **Backend** - API & backend development
- **QA** - Testing & quality assurance
- **Security** - Security review & vulnerability scanning
- **DevOps** - CI/CD & deployment
- **CodeReviewer** - Code quality & review

### 📋 6 Collaboration Tools

| Tool | Description |
|------|-------------|
| `eo_collab` | Main collaboration hub |
| `eo_list_experts` | List available experts |
| `eo_plan` | Create project plan with Planner |
| `eo_architect` | Design architecture with Architect |
| `eo_verify` | Verify checkpoint with QA |
| `eo_code_review` | Code review with CodeReviewer |

### 🔗 Skill Compatibility Layer

- Import Claude Code Skills
- Import ECC (everything-claude-code) Skills
- Automatic format conversion

### ✅ Checkpoint Verification

Multi-stage validation of project milestones.

## Installation

### Option 1: From GitHub (via main repo)
```bash
openclaw plugins install https://github.com/467718584/everything-openclaw
```

### Option 2: From Local Clone
```bash
# Clone the repository
git clone https://github.com/467718584/everything-openclaw.git
cd everything-openclaw

# Install the plugin
openclaw plugins install ./openclaw-eo-plugin
```

### Option 3: Build from Source
```bash
cd openclaw-eo-plugin
npm install
npm run build
openclaw plugins install .
```

## Usage

### Basic Commands

```
/eo-collab "帮我做一个博客系统"
/eo-plan "开发博客系统"
/eo-architect "设计博客系统架构"
/eo-verify "验证架构设计"
/eo-code-review "./src"
```

### Tool Examples

```javascript
// List all experts
await tool('eo_list_experts', { filter: 'architect' })

// Create project plan
await tool('eo_plan', { task: '开发博客系统' })

// Design architecture
await tool('eo_architect', { project: '博客系统' })

// Verify checkpoint
await tool('eo_verify', { checkpoint: 'milestone1' })

// Code review
await tool('eo_code_review', { path: './src' })
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              OpenClaw Agent                      │
│                                                 │
│   ┌─────────────────────────────────────────┐  │
│   │         EO Plugin                        │  │
│   │                                          │  │
│   │  Tools: eo_collab, eo_plan, eo_architect │  │
│   │  Hooks: before_tool_call                 │  │
│   │                                          │  │
│   │  ┌──────────────────────────────────┐   │  │
│   │  │  Expert Library (141 experts)     │   │  │
│   │  │  8 Roles × 细分领域               │   │  │
│   │  └──────────────────────────────────┘   │  │
│   └─────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Requirements

- OpenClaw >= 2026.3.0
- Node.js >= 18.0.0

## Comparison

| Feature | Without EO | With EO |
|---------|-----------|---------|
| Agent count | 1 | N (team) |
| Expert count | 0 | 141 |
| Task decomposition | Manual | Automatic |
| Code review | Basic | Security + Performance + Style |
| Planning | Manual | Planner expert |

## License

MIT

## Links

- [Everything Openclaw](https://github.com/467718584/everything-openclaw)
- [Plugin Source](https://github.com/467718584/everything-openclaw/tree/main/openclaw-eo-plugin)
