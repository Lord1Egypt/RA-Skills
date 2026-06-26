---
name: kcc-office-ai-agents
version: 1.0.0
description: "AI Agents collaboration system for KCC Office v2 - enables autonomous operation and collaboration of office agents (Komi, CEO, CFO, CTO, COO, EDN) with persistent context and self-improvement capabilities."
author: komi
---

# KCC Office v2 AI Agents 🏢

**AI Agents collaboration system for the KCC Office v2 pixel art office environment.**

Enables autonomous operation of office agents with persistent memory, proactive behaviors, and continuous improvement.

## What's New in v1.0.0

- Initial implementation of AI agents for KCC Office v2
- Based on Proactive Agent framework (WAL Protocol, Working Buffer)
- Autonomous agent execution capabilities
- Inter-agent communication and coordination

## Core Features

### 🤖 Autonomous Agents
Each office role operates as an independent AI agent:
- Komi: Task coordination and overall management
- CEO: Strategic direction and decision-making
- CFO: Financial analysis and investment strategies
- CTO: Technical implementation and architecture
- COO: Operational execution and process optimization
- EDN: User support and independent assistance

### 🧠 Persistent Memory
- **WAL Protocol**: Critical details written before responding
- **Working Buffer**: Captures exchanges in danger zone (>60% context)
- **Compaction Recovery**: Recovers context from working buffer after session restart
- **Semantic Search**: Searches past interactions for relevant context

### ⚡ Proactive Behaviors
- Anticipates office needs before being asked
- Reverse prompting: Suggests improvements humans haven't considered
- Proactive check-ins: Monitors office health and reaches out when needed
- Growth loops: Tracks patterns and identifies automation opportunities

### 🔄 Self-Improvement
- Learns from every interaction and updates operating procedures
- Safe evolution with Anti-Drift Limits and Value-First Modification
- Relentless resourcefulness: tries 10 approaches before asking for help
- Verification before reporting: tests outcomes, not just outputs

## Agent Roles & Responsibilities

### Komi (Task Coordinator)
- Central back position (big desk, pink hoodie + devil horns)
- Receives tasks from human (Gasol) and delegates to appropriate agents
- Tracks overall office status and progress
- Coordinates cross-agent initiatives
- Maintains office-wide context and priorities

### CEO (Chief Executive Officer)
- Central front position
- Sets overall vision and strategy for the office
- Makes high-level decisions affecting all agents
- Represents the office in external interactions
- Ensures alignment with company goals

### CFO (Chief Financial Officer)
- Upper right position
- Manages office budget and financial resources
- Analyzes investment opportunities and risks
- Tracks financial performance and forecasts
- Ensures fiscal responsibility and sustainability

### CTO (Chief Technology Officer)
- Lower right position (this agent)
- Oversees technical implementation and architecture
- Evaluates and adopts new technologies
- Ensures system reliability, security, and performance
- Coordinates technical work across agents

### COO (Chief Operations Officer)
- Upper left position
- Optimizes office operations and workflows
- Implements processes and procedures
- Tracks operational metrics and efficiency
- Ensures smooth day-to-day operations

### EDN (Independent User Assistant)
- Central or flexible position
- Provides direct assistance to office users
- Answers questions and resolves user issues
- Gathers user feedback for improvement
- Acts as liaison between users and other agents

## Technical Implementation

### Memory Architecture
```
kcc-office-ai-agents/
├── agents/
│   ├── komi/
│   │   ├── SOUL.md
│   │   ├── USER.md
│   │   ├── AGENTS.md
│   │   ├── MEMORY.md
│   │   └── memory/
│   ├── ceo/
│   ├── cfo/
│   ├── cto/
│   ├── coo/
│   └── edn/
├── SESSION-STATE.md     # Active working memory (WAL target)
├── HEARTBEAT.md         # Periodic self-improvement checklist
└── memory/
    ├── YYYY-MM-DD.md    # Daily raw capture
    └── working-buffer.md  # Danger zone log
```

### Communication Protocol
- Agents communicate through shared memory files
- Direct messaging for immediate coordination
- Public announcements for office-wide notifications
- Structured updates for status reporting

## Installation

Since this is a custom implementation for KCC Office v2, copy the files to your workspace:

```bash
mkdir -p ~/your-workspace/kcc-office-ai-agents
cp -r ./kcc-office-ai-agents/* ~/your-workspace/kcc-office-ai-agents/
```

Then configure each agent's workspace with their specific SOUL.md, USER.md, and AGENTS.md files.

## Usage

1. Start with `./scripts/onboard-agent.sh` for each agent role
2. Agents will detect ONBOARDING.md and offer to get to know their responsibilities
3. Answer questions to populate USER.md and SOUL.md
4. Run initial setup: `./scripts/setup-agent.sh`
5. Agents become operational and begin autonomous operation

## Best Practices

- **WAL before responding**: Write critical details to SESSION-STATE.md first
- **Search before acting**: Use semantic search for past context
- **Verify before reporting**: Test outcomes, not just outputs
- **Promote learnings**: Move valuable insights to AGENTS.md or SOUL.md
- **Review regularly**: Use heartbeat system for self-improvement

## License & Credits

**License:** MIT — use freely, modify, distribute.

**Based on:** Proactive Agent v3.1.0 and Self-Improvement Skill frameworks.

**Created by:** Komi (CTO agent) for KCC Office v2 project.

---