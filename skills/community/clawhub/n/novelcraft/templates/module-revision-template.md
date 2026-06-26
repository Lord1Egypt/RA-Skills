# NovelCraft Module Template: Revision

## Task for Subagent

Revise ONE chapter based on review feedback.

**STEP 1: Load Configuration**
Read these files:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-chapters.md`
3. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/00-concept/concept.md`

**STEP 2: Read Current Chapter (Draft)**
Read: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{CHAPTER_NUMBER}_draft.md`

**STEP 3: Read Review**
Read: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{CHAPTER_NUMBER}_review.md`

**STEP 4: Apply Required Changes**
Follow the "Required Changes" section from the review EXACTLY:

- **MINOR_REVISION (Score 6.0-7.9):** Fix specific issues listed, keep majority of content
- **MAJOR_REVISION (Score 4.0-5.9):** Significant rewrite of marked sections
- **REJECTED (Score 0.0-3.9):** Complete rewrite (treat as new chapter)

**Rules for Revision:**
- Preserve what the review marked as "Strengths"
- Address every item in "Required Changes"
- Maintain UTF-8 encoding (no foreign characters)
- Keep word count within 7000-8000
- Maintain continuity with previous/next chapters

**STEP 5: Save Revised Draft**
Save updated version to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{CHAPTER_NUMBER}_draft.md`

**STEP 6: Increment Revision Counter**
Update revision count in project manifest or chapter metadata.

**STEP 7: Report**
Confirm:
- Changes applied per review
- Word count after revision
- Encoding check passed
- Ready for re-review

**STEP 8: Automatic Decision**
- If this is revision #3 and still not approved → Request complete rewrite
- Otherwise → Schedule re-review
