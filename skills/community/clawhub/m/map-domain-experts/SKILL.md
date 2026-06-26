---
name: map-domain-experts
description: Use when a user wants to quickly learn a domain/field/领域 by mapping representative experts, scholars, practitioners, seminal works, core consensus, major disagreements, comparison tables, or an entry learning roadmap.
---

# Map Domain Experts

## Overview

Use this skill to turn "I want to quickly learn X" into a compact expert map: who matters, what they agree on, where they disagree, and how to start learning. Optimize for accuracy, intellectual structure, and traceable evidence rather than a generic reading list.

Default to answering in the user's language.

## Workflow

### 1. Scope the Field

If the user leaves the field as a placeholder, e.g. `【领域名称】`, ask for the field. If the field is broad, proceed with a clear scope assumption unless that would make the answer misleading.

State the interpreted scope in 1-2 sentences before the main answer:

- domain boundary, such as subfield, time period, region, or applied vs academic angle
- whether "expert" includes scholars, builders, operators, critics, or public intellectuals

### 2. Build an Evidence Base

For current, niche, contested, or high-stakes domains, verify with browsing or available primary sources. Prefer:

- seminal papers/books and publisher pages
- university, lab, institutional, or official biography pages
- citation indexes, conference keynotes, standards bodies, widely adopted tools/frameworks
- reputable interviews, lectures, debates, or essays when they clarify a living practitioner's view

Do not fabricate expertise, works, citations, or consensus. If evidence is thin, say so and reduce confidence.

### 3. Select 5-10 Representative People

Choose people who collectively explain the field, not merely the most famous names. Balance:

- founders/seminal theorists
- method builders or empirical researchers
- practitioners who changed real-world practice
- critics or alternative schools that reveal fault lines
- current voices if the field is active and changing

For each person, capture why they matter in one concrete sentence: concept introduced, method created, institution shaped, tool built, policy changed, or debate reframed.

### 4. Extract Consensus and Disagreement

Core consensus must be a small set of propositions that most selected experts would recognize, even if they phrase them differently. Tie each consensus point to multiple experts.

Disagreements should be axes, not trivia. Look for:

- theory: what explains the phenomenon?
- method: what counts as valid evidence or good practice?
- values: what outcomes should be optimized, protected, or avoided?
- scope: where does the theory/method stop working?
- strategy: what should beginners, organizations, or policymakers do first?

For each disagreement, name the sides, the stakes, and a concrete example of how the disagreement changes action.

## Output Format

Use this structure unless the user asks for another format:

1. `范围说明`: State the scope assumption.
2. `代表人物`: List 5-10 experts with 1-2 sentences each on why they matter.
3. `核心共识`: Summarize 3-6 shared claims.
4. `关键分歧`: Summarize the most important disagreements by axis.
5. `对照表`: Include columns:
   `专家 | 代表作品/论文/观点 | 核心主张 | 与其他人的分歧`
6. `入门学习路线`: Give a staged path:
   `先读/先看` -> `再读/再看` -> `对照阅读` -> `继续追踪的问题`
7. `资料来源`: Include concise citations or links when sources were used.

## Quality Bar

The result should feel like a map of the field's intellectual terrain. Avoid flat encyclopedia summaries. Make tradeoffs visible: why these people, why these disagreements, and why this learning order.
