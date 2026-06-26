---
name: multi-unit-test-report
description: Generate structured markdown test reports for online English classes covering multiple units. Use when the user needs to create a student test report for review units that cover multiple previous units (e.g., Unit 4 reviewing Units 1-3). Triggers on phrases like "multi unit report", "review unit report", "generate report for review unit", or when reviewing student performance across multiple units.
---

# Multi Unit Test Report

## Mission Statement

Before generating any report, read the mission statement from the Obsidian vault:

```
/Users/recom273/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidianclaw/projects/system/openclaw/skills/mission statement multi unit test report.md
```

This file contains the canonical report format, workflow, and improvement suggestions. Always follow the mission statement's guidance for tone and structure.

## Workflow

1. **Read the opening slide** — Check the top left for the level (e.g., PF3, PF5, PF7) and unit number. This is a review unit covering multiple previous units.
2. **Read all summary slides** — These are typically the last slides in the folder. Extract information from each unit reviewed.
3. **Ask about student performance** — Ask the user: "Is there anything the student has performed well in?" Incorporate this into the opening praise.
4. **Create an opening sentence** praising the student using suggested topics and specific performance notes.
5. **Detail the material covered** from each unit, section by section.
6. **Add the standard points to improve** — randomly select 3 from the approved list.

## Report Structure

Each report follows this exact format (correct typos from the mission statement):

```markdown
[Opening praise sentence]
# [Student Name]

Todays test covered material from, [unit number]

We featured

**Vocabulary** — [vocabulary topic from all units]

**Grammar** — We learned how to [grammar point from all units][Performance notes]

**Phonics** — We studied the sound [phonic details from all units][Performance notes]

**Around the world** — In this lesson [lesson summary from all units][Performance notes]

**Story** — We read a story about [story synopsis from all units][Performance notes]

**Song** - We ended by singing a song about [song synopsis from all units][Performance notes]

**Life Science** — We learned [science point from relevant units][Performance notes]

**Social Science** — We learned [social science point from relevant units][Performance notes]

**Social Values** — We learned [value point from relevant units][Performance notes]

## Areas for Improvement

It's hard to suggest ways for a student to improve who has just achieved a full score. [select three random points of improvement]

[point 1]
[point 2]
[point 3]
```

## Key Differences from Single Unit Report

- **Multiple units covered** — The report summarizes content from 2-3 previous units
- **Review unit format** — Opening slide shows "Unit X (Unit Y - Unit Z Review)"
- **Summary slides** — Read ALL summary slides at the end (one per unit reviewed)
- **Combined content** — Group similar sections across units (e.g., all vocabulary together, all grammar together)

## Ways to Improve

Randomly select 3 points from this list:

| Points |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Its good practice for the future if you read the full sentences including the answer, often in English if the sentence sounds correct then it is correct. |
| Always read the full sentences aloud. Reading aloud is a good way of identifying any mistakes that you may have made. |
| Keep practicing! Practice makes perfect. |
| Speak up! Try to use the freetalk at the beginning of the lesson to expand your conversational ability. |
| Always review the previous lessons before the final test, this will help you guarantee a 💯 100% score next time. |
| Try to use full sentences during the lesson, not just one-word answers. |
| Listen carefully to the questions and make sure you understand before answering. |
| Don't be afraid to make mistakes - that's how we learn! Keep trying. |

## Output Location

Save reports to the folder provided by the user. Default to workspace if no location specified.
