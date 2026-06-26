# NovelCraft Module Template: Publication

## Task for Subagent

Create final PDF and EPUB from completed chapters.

**STEP 1: Load Configuration**
Read these files:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-publication.md`

**STEP 2: Prepare Input**
Source files (approved chapters): `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/02-chapters/chapter_*.md`
Images: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/images/`

**Note:** Only use approved chapters from 02-chapters/. Drafts in 01-drafts/ are work-in-progress.

**STEP 3: Build**
| Format | Tool | Output |
|--------|------|--------|
| PDF | xelatex | die-feuer-von-ashara.pdf |
| EPUB | pandoc | die-feuer-von-ashara.epub |

**STEP 4: Layout Settings**
- Font: Latin Modern Roman
- Size: 12pt
- Line height: 1.6
- Margins: 2cm
- Include cover image
- Include table of contents

**STEP 5: Save**
Output: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/03-final/`

**STEP 6: Validation**
- Files exist and are readable
- PDF < 50MB
- EPUB validates

**STEP 7: Report**
Confirm: file sizes, location, any issues.
