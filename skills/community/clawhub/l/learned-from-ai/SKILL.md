---
name: learned-from-ai
description: Turn chat interactions with AI into durable learning materials for humans. Use when the user provides a chat/share link, pasted AI conversation, or rough AI-generated draft and wants it converted into structured, long-lived notes for review and memory. Especially use when the user wants the fixed structure: (1) definition, (2) essential ideas or engineering practice, (3) worked examples and calculations, (4) important derivations, (5) Q&A, (6) further reading/viewing, plus a separate cheat sheet. For tasks under this skill, always use a subagent with model openai-codex/gpt-5.4 and thinking medium by default so the main session stays responsive, unless the user explicitly asks otherwise. Always save outputs in notes/ unless the user explicitly asks otherwise.
---

# learned-from-ai

Turn transient AI chat output into **structured, reviewed, long-lived learning material** that is easy for a human to study, remember, and revisit.

## Non-negotiable rules

1. **Always handle tasks under this skill through a subagent by default** so the main session does not get blocked, unless the user explicitly asks otherwise.
2. **Use the preferred subagent settings by default:** `runtime: subagent`, `model: openai-codex/gpt-5.4`, `thinking: medium`.
3. **Always save outputs in `notes/`** unless the user explicitly asks for a different location.
4. **Always keep the original shared/source link in the main summary note** when a link exists, so the source can be traced easily.
5. **Before writing, search the `notes/` folder for existing related notes** by subject/project so you do not overwrite durable knowledge accidentally.
6. **For boundary cases on the same project/topic, do not rewrite the existing note by default.** Create a new summary and cheat sheet instead.
7. **Name new boundary-case files intelligently**: use either a more specific sub-subject name or the existing knowledge name plus an incremented suffix.
8. **Always generate a cheat sheet** based on the reviewed main note.
9. **Do not violate the preferred structure** unless the user explicitly asks for a different one.
10. **Strongly remove AI slop, repetition, weak filler, and hallucinated claims.**
11. **Cross-check questionable facts, formulas, standards, and numbers when needed.**
12. **Keep the main note and cheat sheet separate.**

---

## Preferred structure

Use this exact structure unless the user explicitly overrides it:

1. **Definition**
2. **Essential ideas / engineering practice**
3. **Worked examples and calculations**
4. **Important theoretical derivations**
5. **Q&A from the discussion**
6. **Further reading / viewing**

Always create a separate cheat sheet file based on the reviewed main note.

---

## Workflow

1. **Start by spawning the working subagent**
   - For tasks under this skill, start with a subagent by default so the main session stays responsive.
   - When this skill is activated with a slash command and the user appends a chat/share link, immediately spawn the subagent.
   - Use the default settings unless the user explicitly overrides them:
     - `runtime: subagent`
     - `model: openai-codex/gpt-5.4`
     - `thinking: medium`
   - Give the subagent the link or source material and the required output structure.

2. **Inspect the source**
   - Read the shared link, pasted chat, file, or notes.
   - Extract the real technical content.
   - Ignore UI noise, fluff, and repeated AI phrasing.

3. **Pre-search the knowledge base in `notes/`**
   - Before naming or writing files, inspect existing note filenames in `notes/` for the same subject, project, or nearby topic.
   - Use this step to avoid overwriting durable notes.
   - If the new source is clearly a new subtopic or a separate chat on the same project, plan a new note instead of rewriting the old one.

4. **Identify the subject and output files**
   - Pick a short subject-based filename.
   - By default, write a new note rather than overwriting an existing one when the source is a new chat, new link, or new subtopic.
   - Write the main note to `notes/<subject>.md`.
   - Always write the cheat sheet to `notes/<subject>-cheatsheet.md`.
   - If needed, use either:
     - a more specific sub-subject name, or
     - the existing knowledge name plus an incremented suffix.
   - If the source came from a shared/public link, record that original link near the top of the main note so the summary can be traced back to its source easily.

5. **Review and verify before polishing**
   - During review, use strong reasoning and factual discipline.
   - Catch factual errors.
   - Remove hallucinations.
   - Strip AI slop.
   - Cross-check formulas, standards, fit values, and calculations when needed.
   - Distinguish exact statements from approximations.
   - Preserve useful approximations, but label them honestly as approximations, first-pass checks, or worst-case bounds.

6. **Write the main note**
   - Follow the preferred structure exactly.
   - Do **not** reorder or silently replace it with a different teaching flow.
   - Make definitions crisp, logic coherent, and examples numerically consistent.
   - The preferred structure must not be violated.
   - Do not overwrite an existing durable note unless the user explicitly asks for revision of that specific file.

7. **Write the cheat sheet**
   - Base it on the reviewed main note.
   - Keep it separate from the main note.
   - Distill, do not duplicate.
   - The preferred main-note structure must still remain intact and must not be violated.

8. **Finalize and organize**
   - Ensure files are in `notes/`.
   - Use short, practical names.
   - Avoid redundant filenames like `-study-note` unless the user explicitly wants them.

---

## Writing standards

### Keep
- precise definitions
- practical engineering or domain logic
- worked numerical examples
- short derivations that reveal the principle
- explicit assumptions and limitations
- Q&A clearly separated from exposition

### Remove
- AI filler
- repetitive hype
- vague certainty
- unsupported claims
- long padding that does not improve learning

### Prefer
- short sections
- bullets over bloated prose
- equations when they clarify reasoning
- ASCII sketches when a simple drawing helps
- concise filenames

---

## Review checklist

Before finishing, check:

- Are the files in `notes/`?
- Does the main note keep the original shared/source link when one exists?
- Does the main note follow the preferred structure exactly?
- Is the cheat sheet separate and genuinely distilled?
- Were suspicious claims cross-checked?
- Were hallucinations and AI slop removed?
- Are examples and calculations internally consistent?
- Are approximations labeled clearly?
- Are filenames short and subject-based?

---

## Example file layout

```text
notes/
  gdt.md
  gdt-cheatsheet.md
```

---

## Scope

This skill is for turning **AI chat interactions into durable human learning materials**.

It is not mainly for:
- writing full textbooks from scratch
- doing exhaustive literature reviews
- dumping raw chat transcripts into files without review

If the source is rough, correct it. If it is verbose, compress it. If it is uncertain, verify it.