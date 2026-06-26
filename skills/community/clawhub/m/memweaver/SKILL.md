---
name: memweaver
description: "Memory Profiler — Mine hidden patterns from your Agent's memory, confirm via interactive quiz, and generate a structured user profile."
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# MemWeaver — Memory Profiler

> Your Agent reads your memory every day, but does it truly *understand* you?

MemWeaver digs into your memory files — long-term memory (`MEMORY.md`) and daily logs — to uncover preferences, behavioral patterns, and **hidden traits you might not even be aware of**, then confirms findings through an interactive questionnaire and outputs a structured user profile (YAML).

## What Makes This Different

| Existing tools | What they do | What MemWeaver does differently |
|---|---|---|
| Mem0 / Zep | Memory **retrieval** | Not retrieval — **understanding** |
| SimpleMem / LightMem | Memory **compression** | Not compression — **insight mining** |
| ai-persona-os | Give AI a persona | Opposite direction: discover **your** persona from memory |

**Core value**: MemWeaver finds the gap between what you *say* you prefer and what you *actually do* — then asks you about it.

## Overview

- **Input**: `MEMORY.md` (long-term memory) + recent daily logs (`memory/*.md`)
- **Process**: LLM deep analysis → batch interactive questionnaire
- **Output**: Structured user profile at `output/profile_YYYYMMDD.yaml`

## Workflow

### Step 1: Collect Memory

```bash
cd {baseDir} && python3 scripts/collect_memory.py --days 14
```

The script reads long-term memory and recent logs, outputs JSON to stdout. The Agent parses `content.long_term` and `content.daily_logs` fields from the JSON.

**Note**: If `estimated_tokens` exceeds 8000, consider reducing the `--days` parameter.

### Step 2: LLM Deep Analysis

The Agent analyzes collected memory in 3 sub-tasks:

#### 2.1 Basic Profile Extraction

Extract factual information from memory across these dimensions:

| Dimension | What to extract | Confidence source |
|---|---|---|
| Identity | Role, tech stack, MBTI | Explicit statements → 1.0 |
| Work patterns | Active projects, decision style, creation preference | Behavioral inference → 0.7-0.9 |
| Interests | Professional interests, hobbies, depth of engagement | Topic frequency → 0.6-0.9 |
| Communication | Response depth preference, format preference, dislikes | Interaction pattern → 0.7-0.85 |
| Long-term goals | Career direction, product plans, values | Explicit statements → 0.9-1.0 |

Tag each field with a `confidence` score.

#### 2.2 Hidden Pattern Mining

This is MemWeaver's most valuable part. The Agent specifically analyzes these 6 types of hidden patterns:

1. **Decision patterns**: What does the user lean toward when facing multiple options? (Analysis-driven vs intuition? Fast vs slow decisions?)
2. **Time & energy allocation**: Does actual energy distribution (from log frequency) match user's self-description?
3. **Overlooked interests**: Topics that appear repeatedly but the user hasn't formally tracked
4. **Statement vs behavior contradictions**: Are stated preferences inconsistent with actual actions?
5. **Emotion/energy triggers**: What scenarios make the user especially productive or resistant?
6. **Unlabeled skills**: Abilities the user demonstrates but hasn't self-recognized

Each finding needs **evidence** (citing specific memory content) and **reasoning logic**.

#### 2.3 Project Importance Re-evaluation

List every project and idea recorded in MEMORY.md, provide reassessment:

- Current status (active / paused / archived / concept)
- Suggested importance (high / medium / low / shelved)
- Assessment reasoning (frequency in logs, recent activity, user investment)
- Questions to confirm with user (if uncertain)

### Step 3: Interactive Confirmation (Batch Questionnaire)

Interact with the user in **batch mode**, similar to a personality test. Each question is based on the user's actual memory content, not just showing analysis conclusions.

**Core design principles**:
- **Push 5 questions per batch**, user answers at once (e.g., "1A 2C 3B 4D 5A"), Agent provides feedback then pushes next batch
- Questions reference user's real memories as context
- Provide options (A/B/C/D or open-ended), user can choose or free-form
- **Type B (hidden insight) questions should be ≥50% of total** — this is MemWeaver's core value
- Three question types interleaved, not strictly separated by rounds

**Question Design Rules**:

The Agent designs 10-15 questions based on Step 2 analysis. Three types:

#### Type A: Scenario Recall (validate profile facts, ≤25%)

Reconstruct a real scene from memory, let user choose the best description.

```
📋 Q1.

Your memory shows you did [specific behavior] on [specific date].
For you, this was more like:

A. [option: engineering intuition / habit-driven]
B. [option: lesson learned]
C. [option: personality-driven]
D. Other: ___
```

#### Type B: Hidden Insight (core value, ≥50%)

**This is MemWeaver's most important question type.** The Agent uses specific evidence from memory to point out contradictions or blind spots between user's "self-perception" and "actual behavior".

**Methodology**:
1. Find user's **explicit statement** (e.g., "I prefer X")
2. Find **contradictory behavioral records** (e.g., logs show consistently doing Y)
3. Present the contradiction to user, guide explanation via options
4. Options should include: acknowledge contradiction, deny, offer new explanation, other

```
📋 Q5.

Your memory says "[user's explicit statement]".
But logs show from [date A] to [date B] you've been consistently doing [contradictory behavior].

These two things:
A. Don't contradict — [reasonable explanation]
B. Actually contradict — my real preference differs from self-perception
C. Depends on context — [conditional explanation]
D. Other: ___

> 🔍 Your words say X, but your actions say Y
```

**Hidden insight mining directions** (look for these 6 types of clues in memory):
1. **Statement vs behavior contradictions**: Stated preferences inconsistent with actual actions
2. **Time allocation truth**: Log frequency/length reveals real energy distribution vs stated priorities
3. **Silence signals**: Topics in MEMORY that disappear from logs → possible priority drift
4. **Energy fingerprint**: Length differences across log types → reveals energy sources
5. **Choice patterns**: Consistent tendencies when user faces decisions
6. **Unlabeled skills**: Abilities demonstrated but not self-recognized

#### Type C: Priority Trade-off (re-evaluate project importance, ≤25%)

Create resource-constraint scenarios, force user to choose between projects, revealing true priorities.

```
📋 Q10.

If you could only advance 2 personal projects next month (work doesn't count),
your memory mentions these: [project list from MEMORY.md]

Which two?
A. [Project1] + [Project2]
B. [Project1] + [Project3]
C. [Project2] + [Project3]
D. Other combination: ___
```

**Question count and batching**:
- Total **10-15 questions**, pushed in **2-3 batches** (~5 per batch)
- Batch 1 (5 questions): 1-2 warm-up Type A + 3 Type B (hidden insights)
- Batch 2 (5 questions): 3-4 Type B + 1-2 Type C (priority trade-offs)
- Optional Batch 3 (2-3 questions): follow-up questions based on unexpected findings from previous batches
- After each batch, Agent waits for user to answer all at once

**Answer processing**:
- After user submits a batch (e.g., "1C 2B 3A 4B 5C"), Agent processes collectively
- Give 1 brief feedback per question, noting profile inference
- If an answer reveals new insight leads, add follow-up questions in next batch
- All answers recorded internally as profile evidence, aggregated into Step 4

**Completion**:
- After the last batch, Agent outputs a brief **profile summary** (like a personality test result page)
- Then proceeds to Step 4

### Step 4: Generate and Save Profile

Generate the confirmed profile as YAML and save via script:

1. Agent generates complete YAML profile (see "Profile Template" below)
2. Save via script:

```bash
cd {baseDir} && python3 scripts/save_profile.py --file /tmp/memweaver_profile.yaml
```

Or via stdin:

```bash
echo '<YAML content>' | cd {baseDir} && python3 scripts/save_profile.py
```

The script automatically backs up old profiles and saves to `output/profile_YYYYMMDD.yaml`.

---

## Profile Template

```yaml
# MemWeaver User Profile
# Generated: YYYY-MM-DD
# Version: 1

identity:
  role: ""
  tech_stack: []
  mbti: ""
  confidence: 1.0

work_patterns:
  decision_style: ""    # data_driven / intuitive / consultative
  detail_preference: "" # high / medium / low
  creation_preference: "" # 0to1 / polish / both
  energy_source: ""     # ideation / execution / collaboration
  work_rhythm: ""       # burst / steady / mixed
  confidence: 0.0

interests:
  professional:
    - topic: ""
      depth: ""         # expert / active_research / exploring / casual
      importance: ""    # high / medium / low
      last_active: ""
  personal:
    - topic: ""
      depth: ""
      importance: ""

communication:
  preferred_depth: ""   # deep_analysis / balanced / brief
  preferred_format: ""  # structured / narrative / mixed
  language: ""
  dislikes: []

goals:
  career:
    - goal: ""
      priority: ""      # high / medium / low / shelved
      timeframe: ""     # immediate / short_term / long_term
  products:
    - name: ""
      priority: ""
      status: ""        # active / designing / idea / archived

hidden_patterns:
  - pattern: ""
    evidence: ""
    confirmed: false

projects:
  - name: ""
    importance: ""      # high / medium_high / medium / low / shelved
    status: ""          # active / iterating / designing / exploring / archived / idea

meta:
  generated_at: ""
  memory_files_analyzed: 0
  total_memory_lines: 0
  user_confirmed: true
  next_review: ""       # Suggest re-profiling in 2 weeks
```

## Output

- User profile: `{baseDir}/output/profile_YYYYMMDD.yaml`
- Analysis cache: `{baseDir}/cache/analysis_cache.json` (future version)

## Requirements

No external dependencies. Python 3.8+ standard library only.
