# NovelCraft Module Template: Writer Extras

## Task for Subagent

Write optional prolog and/or epilog for the book.

**STEP 1: Load Configuration**
Read these files:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-writer-extras.md`
3. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/00-concept/concept.md`

**STEP 2: Check if Enabled**
In project-manifest.md, check if prolog/epilog is enabled.

**STEP 3: Create Output Files**
Save to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/`

| File | When | Content |
|------|------|---------|
| prolog.md | Before chapter 1 | Hook reader, establish mystery |
| epilog.md | After last chapter | Closure, character fates |

**STEP 4: Validation Rules**
- 1500-3000 words each
- UTF-8 encoding
- No foreign characters
- Connects to main narrative

**STEP 5: Report**
Confirm which files were written.
