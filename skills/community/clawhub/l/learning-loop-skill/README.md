# Learning Loop Skill — The GEARS System

An [OpenClaw](https://openclaw.com) skill for autonomous structured learning. Master complex topics through cron-based feedback loops that run without supervision.

## How It Works

GEARS is a 5-session daily cycle:

| Phase | Session | What Happens |
|-------|---------|-------------|
| **G**ather | S1 | Research concepts, create test questions |
| **E**xecute | S2 | Take the test blind, document failures |
| **A**nalyze | S3 | Diagnose why you failed, research solutions |
| **R**etry | S4 | Apply fixes, measure improvement |
| **S**ynthesize | S5 | Validate mastery, adjust schedule |

Say "learn machine learning" and the agent:
1. Researches the topic and builds a curriculum (15-20 subtopics)
2. Generates a self-contained playbook for isolated cron agents
3. Schedules 5 sessions per day — each runs autonomously
4. Tracks scores, advances on mastery (>=85%), retries on gaps

## Install

### From ClawHub

```bash
clawhub install learning-loop-skill
```

### Manual

Copy this directory into your OpenClaw skills folder:

```bash
cp -r learning-loop-skill ~/.openclaw/workspace/skills/
```

The skill is discovered automatically — no restart needed.

## Usage

Tell your agent:

- "Learn Kubernetes"
- "Teach me database design"
- "Master Docker networking"
- "Deep dive into distributed systems"

The agent sets up the pipeline interactively, then cron jobs handle the rest.

## Scoring & Progression

| S4 Score | Action |
|----------|--------|
| >= 85% | Subtopic mastered, advance to next |
| 50-84% | Retry same subtopic tomorrow |
| < 50% | Flag for user intervention |

## Commands

Check progress on active learning topics:

```bash
bash scripts/check_progress.sh           # all topics
bash scripts/check_progress.sh docker     # specific topic
```

Pause/resume via your agent:
- "Pause learning Docker"
- "Resume learning Docker"

## Structure

```
memory/learning/<topic-slug>/
├── playbook.md          # Instructions for cron agents
├── state.json           # Progress tracker
├── curriculum.md        # Subtopic breakdown
├── sessions/day-NN/     # Daily session outputs
└── knowledge/validated.md  # Accumulated mastery
```

## License

[MIT](LICENSE)
