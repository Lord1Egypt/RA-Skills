# Novel Writer Skill

OpenClaw skill for planning, drafting, continuing, and revising long-form fiction.

## What It Does

- Helps the user choose a novel topic or refine an existing idea.
- Builds a reusable novel bible before long-form drafting.
- Creates chapter outlines and writes chapter-by-chapter prose.
- Tracks continuity across characters, timeline, world rules, clues, foreshadowing, and unresolved threads.
- Supports continuation and revision without breaking established facts.

## Files

- `skill.yaml`: OpenClaw metadata, trigger keywords, and prompt file pointer.
- `SKILL.md`: Main agent instructions and writing workflow.
- `references/templates.md`: Reusable templates for topic menus, novel bibles, chapter plans, and continuity updates.

## Usage

Place this folder where OpenClaw loads skills, or keep it under a workspace `skills/` directory:

```text
skills/
  novel-writer-1.0.0/
    skill.yaml
    SKILL.md
    references/
      templates.md
```

Example prompts:

```text
帮我用 novel-writer 写一部长篇小说，先让我选题。
```

```text
我要写一部科幻长篇，请先做小说设定总纲和章节大纲。
```

```text
根据前面的设定，继续写第 3 章，并更新连续性台账。
```

