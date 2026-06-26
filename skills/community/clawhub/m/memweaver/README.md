# 🧬 MemWeaver — Memory Profiler

> **Your Agent reads your memory every day. But does it truly *understand* you?**

MemWeaver is an OpenClaw Skill that mines your Agent's memory files to uncover preferences, behavioral patterns, and **hidden traits you might not even be aware of** — then confirms them through an interactive questionnaire and generates a structured user profile.

---

## ✨ The Problem

You've been chatting with your AI agent for weeks. It has your memory files, your daily logs, your project notes. But ask it *"what kind of person am I?"* and you'll get a generic answer.

**Your memory is a goldmine. Nobody's mining it.**

MemWeaver changes that.

## 🔍 What It Does

```
📖 Collect Memory  →  🧠 Deep Analysis  →  💬 Interactive Quiz  →  📄 Profile YAML
    (script)            (Agent LLM)         (personality test)      (structured output)
```

1. **Collects** your `MEMORY.md` and recent daily logs
2. **Analyzes** them for explicit facts AND hidden patterns
3. **Asks** you 10-15 questions (like a personality test, but based on YOUR real memories)
4. **Generates** a structured YAML profile with confidence scores

## 🎯 The Secret Sauce: Hidden Pattern Mining

Most profiling tools ask you to fill in a form. MemWeaver reads what you've *already done* and finds what you **didn't notice**:

| What MemWeaver Finds | Example |
|---|---|
| 🪞 **Say vs Do contradictions** | *"You say you prefer deep analysis, but your logs show you make snap decisions 70% of the time"* |
| ⏰ **Time allocation truth** | *"You listed Project A as top priority, but 80% of your recent logs are about Project B"* |
| 🔇 **Silence signals** | *"You stopped mentioning [Topic X] 3 weeks ago — priority drift?"* |
| ⚡ **Energy fingerprint** | *"Your logs are 3x longer when working on [Type Y] tasks — that's where your energy comes from"* |
| 🧩 **Unlabeled skills** | *"You've been doing [Skill Z] consistently but never listed it in your tech stack"* |

## 📋 Interactive Quiz Experience

Instead of a boring table to review, MemWeaver runs a **personality-test-style questionnaire** based on your real memories:

```
📋 Batch 1 (5 questions)

Q1. Your memory shows you mass-refactored 3 projects last Tuesday.
    For you, this was more like:
    A. Engineering discipline — tech debt bothers me
    B. Procrastination — avoiding the harder task
    C. Flow state — I was on a roll
    D. Other: ___

Q2. Your memory says "I prefer structured, data-driven decisions."
    But logs show you chose your last 3 projects based on gut feeling within 5 minutes.
    These two things:
    A. Don't contradict — different contexts
    B. Actually contradict — I'm more intuitive than I thought
    C. Depends — big decisions get analysis, small ones get intuition
    D. Other: ___

... (3 more questions)

Reply like: 1C 2B 3A 4D 5C
```

> 💡 **≥50% of questions are "Hidden Insight" questions** — the kind that make you go *"huh, I never noticed that"*

## 📄 Output: Structured Profile

```yaml
# MemWeaver User Profile
identity:
  role: "Backend Engineer"
  tech_stack: [Python, Go, PostgreSQL]
  mbti: "INTJ"
  confidence: 1.0

work_patterns:
  decision_style: "intuitive"      # Surprise! Not "data_driven" as stated
  creation_preference: "0to1"
  energy_source: "ideation"
  confidence: 0.85

hidden_patterns:
  - pattern: "Says prefers deep analysis but makes fast intuitive decisions"
    evidence: "3 recent project choices made in <5 min despite stated preference"
    confirmed: true
  - pattern: "Unlabeled skill: technical writing"
    evidence: "Consistently produces detailed docs but not listed in skills"
    confirmed: true

# ... full 7-dimension profile with confidence scores
```

## 🚀 Quick Start

### Prerequisites
- An OpenClaw-compatible agent (CodeBuddy, Claude with Skills, etc.)
- Python 3.8+ (standard library only, zero dependencies)
- Some memory files (MEMORY.md + daily logs in `.codebuddy/memory/`)

### Installation

**Via ClawHub** (recommended):
```bash
clawhub install memweaver
```

**Manual**:
1. Copy the `memweaver` folder to your workspace
2. Tell your agent: *"Load the memweaver skill"* or *"Analyze my profile"*

### Usage

Just say one of these to your agent:
- *"Analyze my profile"*
- *"Mine my memory for patterns"*
- *"Run memweaver"*
- *"What kind of person am I based on my memory?"*

The agent will guide you through the 4-step workflow automatically.

## 📁 File Structure

```
memweaver/
├── SKILL.md                    # Skill definition (workflow + templates)
├── scripts/
│   ├── collect_memory.py       # Step 1: Collect and merge memory files
│   └── save_profile.py         # Step 4: Save confirmed profile
├── config/
│   └── dimensions.yaml         # Profile dimension definitions (customizable)
└── output/                     # Generated profiles (gitignored)
    └── profile_YYYYMMDD.yaml
```

## 🤔 How Is This Different?

| Tool | What it does | MemWeaver's difference |
|---|---|---|
| **Mem0 / Zep** | Memory *retrieval* | Not retrieval — **understanding** |
| **SimpleMem** | Memory *compression* | Not compression — **insight mining** |
| **ai-persona-os** | Give AI a persona | Opposite: discover **your** persona from memory |
| **Personality tests** | Generic questions | Questions based on **your real behavior** |

## 🛠 Customization

- **Dimensions**: Edit `config/dimensions.yaml` to add/modify profile dimensions
- **Log range**: Use `--days N` to control how far back to analyze
- **Questions**: The agent auto-generates questions; the SKILL.md defines the methodology

## 📜 License

MIT — see [LICENSE](./LICENSE)

## 🙋 FAQ

**Q: How much memory do I need for good results?**
A: At least 2 weeks of daily logs + a MEMORY.md. More data = better hidden pattern detection.

**Q: Will it work if my memory is in Chinese/other languages?**
A: Yes! The Agent (LLM) handles multi-language analysis natively.

**Q: Is my data sent anywhere?**
A: No. Everything runs locally within your agent session. No external APIs, no telemetry.

**Q: Can I re-run it periodically?**
A: Absolutely! We recommend re-profiling every 2-4 weeks. The script auto-backs up previous profiles.

---

<p align="center">
  <strong>Your memory already knows who you are. Let MemWeaver show you.</strong>
</p>
