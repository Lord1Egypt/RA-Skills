---
name: knowledge-distillation
description: Distill OpenClaw daily memory, session transcripts, and newly generated report files into new knowledge points and deeper knowledge leads. Use when the input is workspace-native materials such as MEMORY.md, memory/*.md, session logs, daily notes, summaries, or generated report files, and the goal is to extract (1) newly formed knowledge worth retaining and (2) promising knowledge threads worth further study. Output should be a dated Markdown file.
version: 1.1.0
---

# Knowledge Distillation

## Overview

This skill is an **OpenClaw internal knowledge distiller**.

Its job is not to summarize everything. Its job is to scan agent-native working materials, identify what is newly learned, and separate that from what should be investigated, connected, or strengthened next.

## Input Scope

Use this skill when the source materials come from the OpenClaw environment, especially:

- `MEMORY.md`
- `memory/*.md`
- session transcripts or conversation logs
- newly generated report files
- daily review notes
- task summaries and execution reports

Treat these as raw internal learning material.

## Core Objective

From the input set, produce two things:

1. **New Knowledge Points**
   - information that now appears stable enough to retain
   - repeatable patterns, conclusions, heuristics, rules, or insights
   - decisions or lessons that deserve long-term reuse

2. **Knowledge Leads Worth Deepening**
   - incomplete but promising patterns
   - recurring signals without enough confidence yet
   - tensions, contradictions, anomalies, or open questions
   - topics worth another round of observation, validation, or focused research

## Workflow

### 1. Classify the source material

Identify what each input contributes:

- long-term memory
- recent memory
- session/process evidence
- generated report or analysis artifact

Do not treat all sources equally. Give more weight to repeated evidence across multiple sources.

### 2. Extract candidate signals

Look for:

- repeated observations
- recurring user preferences
- stable work rules
- decision patterns
- successful or failed workflows
- bottlenecks that appear more than once
- newly surfaced concepts or frameworks

Prefer signal over chronology.

### 3. Distinguish stable knowledge from emerging leads

Promote something to **New Knowledge Points** only when at least one of these is true:

- it appears repeatedly across days or sessions
- it has already affected real decisions or behavior
- it has clear reuse value
- it is specific enough to guide future action

Keep something in **Knowledge Leads Worth Deepening** when:

- evidence is partial
- it shows potential but not enough stability
- it conflicts with older observations
- it needs targeted follow-up material

### 4. Merge duplicates and raise abstraction

Do not list near-duplicate observations separately.

Merge them upward into:

- a principle
- a rule of thumb
- a workflow lesson
- a reusable framework
- a watchpoint for future review

### 5. Add explicit basis

Each knowledge point should include a short basis such as:

- what kind of source supported it
- whether it appeared once or repeatedly
- whether it is high-confidence or tentative

Do not fabricate precision. Keep basis brief and honest.

### 6. End with next-step deepening suggestions

For each deepen-able knowledge point, explain how to deepen it, for example:

- keep observing for 3-7 more days
- compare against older sessions
- collect one more concrete case
- convert into an explicit workflow rule
- ask a targeted question next time
- create a dedicated report around the topic

## Output Requirements

The output must be a **dated Markdown file**.

Filename format:

- `knowledge-distillation-YYYY-MM-DD.md`

If multiple runs happen on the same day, use one of:

- `knowledge-distillation-YYYY-MM-DD-01.md`
- `knowledge-distillation-YYYY-MM-DD-02.md`

## Required Output Structure

Use this structure unless the user explicitly asks for another one:

```markdown
# Knowledge Distillation - YYYY-MM-DD

## Input Summary
- Memory files:
- Session/log sources:
- Report files:

## New Knowledge Points
### 1. Title
- Conclusion:
- Basis:
- Value:
- Scope:

### 2. Title
- Conclusion:
- Basis:
- Value:
- Scope:

## Knowledge Leads Worth Deepening
### 1. Title
- Current observation:
- Why worth deepening:
- Current gaps:
- Next step suggestions:

### 2. Title
- Current observation:
- Why worth deepening:
- Current gaps:
- Next step suggestions:

## Distillation Conclusions This Round
- Most worth retaining (1-3 points):
- Most worth tracking (1-3 leads):
```

For reusable variants, read `references/output-templates.md`.

## Script Usage

```bash
# Explicit input/output directories
bash scripts/distill.sh ./memory ./dist

# Or use environment variables
KNOWLEDGE_DISTILLATION_MEMORY_DIR=./memory KNOWLEDGE_DISTILLATION_OUTPUT_DIR=./dist bash scripts/distill.sh

# Release/package verification
bash scripts/test.sh
```

`scripts/distill.sh` creates a dated Markdown draft with the required structure.
It does not automatically claim new knowledge; the agent must fill the draft
from reviewed source material and label evidence strength honestly.

## Quality Rules

- Do not write a generic summary of the inputs.
- Do not merely restate chronology.
- Do not promote weak hints into firm knowledge.
- Do not bury the “new knowledge” section under background detail.
- Prefer fewer stronger points over many shallow points.
- If nothing truly qualifies as new knowledge, say so honestly.

## Good Trigger Examples

Use this skill for requests like:

- “把最近的 memory 和 session 蒸馏一下”
- “从最近日报和会话里提炼新的知识点”
- “看这些报告文件，找出值得沉淀和继续深化的点”
- “把 OpenClaw 这几天的运行材料蒸馏成知识”
- “输出一个今天的知识蒸馏 md 文件”

## Resources

### references/

- `references/output-templates.md`: dated Markdown output variants for standard runs, report-heavy runs, and follow-up runs
