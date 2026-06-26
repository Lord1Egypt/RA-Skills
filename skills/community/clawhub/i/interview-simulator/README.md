# 🎯 Interview Simulator

A universal, prompt-based mock interview skill powered entirely by Markdown. No code, no dependencies — just natural language.

## What Is This?

**Interview Simulator** is a Markdown-based AI skill (prompt) that transforms any LLM into a professional mock interviewer. It supports **any profession or role** and adapts dynamically to the candidate's experience level and focus area.

## Supported Roles

This skill covers **all professions**, including but not limited to:

| Category | Example Roles |
|---|---|
| 🔧 Engineering | Frontend, Backend, Mobile/Client, Full-stack, DevOps/SRE, Data, ML, Embedded, QA/Test |
| 📦 Product & Design | Product Manager, UI/UX Designer, Technical Writer |
| 💼 Business & Operations | Operations, Sales, Marketing, Business Development, Customer Success |
| 👥 People & Admin | HR / Recruiter, Accounting / Finance, Legal, Admin |
| 🎯 Other | Any role you specify! |

## Features

- ✅ **Universal** — Works for any profession, not just engineering
- ✅ **Adaptive Difficulty** — Adjusts to intern → junior → mid → senior → staff → executive
- ✅ **Multiple Interview Modules** — System design, coding, behavioral, case study, role play, domain knowledge
- ✅ **Detailed Feedback** — Per-question scoring (1–10) with strengths, improvements, and model answers
- ✅ **Session Scorecard** — Comprehensive end-of-session report with verdict
- ✅ **Resume Analysis** — Optional CV upload for targeted interviews
- ✅ **Interactive Commands** — `skip`, `hint`, `explain`, `harder`, `easier`, and more
- ✅ **Multilingual** — Automatically matches the user's language
- ✅ **Zero Dependencies** — Pure Markdown, no code required

## How to Use

### 1. Load the Skill

Copy the contents of [`SKILL.md`](./SKILL.md) into your LLM's system prompt (or use it as a custom instruction / skill file in platforms that support Markdown-based skills).

### 2. Start an Interview

Simply tell the AI what role you want to practice for. Examples:

```
Mock interview for Backend Engineer, senior level, focus on distributed systems, 45 minutes.
```

```
Mock interview for Product Manager, mid-level, focus on B2B growth.
```

```
Mock interview for Sales, junior level, focus on SaaS enterprise sales.
```

```
Mock interview for HR, senior level, focus on employee relations.
```

```
Mock interview for Accounting, mid-level, focus on financial auditing.
```

```
I have an interview for a Frontend Engineer position in 2 hours. Help me prepare.
```

```
Here is my resume [paste resume]. Please conduct a targeted interview.
```

### 3. During the Interview

- Answer questions naturally, as you would in a real interview
- Use **commands** anytime:

| Command | Action |
|---|---|
| `skip` | Skip current question |
| `hint` | Get a hint |
| `explain` | Get the ideal answer explained |
| `score` | Show running scorecard |
| `harder` / `easier` | Adjust difficulty |
| `switch [module]` | Change interview module |
| `end` | End session & get final scorecard |
| `restart` | Start over |

### 4. Get Your Results

At the end, you'll receive a detailed scorecard:

```
═══════════════════════════════════════
         📋 INTERVIEW SCORECARD
═══════════════════════════════════════
Role:            Backend Engineer
Level:           Senior
Focus:           Distributed Systems
Duration:        42 minutes
───────────────────────────────────────
Module Scores:
  • System Design:      8/10
  • Coding:             7/10
  • Behavioral:         9/10
───────────────────────────────────────
Overall Score:          8/10
Verdict:         Hire
───────────────────────────────────────
Key Strengths:
  1. Excellent understanding of CAP theorem trade-offs
  2. Clear communication of design decisions
  3. Strong leadership examples in behavioral answers

Areas for Improvement:
  1. Consider edge cases in failure scenarios
  2. Discuss monitoring and observability earlier
  3. Quantify impact in behavioral answers

Recommended Study Topics:
  1. Consensus algorithms (Raft, Paxos)
  2. Distributed tracing systems
  3. Capacity estimation techniques
═══════════════════════════════════════
```

## File Structure

```
interview-simulator/
├── SKILL.md      # The core skill definition (load this as the AI prompt)
└── README.md     # This file — documentation and usage guide
```

## Compatibility

This skill works with any LLM that supports system prompts or custom instructions:

- ChatGPT (Custom Instructions / GPTs)
- Claude (System Prompt / Projects)
- Gemini
- Any other LLM with prompt customization

## License

MIT — free to use, modify, and share.
