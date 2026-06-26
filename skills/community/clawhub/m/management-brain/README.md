---
name: boss-ai-agent
version: "1.3.0"
description: "Boss AI Agent — your AI management middleware. Connects boss to all systems (Telegram/Slack/GitHub/Notion/Email), 16 mentor philosophies, 6 AI C-Suite seats, 9 culture packs, 7 automated scenarios. Works with Claude Code, ChatGPT, and Gemini via MCP."
user-invocable: true
emoji: "🤖"
homepage: "https://manageaibrain.com"
metadata:
  openclaw:
    primaryEnv: "BOSS_AI_AGENT_API_KEY"
    optional:
      env:
        - name: "BOSS_AI_AGENT_API_KEY"
          description: "Optional. Connects to manageaibrain.com cloud for full mentor configs, C-Suite board, web dashboard, and cross-team analytics. Without it, all 7 scenarios work locally with no degradation."
        - name: "MANAGEMENT_BRAIN_API_KEY"
          description: "Legacy fallback for BOSS_AI_AGENT_API_KEY. Accepted for backward compatibility with management-brain skill."
    requires:
      config:
        - "~/.openclaw/skills/boss-ai-agent/config.json"
---

# Boss AI Agent

Your AI management middleware — connects you to all systems through mentor wisdom.

## Features

- **7 automated scenarios**: daily check-in cycle, project health patrol, smart briefing, 1:1 meeting prep, signal scanning, knowledge base, emergency response
- **16 mentor philosophies**: Musk, Inamori, Jack Ma, Dalio, Grove, Ren Zhengfei, Son, Jobs, Bezos, Buffett, Zhang Yiming, Lei Jun, Cao Dewang, Chu Shijian, Erin Meyer, Jack Trout
- **6 AI C-Suite seats**: CEO, CFO, CMO, CTO, CHRO, COO — virtual board discussions for strategic decisions
- **9 culture packs**: default, Philippines, Singapore, Indonesia, Sri Lanka, Malaysia, China, USA, India
- **Multi-client MCP**: works with Claude Code (stdio), ChatGPT (HTTP), and Gemini (HTTP)
- **23+ messaging platforms**: works with any channel connected to OpenClaw
- **Zero external dependency**: fully functional without any cloud account

## Install

```
clawhub install boss-ai-agent
```

## Quick Start

```
/boss-ai-agent
> How many people do you manage? 5
> What communication tools does your team use? Telegram and GitHub
> Done! Musk mode activated. First check-in at 9 AM tomorrow.
```

## Mentors

| ID | Name | Style |
|----|------|-------|
| musk | Elon Musk | First principles, urgency, 10x thinking |
| inamori | Kazuo Inamori (稻盛和夫) | Altruism, respect, team harmony |
| ma | Jack Ma (马云) | Embrace change, teamwork, customer-first |
| dalio | Ray Dalio | Radical transparency, principles-driven |
| grove | Andy Grove | OKR-driven, data-focused, high output |
| ren | Ren Zhengfei (任正非) | Wolf culture, self-criticism, striver-oriented |
| son | Masayoshi Son (孙正义) | 300-year vision, bold bets |
| jobs | Steve Jobs | Simplicity, excellence pursuit |
| bezos | Jeff Bezos | Day 1 mentality, customer obsession |
| buffett | Warren Buffett | Long-term value, patience |
| zhangyiming | Zhang Yiming (张一鸣) | Delayed gratification, data-driven |
| leijun | Lei Jun (雷军) | Extreme value, user participation |
| caodewang | Cao Dewang (曹德旺) | Industrial spirit, craftsmanship |
| chushijian | Chu Shijian (褚时健) | Ultimate focus, resilience |
| meyer | Erin Meyer (艾琳·梅耶尔) | Cross-cultural communication, culture map |
| trout | Jack Trout (杰克·特劳特) | Positioning theory, brand strategy |

## AI C-Suite Board

Convene 6 AI executives for cross-functional strategic analysis:

| Seat | Domain |
|------|--------|
| CEO | Strategy, vision, competitive positioning |
| CFO | Finance, budgets, ROI analysis |
| CMO | Marketing, growth, brand strategy |
| CTO | Technology, architecture, engineering |
| CHRO | People, culture, talent management |
| COO | Operations, process, efficiency |

Ask: *"Should we expand to Japan?"* → All 6 seats analyze from their perspective, followed by a unified synthesis.

## MCP Server

9 tools accessible via MCP for Claude Code, ChatGPT, and Gemini:

| Tool | Description |
|------|-------------|
| `get_team_status` | Today's check-in progress |
| `get_report` | Weekly/monthly performance with rankings |
| `get_alerts` | Alerts for consecutive missed check-ins |
| `switch_mentor` | Change management philosophy |
| `list_mentors` | All 16 mentors with expertise |
| `board_discuss` | AI C-Suite board meeting |
| `chat_with_seat` | Direct chat with one C-Suite exec |
| `list_employees` | All active employees |
| `get_employee_profile` | Employee sentiment and history |

**ChatGPT/Gemini**: connect via `https://manageaibrain.com/mcp` (MCP HTTP)

## Scenarios

1. **Daily Management Cycle** — AI sends check-ins, chases non-responders, generates end-of-day summary
2. **Project Health Patrol** — scans GitHub/Linear/Jira for stale PRs, failed CI, overdue tasks
3. **Smart Daily Briefing** — cross-channel morning briefing sorted by mentor priority
4. **1:1 Meeting Assistant** — auto-generates prep document with employee data and suggested topics
5. **Periodic Signal Scanning** — monitors team channels every 30 min for urgent/warning signals
6. **Knowledge Base Management** — records decisions and notes to Notion, Google Sheets, or local files
7. **Emergency Response** — detects critical signals, alerts boss immediately, gathers rapid intel

## Cloud Platform (Optional)

Connect to manageaibrain.com for additional features:

- Web dashboard and analytics
- Full mentor configs for all 16 mentors
- AI C-Suite virtual board discussions
- Cross-team benchmarking

Set `BOSS_AI_AGENT_API_KEY` to enable. All 7 scenarios work without it.

## Migrating from management-brain?

Boss AI Agent is a new skill, not an upgrade. Your existing management-brain data is untouched.

To switch:
1. Install boss-ai-agent
2. Run onboarding (`/boss-ai-agent`)
3. Add your team members

Legacy env var `MANAGEMENT_BRAIN_API_KEY` is accepted as fallback.

## 中文说明

Boss AI Agent 是老板的 AI 管理中间件。通过已有的 OpenClaw 频道（Telegram/Slack/飞书）管理团队，零外部依赖。

**核心功能：**
- 7 大自动化场景（签到、巡检、早报、1:1、信号扫描、知识库、紧急响应）
- 16 位导师哲学（马斯克、稻盛和夫、马云、梅耶尔、特劳特等）
- 6 位 AI C-Suite 高管（虚拟董事会）
- 9 套文化包（适配菲律宾、新加坡、中国、美国、印度等文化差异）
- 多客户端支持：Claude Code + ChatGPT + Gemini

安装：`clawhub install boss-ai-agent`

## Links

- Website: https://manageaibrain.com
- GitHub: https://github.com/tonypk/ai-management-brain
- ClawHub: https://clawhub.ai/tonypk/boss-ai-agent
