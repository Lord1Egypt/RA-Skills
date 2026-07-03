---
name: insight
description: "25-perspective universal AI note analysis. Multi-source: Obsidian/Flomo/Evernote/Dedao/markdown. Auto-detect note type + time range filtering + persona integration."
---

# Insight — Universal Multi-Perspective Note Analysis

25 thinking frameworks to analyze your notes. Works with Obsidian, Flomo, Evernote, Dedao, and any markdown-based note system.

## Quick Start

```
/insight                                          # Default analysis
/insight --perspective first --source obsidian     # First Principles
/insight --perspective action --source flomo       # Action Guide
/insight --persona musk --source all               # Musk persona
```

## Multi-Source Support

| Source | Flag | Setup |
|--------|------|-------|
| Obsidian | `--source obsidian` | Point to vault path |
| Flomo | `--source flomo` | MCP token (Settings → MCP) |
| Evernote | `--source evernote` | ENEX export or API |
| Dedao | `--source dedao` | Export directory |
| Generic Markdown | `--source md` | Any directory |
| All Sources | `--source all` | Search everywhere |

## Search Options

| Parameter | Default | Values |
|-----------|---------|--------|
| `--source <s>` | `obsidian` | `obsidian` / `flomo` / `evernote` / `dedao` / `md` / `all` |
| `--search <q>` | — | Free text keyword |
| `--time <r>` | `all` | `1d` / `7d` / `1m` / `3m` / `6m` / `1y` / `all` |
| `--note-type <t>` | `all` | `original` / `clip` / `all` |
| `--perspective <p>` | `default` | See 25 perspectives below |
| `--persona <name>` | — | Character persona |
| `--dir <path>` | notes dir | Any path |
| `--glob <pattern>` | `*.md` | File filter |
| `--output <mode>` | `append` | `append` / `separate` / `reply-only` |
| `--count <n>` | `5` | Notes per session |

---

## 25 Analysis Perspectives

### Self-Discovery

#### 1. Deep Scan (深度扫描)
Surface the hidden assumptions, motivations, and thinking patterns beneath your words. What are you not telling yourself?
**Range:** all notes

#### 2. Inversion Check (反向验证)
Take every conclusion in your notes and flip it. What if the opposite were true? What are you missing by looking only one way?
**Range:** all notes

#### 3. Root Cause Trace (根因追溯)
For every problem mentioned, ask "what caused that?" three times. Move from symptoms to system-level forces.
**Range:** all notes

#### 4. Contradiction Finder (矛盾定位)
Every situation has opposing forces. Find the core tension driving the dynamics — the one contradiction that, if resolved, unlocks everything else.
**Range:** 2 months

#### 5. Blind Spot Reveal (盲区揭示)
Reveal three things in your notes that you can't see about yourself: a pattern you repeat, a topic you skirt, a signal you're undervaluing.
**Range:** 6 months, original notes

#### 6. Mirror Check (镜像自检)
Step outside yourself. Read your notes as if they were written by a stranger. What would you tell this person?
**Range:** all notes

#### 7. Values Extraction (价值提取)
Your notes are a map of what you care about. Extract 3-5 core values from what you spend the most words on.
**Range:** 3 months, original notes

---

### Emotional & Mental Health

#### 8. Thought Trap Audit (思维陷阱审计)
Scan for cognitive distortions: all-or-nothing framing, catastrophizing, mind-reading, overgeneralization. For each, build a more balanced view.
**Range:** 1 month, original notes

#### 9. Non-Reaction Scan (非反应扫描)
Identify worries, grievances, and frustrations in your notes. Sort them into two piles: things you can control, and things you can't. Focus energy only on the first.
**Range:** 1 month, original notes

#### 10. Resilience Inventory (心理韧性盘点)
Find evidence of your coping strategies, support systems, and recovery patterns. What inner resources are you already using without noticing?
**Range:** 3 months, original notes

#### 11. Personality Fingerprint (人格指纹)
From your writing style, word choices, and decision descriptions, infer your cognitive preferences. Treat as exploration, not diagnosis.
**Range:** 1 year, original notes | **Frequency: low**

---

### Motivation & Direction

#### 12. Motivation Mapper (动力图谱)
What drives you shows up in your notes — sometimes clearly, sometimes in the gaps. Map what energizes you and what drains you.
**Range:** 6 months

#### 13. Inner Compass (内在罗盘)
Find the recurring questions you keep circling back to. These are clues to what you're really trying to figure out.
**Range:** 6 months

#### 14. Flywheel Blueprint (飞轮蓝图)
Connect your interests, skills, and opportunities into a self-reinforcing loop. What small win could start a compounding cycle?
**Range:** 1 year, original notes

#### 15. Life Script Edit (人生剧本编辑)
Read your notes as scenes in a story. What narrative arc are you in? Which scene needs rewriting? What's the next chapter?
**Range:** 6 months, original notes

---

### Action & Creation

#### 16. Next Step Generator (下一步生成器)
Transform every vague intention, worry, and aspiration into a concrete action. Specific, time-boxed, doable tomorrow.
**Range:** 1 year, original notes | **Frequency: high**

#### 17. Theme Weaver (主题编织)
Look across weeks of notes for emerging threads. What topics, ideas, or questions keep surfacing? What book could your notes become?
**Range:** 1 year, original notes

#### 18. Asset Inventory (资产盘点)
Catalog the knowledge, skills, connections, and tools mentioned in your notes. What do you have that you're not leveraging?
**Range:** 3 months, original notes

#### 19. Counter-Intuitive Mining (反直觉挖掘)
Search for surprising, unexpected, or "that can't be right" moments in your notes. These anomalies often contain the biggest insights.
**Range:** 3 months

#### 20. First Principles Deconstruction (第一性原理拆解)
Take a belief or decision from your notes. Strip away convention, tradition, and "how it's always done." What remains at the physical or logical bottom?
**Range:** all notes, original

---

### Quick Boost

#### 21. Daily Wins (每日亮点)
Find yesterday's small victories, moments of pride, and things that went right. Building a habit of noticing progress.
**Range:** 1 day

#### 22. Key Relationships (关键关系)
Identify the people who appear most in your notes. What role do they play? Are these relationships growing or draining you?
**Range:** 3 months

#### 23. Mental Models Audit (心智模型审计)
Analyze your notes through multiple mental models simultaneously. What does each lens reveal that the others miss?
**Range:** all notes

#### 24. Growth Patterns (成长轨迹)
Track changes in your thinking over time. What beliefs have shifted? What used to bother you that doesn't anymore?
**Range:** 1 year, original notes

#### 25. Anxiety Deconstructor (焦虑拆解器)
Break down anxious thoughts into: the observable fact, the interpretation you added, the worst-case scenario, and what's actually in your control.
**Range:** 1 month, original notes

---

## Quick Reference

| # | Perspective | Time | Type | Freq |
|---|------------|:----:|:----:|:----:|
| 1 | Deep Scan | all | all | — |
| 2 | Inversion Check | all | all | — |
| 3 | Root Cause Trace | all | all | — |
| 4 | Contradiction Finder | 2m | all | — |
| 5 | Blind Spot Reveal | 6m | original | — |
| 6 | Mirror Check | all | all | — |
| 7 | Values Extraction | 3m | original | — |
| 8 | Thought Trap Audit | 1m | original | — |
| 9 | Non-Reaction Scan | 1m | original | — |
| 10 | Resilience Inventory | 3m | original | — |
| 11 | Personality Fingerprint | 1y | original | low |
| 12 | Motivation Mapper | 6m | all | — |
| 13 | Inner Compass | 6m | all | — |
| 14 | Flywheel Blueprint | 1y | original | — |
| 15 | Life Script Edit | 6m | original | — |
| 16 | Next Step Generator | 1y | original | high |
| 17 | Theme Weaver | 1y | original | — |
| 18 | Asset Inventory | 3m | original | — |
| 19 | Counter-Intuitive Mining | 3m | all | — |
| 20 | First Principles | all | original | — |
| 21 | Daily Wins | 1d | all | — |
| 22 | Key Relationships | 3m | all | — |
| 23 | Mental Models Audit | all | all | — |
| 24 | Growth Patterns | 1y | original | — |
| 25 | Anxiety Deconstructor | 1m | original | — |

---

## Note Type Auto-Detection

| Type | Rule |
|------|------|
| `original` | No `source` field in frontmatter, or personal/internal source |
| `clip` | `source` field contains external URL, platform name, or social media |

Overridable via `--note-type`.

---

## Persona Integration

Connect with character-based personas for layered analysis:

| Persona | Lens |
|---------|------|
| `musk` | Physics-first deconstruction, cost minimalism |
| `munger` | Mental models, inversion, circle of competence |
| `feynman` | Explain-it-simply, question received wisdom |
| `jobs` | Simplicity, product intuition, "one more thing" |
| `taleb` | Antifragility, black swans, skin in the game |
| `naval` | Leverage, specific knowledge, long-term compounding |
| `graham` | Maker's schedule, startup mindset, essay thinking |
| `zhang` | Algorithm-first, delayed gratification |
| `ilya` | Deep learning intuition, first-principles AI |
| `karpathy` | Hands-on engineering, software 2.0 |
| `trump` | Deal-making, negotiation leverage |
| `mrbeast` | Viral optimization, audience attention |
| `sun` | Attention economics, market positioning |
| `mastery` | Content growth, monetization strategy |

---

## Output Modes

| Mode | Behavior |
|------|----------|
| `append` | Add to end of original note with `<!--insight:name-->` marker |
| `separate` | Create standalone: `YYYY-MM-DD-[Insight]-title-perspective.md` |
| `reply-only` | Return in chat, don't write to files |

---

## Installation

```bash
cp -r insight/ <agent-skills-dir>/insight/
```

No external dependencies. Works with any LLM agent that supports skills.
