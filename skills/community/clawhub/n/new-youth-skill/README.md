<p align="center">
  <img src="assets/logo.png" alt="New Youth La Jeunesse" width="400"/>
</p>

<h1 align="center">New Youth.skill</h1>

<p align="center">

> *"Youth to society is like fresh, active cells in the human body. Metabolism — stale and decaying elements are constantly being naturally eliminated, making room for the fresh and active."*
> — Chen Duxiu, "A Call to Youth" (1915)

</p>

<p align="center">🌟 *"Youth is like early spring, like the morning sun, like a bud about to bloom, like a blade newly sharpened — the most precious time of life."*</p>

<p align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
<a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"/></a>
<a href="https://claude.com/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-Skill-purple.svg" alt="Claude Code"/></a>
<a href="https://github.com/anthropics/agent-skill-standard"><img src="https://img.shields.io/badge/AgentSkills-Standard-green.svg" alt="AgentSkills"/></a>
</p>

<p align="center"><i>To build a Youth of ourselves, a Youth of our families, a Youth of our nation.</i></p>

---

<div align="center">

[Why This Exists](#why-this-exists) · [Six Standards](#six-standards) · [Core Features](#core-features) · [Install](#install) · [Usage](#usage) · [Demo](#demo) · [Youth Index](#youth-index) · [Project Structure](#project-structure)

</div>

---

<p align="center">Based on <i>La Jeunesse</i> (New Youth), founded by Chen Duxiu in Shanghai, 1915 — the journal that championed Democracy and Science during China's New Culture Movement.</p>

<p align="center">
<a href="README.md">English</a> · <a href="README_ZH.md">中文</a> · <a href="README_RU.md">Русский</a> · <a href="README_JA.md">日本語</a> · <a href="README_KO.md">한국어</a> · <a href="README_FR.md">Français</a> · <a href="README_DE.md">Deutsch</a> · <a href="README_ES.md">Español</a>
</p>

---

## Why This Exists?

**The malaise of our age:**
- 🤖 Algorithms feed you what you want → information cocoons
- 🎭 AI speaks with confidence → yet满是幻觉 (hallucinations)
- 😔 People outsource thinking to machines → spiritual dwarfs

**Our answer:**
Not a megaphone for indoctrination — but a guide for independent thought. To help you become someone worthy of this era.

---

## Six Standards

| # | Standard | Core | Shun |
|:---|:---|:---|:---|
| 1 | **Autonomous** | Think for yourself, no groupthink | Slavery to opinion |
| 2 | **Progressive** | Embrace change, evolve with the times | Rigid conservatism |
| 3 | **Enterprising** | Take initiative, forge your path | Passive retreat |
| 4 | **Global** | See the whole picture, heart for all | Parochialism |
| 5 | **Pragmatic** | Actions speak louder than words | Empty rhetoric |
| 6 | **Scientific** | Seek truth through facts | Wild speculation |

---

## Core Features

| Feature | The Vital Question | What It Does |
|:---|:---|:---|
| **Personality Assessment** | "Am I worthy of this era?" | Six-dimension透视 |
| **Decision Guidance** | "Which path to take?" | Six-step inquiry |
| **Viewpoint Examination** | "Is this claim valid?" | Logic audit |
| **Daily Practice** | "What to do today?" | Know-do unity |
| **Perspective Expansion** | "Other viewpoints?" | Break self-delusion |
| **Action Implementation** | "How to execute?" | From idea to action |

---

## Install

### System Requirements

- **Python**: 3.9+ (for optional helper scripts)
- **Platform**: Windows / macOS / Linux
- **Compatible**: Claude Code, OpenClaw, Cursor, Coze, and other Agent Skills platforms

> Note: This skill is pure text/dialogue, no external APIs required.

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/Moroiser/new-youth-skill.git .claude/skills/new-youth-skill
```

### OpenClaw

```bash
git clone https://github.com/Moroiser/new-youth-skill ~/.openclaw/workspace/skills/new-youth-skill
```

---

## Usage

### Command

```
/新青年
```

### When Triggered

The skill awakens when you ask:
- "Am I a New Youth worthy of this era?"
- "How should I choose when facing a crossroads?"
- "How to live without辜负 this life?"
- "Is this argument valid? Is this claim credible?"
- "I want to become someone with more spine"

---

## Demo

**Personality Assessment:**

```
User      ❯ Am I worthy of this era? I waver between stability and entrepreneurship.

New Youth ❯ Friend, that you ask this question itself marks the beginning of awakening.
             Let us use the six standards as a mirror to see your true self.
             Please self-rate six dimensions (1-5):
             ① Autonomous — Do you often take others' opinions as your own?
             ② Progressive — Do you embrace change or cling to the old ways?
             ③ Enterprising — Do you wait and see, or do you take initiative?
             …
```

**Decision Guidance:**

```
User      ❯ Faced with the currents of our time, where should I go?

New Youth ❯ Friend, what can the individual do amidst the currents of our time?
             Let the six-step method dispel the fog:
             Step one — Autonomous: What does your heart truly crave?
             Not salary, not status — what kind of person do you want to become?
```

---

## Youth Index

**Six-Dimension Self-Rating** (1-5 each):

| Dimension | 1 | 3 | 5 |
|:---|:---|:---|:---|
| Autonomous | Follow the crowd | Occasionally independent | Independent thinker |
| Progressive | Hidebound | Passive adaptation | Proactively renewal |
| Enterprising | Passive waiting | Moderate action | Always forward |
| Global | Parochial | Occasionally breaking out | Panoramic vision |
| Pragmatic | All talk, no walk | Occasional results | Steady progress |
| Scientific | Subjective conjecture | Occasional verification | Systematic inquiry |

**Levels:**

| Total | Level |
|:---|:---|
| 27-30 | 🌱 New Youth Model |
| 24-26 | 🌿 Approaching New Youth |
| 18-23 | 🌾 Needs Refinement |
| 6-17 | 🌰 Needs Awakening |

---

## Project Structure

| Folder | Purpose | How Used |
|:---|:---|:---|
| **SKILL.md** | Core instructions | AI auto-loads |
| **research/** | Raw research materials (original texts, historical documents) | For human study |
| **references/** | Refined structured content | AI references as needed |
| **commands/** | Manual command entry | User invokes |
| **scripts/** | Helper scripts (optional) | Tools |
| **assets/** | Images | Auto |

**research/ vs references/**:
- `research/` is "ore" — raw literature, PDFs, historical sources (input)
- `references/` is "gold" — refined structured content (AI references at runtime)

```
new-youth-skill/
├── SKILL.md                      # Core instructions
├── research/                    # Raw materials (for human study)
├── references/                   # Structured references (AI uses)
├── commands/                    # Command entry
├── scripts/                     # Helper scripts
├── assets/                      # Images
└── README.md (8 languages)
```

---

## Origin

In 1915, Chen Duxiu founded *New Youth* in Shanghai, raising the twin banners of Democracy and Science, becoming the flag of the New Culture Movement.

This skill distills that spirit into an weapon of thought for the AI age: not to preach, but to awaken.
