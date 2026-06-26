# NovelCraft Module Template: Chapters

## Task for Subagent

Write ONE chapter for the book. NEVER write multiple chapters in parallel.

**STEP 1: Load Configuration**
Read these files BEFORE writing:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-chapters.md`
3. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/00-concept/concept.md`

**STEP 2: Read Previous Chapter (if exists)**
If this is chapter X > 1, read chapter_{X-1}_final.md first for continuity.

**STEP 3: Write Chapter**
- Chapter: {CHAPTER_NUMBER} - "{CHAPTER_TITLE}"
- Words: 7000-8000
- Style: Dense atmosphere, character-driven, dark-hopeful
- Encoding: UTF-8 ONLY
- Language: German

**STEP 4: CRITICAL - Validate Encoding**
Before saving, check:
- No Chinese/Arabic/Japanese characters
- Only valid: a-z, A-Z, äöüßÄÖÜ, 0-9, punctuation, whitespace
- Test: `cat -v` should show no `M-` prefixes

**STEP 5: Save**
**Save Draft:**
Save to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{XX}_draft.md`

**After APPROVAL - Move to Final:**
Copy approved chapter to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/02-chapters/chapter_{XX}.md`

**STEP 6: Request Review**
After saving, this chapter MUST be reviewed before the next chapter can be written.

The review will check:
- Encoding UTF-8 (Critical)
- Word count 7000-8000 (High)
- Continuity with previous chapter (High)
- Character voice and style (Medium)
- Plot progression (High)

**DO NOT proceed to next chapter until review is complete.**

**STEP 7: Report**
Confirm: chapter number, title, word count, encoding check passed, and note that review is pending.
