# Council of Wisdom - Project Summary

**Created:** 2026-03-07
**For:** Fayez (Miknas)
**Project Type:** Multi-Agent AI Debate System

---

## What Was Built

A sophisticated multi-agent AI debate framework called **Council of Wisdom** that enables structured debates between expert agents with automatic voting, cleanup, and enterprise-grade monitoring.

---

## Project Structure

```
council-of-wisdom/
├── SKILL.md                    # Complete skill documentation (18.7KB)
├── README.md                   # Quick start guide
├── IMPLEMENTATION.md           # Technical implementation guide (10KB)
├── _meta.json                  # ClawHub metadata
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions CI/CD
├── scripts/
│   ├── council-of-wisdom.sh    # Main CLI (17.4KB)
│   └── validate-skill.sh       # Validation script
└── templates/
    ├── referee-prompt.md       # Referee agent prompt (7.3KB)
    ├── debater-prompt.md       # Debater agent prompt (8.1KB)
    └── council-prompts.md      # 9 council member prompts (13.4KB)
```

---

## Key Features

### 1. **Structured Debate System**
- 2 Master Debaters with opposing viewpoints
- 9 Council members with distinct analytical frameworks
- Referee agent orchestrates entire debate flow

### 2. **Council of 9 Expert Frameworks**
1. **Logician** - Formal logic, fallacy detection
2. **Empiricist** - Evidence-based analysis
3. **Pragmatist** - Real-world applicability
4. **Ethicist** - Moral frameworks and fairness
5. **Futurist** - Long-term implications
6. **Historian** - Precedent analysis
7. **Systems Thinker** - Holistic view
8. **Risk Analyst** - Failure mode analysis
9. **Synthesizer** - Integration and hybrid solutions

### 3. **Automatic Agent Lifecycle**
```
Spawn → Debate → Vote → Report → Cleanup
```
- Council agents terminated after voting
- Context cleared for next query
- Logs archived automatically

### 4. **Multi-LLM Provider Support**
- Different providers for each council member
- Random assignment for diverse reasoning
- Supports: OpenAI, Anthropic, Google, Zai, etc.

### 5. **Enterprise Monitoring (5-Cadence)**
- **Daily:** Debate quality, agent performance
- **Weekly:** Decision impact, user feedback
- **Monthly:** Council effectiveness, ROI
- **Quarterly:** Strategic alignment, scalability
- **Annually:** Vision review, evolution

### 6. **Comprehensive Testing**
- Unit tests for individual agents
- Integration tests for full flow
- Quality checks for argument depth
- Performance tests for scalability

### 7. **GitHub Integration**
- Private repository for each project
- Automated issue tracking
- GitHub Actions for CI/CD
- Wiki for knowledge base

---

## Quick Start

### Initialize a Council

```bash
# Make CLI available
chmod +x ~/.openclaw/workspace/skills/council-of-wisdom/scripts/council-of-wisdom.sh

# Initialize a new council project
~/.openclaw/workspace/skills/council-of-wisdom/scripts/council-of-wisdom.sh init strategic-decisions
```

This creates:
```
council-of-wisdom/strategic-decisions/
├── workspace/
│   ├── strategy.md              # Define council purpose
│   ├── monitoring/              # Metrics & dashboards
│   ├── testing/                 # Test cases
│   ├── feedback/                # User feedback
│   ├── prompts/                 # Agent prompts
│   ├── agents/                  # Agent configs
│   ├── logs/                    # Debate transcripts
│   └── reports/                 # Outcome reports
├── .github/                     # GitHub integration
└── README.md
```

### Run a Debate

```bash
council-of-wisdom debate \
  "Should we use microservices or monolithic architecture?" \
  --domain software-architecture \
  --perspective-a "Microservices offer scalability and independent deployment" \
  --perspective-b "Monolith offers simplicity and lower operational overhead"
```

### View Outcome Report

```bash
council-of-wisdom report debate-20260307-001
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     QUERY / ADVISE                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    REFEREE AGENT                            │
│  • Receives query                                           │
│  • Orchestrates debate                                      │
│  • Manages council voting                                   │
│  • Delivers structured outcome                              │
└─────────────┬───────────────────────┬───────────────────────┘
              │                       │
              ▼                       ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│    MASTER DEBATER A     │  │    MASTER DEBATER B     │
│  • Domain expert #1     │  │  • Domain expert #2     │
│  • Persuasive arguments │  │  • Persuasive arguments │
└─────────────────────────┘  └─────────────────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              COUNCIL OF 9 EXPERTS                            │
│  • Each votes independently                                 │
│  • Unique analytical perspective                            │
│  • Multi-LLM provider support                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STRUCTURED OUTCOME REPORT                       │
│  • Winner declaration                                        │
│  • Vote tally                                                │
│  • Key arguments from each side                              │
│  • Council consensus insights                                │
│  • Actionable recommendations                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Requirements

### Prerequisites
1. **OpenClaw with ACP runtime** - For agent spawning
2. **Agent IDs configured** - Referee, 2 Debaters, 9 Council members
3. **GitHub CLI (`gh`)** - For repo integration (optional but recommended)

### Next Steps

1. **Review SKILL.md** - Complete documentation
2. **Read IMPLEMENTATION.md** - Technical guide for ACP integration
3. **Initialize a project** - `council-of-wisdom init <project-name>`
4. **Configure agents** - Set up agent IDs in OpenClaw
5. **Test debate flow** - Run a test debate to verify all components
6. **Set up monitoring** - Configure metrics and dashboards

---

## Strategy & Monitoring Built-In

### Strategy Framework
Every council project has a `strategy.md` with:
- Council Purpose
- Domain Expertise
- Decision Criteria
- Stakeholders
- Success Metrics

### Monitoring System
5-Cadence operating rhythm with:
- Debate quality metrics
- Agent performance metrics
- Outcome metrics
- Operational metrics

### Testing Framework
- Unit tests for individual agents
- Integration tests for full flow
- Quality checks for argument depth
- Performance tests for scalability

### Feedback & Optimization
- User feedback capture
- Automated prompt optimization
- Provider tuning
- Continuous improvement

---

## GitHub Repository

Each Council of Wisdom project has its own private GitHub repo:

```bash
cd ~/.openclaw/workspace/council-of-wisdom/<project-name>
gh repo create council-<project-name> --private --source=. --remote=origin --push
```

---

## Files Reference

| File | Purpose | Size |
|------|---------|------|
| **SKILL.md** | Complete skill documentation | 18.7KB |
| **IMPLEMENTATION.md** | Technical implementation guide | 10KB |
| **README.md** | Quick start guide | 3KB |
| **_meta.json** | ClawHub metadata | 1.3KB |
| **council-of-wisdom.sh** | Main CLI | 17.4KB |
| **referee-prompt.md** | Referee agent prompt | 7.3KB |
| **debater-prompt.md** | Debater agent prompt | 8.1KB |
| **council-prompts.md** | 9 council member prompts | 13.4KB |
| **test.yml** | GitHub Actions workflow | 9KB |

---

## Enterprise Features

✅ **Multi-Agent Orchestration** - Complex debate flows
✅ **Automatic Cleanup** - No memory leaks, clean state each query
✅ **Multi-Provider Support** - Diverse reasoning patterns
✅ **5-Cadence Monitoring** - Daily to yearly reviews
✅ **Comprehensive Testing** - Unit, integration, quality, performance
✅ **Feedback Loops** - Continuous optimization
✅ **GitHub Integration** - Version control, CI/CD, issues
✅ **Scalable Architecture** - Horizontal and vertical scaling
✅ **Private by Default** - All repos private (Fayez's preference)
✅ **Strategy-First** - Every project has defined strategy

---

## Example Use Cases

1. **Technical Architecture Decisions**
   - "Should we use microservices or monolith?"

2. **Product Strategy**
   - "Should we prioritize speed or quality?"

3. **Marketing Strategy**
   - "SEO content vs. paid ads?"

4. **Investment Decisions**
   - "Should we invest in AI or human expertise?"

5. **Process Design**
   - "Should we automate or keep manual?"

---

## Next Actions

1. ✅ **Skill created** - Complete framework built
2. ⏭️ **Review documentation** - Read SKILL.md and IMPLEMENTATION.md
3. ⏭️ **Initialize first council** - Run `council-of-wisdom init strategic-decisions`
4. ⏭️ **Configure agents** - Set up agent IDs in OpenClaw
5. ⏭️ **Test debate flow** - Run first test debate
6. ⏭️ **Set up monitoring** - Configure metrics and dashboards

---

**Council of Wisdom: Structured debate, collective intelligence, actionable decisions.**

*Built with Skill Forge for Fayez (Miknas)*
