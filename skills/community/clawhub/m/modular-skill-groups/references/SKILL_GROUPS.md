# SKILL_GROUPS.md — Modular Skill Activation System

## Overview
Skills are organized into named groups. Each group has an `active` flag.
Only skills in the active group are loaded at session start (unless a skill is explicitly needed).
This keeps context windows clean and reduces token burn.

## How It Works
- `ACTIVE_GROUP`: Set via `~/.openclaw/active_skill_group` file (one group name, no trailing whitespace)
- Session start: read `ACTIVE_GROUP`, load skills from that group only (plus always-loaded CORE skills)
- Skill lookup: if a skill from an inactive group is needed, it can be loaded explicitly
- To switch groups: `echo "group-name" > ~/.openclaw/active_skill_group`

## Always-Loaded Core (never need to switch)
These skills are so lightweight/multi-use they load in every session:
- `self-improving` — self-reflection and memory
- `proactivity` — anticipation and follow-through
- `sub-agent-orchestrator` — team coordination
- `research-assistant` — web search and summarization

---

## GROUP: agent-builder  (DEFAULT — M.ai.K.R development)
**Description:** Building and operating the M.ai.K.R agent SaaS platform
**Active by default**

Skills (20):
- ai-agent-builder
- analytics
- automation-workflows
- calendar-manager
- client-onboarding-automator
- customer-onboarding-guider
- director
- email-automation
- invoice-generator
- javascript-skills
- meeting-intelligence
- node-connect
- prisma
- sql-toolkit
- stripe-best-practices
- task-queue
- code-cog
- file-organizer
- data-analysis
- data-visualization-2

---

## GROUP: creative
**Description:** Game development, art direction, image generation, multimedia

Skills (9):
- game-ai
- game-design-philosophy
- image-cog
- best-image-generation
- react-native
- video-frames
- music_generate (tool)
- image_generate (tool)
- agent-browser-clawdbot

---

## GROUP: research
**Description:** Deep research, competitive analysis, web intelligence

Skills (5):
- cellcog
- research-assistant
- content-repurposer
- business-doc-generator
- web_fetch (tool)

---

## GROUP: marketing
**Description:** Lead generation, outreach, email automation, social

Skills (6):
- client-outreach-automator
- email-automation
- content-repurposer
- meeting-intelligence
- invoice-generator
- calendar-manager

---

## GROUP: minimal
**Description:** Bare minimum — only CORE skills, nothing else loads.
Use when doing simple Q&A or when context is tight.

Skills: (none beyond CORE)

---

## Skill → Group Map (quick lookup)

| Skill | Group |
|-------|-------|
| ai-agent-builder | agent-builder |
| analytics | agent-builder |
| automation-workflows | agent-builder |
| calendar-manager | agent-builder |
| client-onboarding-automator | agent-builder |
| client-outreach-automator | marketing |
| code-cog | agent-builder |
| content-repurposer | research |
| customer-onboarding-guider | agent-builder |
| data-analysis | agent-builder |
| data-visualization-2 | agent-builder |
| business-doc-generator | research |
| best-image-generation | creative |
| email-automation | marketing |
| elite-longterm-memory | core (always) |
| file-organizer | agent-builder |
| game-ai | creative |
| game-design-philosophy | creative |
| image-cog | creative |
| invoice-generator | marketing |
| javascript-skills | agent-builder |
| meeting-intelligence | marketing |
| mem-redis | core (always) |
| music_generate | creative |
| n8n-workflow-builder | agent-builder |
| node-connect | agent-builder |
| prisma | agent-builder |
| proactivity | core (always) |
| qdrant-memory | core (always) |
| react-native | creative |
| research-assistant | research |
| self-improving | core (always) |
| sql-toolkit | agent-builder |
| stripe-best-practices | agent-builder |
| sub-agent-orchestrator | core (always) |
| task-queue | agent-builder |
| video-frames | creative |

---

## Switching Groups

```bash
# Switch to agent-builder mode (M.ai.K.R development)
echo "agent-builder" > ~/.openclaw/active_skill_group

# Switch to creative mode
echo "creative" > ~/.openclaw/active_skill_group

# Switch to research mode
echo "research" > ~/.openclaw/active_skill_group

# Switch to marketing mode
echo "marketing" > ~/.openclaw/active_skill_group

# Minimal mode (tight context)
echo "minimal" > ~/.openclaw/active_skill_group
```

## Custom Groups
Add new groups at the bottom of this file following the same format.
