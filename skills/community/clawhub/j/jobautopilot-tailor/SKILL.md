---
name: jobautopilot-tailor
description: Tailors your resume and cover letter to a specific job description. Fetches the JD, rewrites bullet points to match keywords, and exports polished .docx files — 100% based on your real experience, nothing invented. Picks up shortlisted jobs from jobautopilot-search and hands resume_ready entries to jobautopilot-submitter.
author: jerronl
version: "1.3.0"
homepage: https://github.com/jerronl/jobautopilot
tags:
  - resume
  - cover-letter
  - docx
  - job-search
  - career
requires:
  tools:
    - web_search
    - browser
  python_packages:
    - python-docx
    - lxml
  env:
    - RESUME_DIR
    - RESUME_OUTPUT_DIR
    - RESUME_TEMPLATE
    - MD_TO_DOCX_SCRIPT
    - JOB_SEARCH_TRACKER
    - USER_FIRST_NAME
    - USER_LAST_NAME
    - USER_EMAIL
    - USER_PHONE
    - USER_LINKEDIN
  bins:
    - python3
metadata:
  clawdbot:
    emoji: "📄"
    requires:
      env:
        - RESUME_DIR
        - RESUME_OUTPUT_DIR
        - RESUME_TEMPLATE
        - MD_TO_DOCX_SCRIPT
        - JOB_SEARCH_TRACKER
        - USER_FIRST_NAME
        - USER_LAST_NAME
        - USER_EMAIL
        - USER_PHONE
        - USER_LINKEDIN
      bins:
        - python3
      pip:
        - python-docx
        - lxml
    files:
      - scripts/md_to_docx.py
---

# Job Autopilot — Resume Tailor

Produces a tailored resume and cover letter for each `shortlist` job in the tracker. Delivers `.docx` files ready to attach and send.

## Core principles

1. **100% truthful** — never invent experience, inflate metrics, or fabricate credentials.
2. **Resume content comes from the user's original files first** — always read `$RESUME_DIR` before writing anything.
3. **md before docx** — complete markdown drafts for ALL shortlisted jobs first, then convert to docx in batch. Do not interleave md writing and docx conversion.
4. **One job at a time for reporting** — finish and report each job's result before moving to the next.
5. **No silent spinning** — if a job cannot be reliably completed within 30 minutes, mark it `error` with a clear reason and move on.

## Setup

Add to `~/.openclaw/workspace/job_search/config.sh`:

```bash
export RESUME_DIR="$HOME/Documents/jobs/"           # your original resume files live here
export RESUME_OUTPUT_DIR="$HOME/Documents/jobs/tailored/"  # where tailored files are saved
export RESUME_TEMPLATE="$HOME/.openclaw/workspace/job_sub_agent/scripts/sample_placeholders.docx"
# Download template: https://github.com/jerronl/jobautopilot/raw/main/jobautopilot-tailor/scripts/sample_placeholders.docx
export MD_TO_DOCX_SCRIPT="$HOME/.openclaw/workspace/job_sub_agent/scripts/md_to_docx.py"
export JOB_SEARCH_TRACKER="$HOME/.openclaw/workspace/job_search/job_application_tracker.md"
export USER_FIRST_NAME="Your"
export USER_LAST_NAME="Name"
export USER_EMAIL="your@email.com"
export USER_PHONE="+1-555-000-0000"
export USER_LINKEDIN="https://linkedin.com/in/yourprofile"
mkdir -p "$RESUME_OUTPUT_DIR"
```

## Session start

Read in order:
1. `$RESUME_DIR` — understand the user's full experience and skills
2. `$JOB_SEARCH_TRACKER` — find all `shortlist` entries to process

## JD fetch order

For each shortlist job:
1. Use the exact URL from the tracker
2. Try `web_search` first to extract job responsibilities, skills, keywords, asset classes
3. If `web_search` returns no useful JD, use browser to open the URL directly
4. If the URL is broken, a generic careers page, or wrong role → mark tracker `error` and explain why

## Content production order

For each job, strictly in this sequence:

### Step 1 — Read source material

Read all files in `$RESUME_DIR`. The pool may contain:

| File type | What to extract |
|-----------|----------------|
| Master resume (`.docx` / `.pdf`) | Full work history, bullet points, metrics, dates. PDF text is extracted by the agent's built-in tools; the conversion script handles `.docx` and `.md` only. |
| Older tailored versions | Phrasing that worked well for similar roles |
| Cover letter drafts | Preferred voice, opening formulas, recurring themes |
| Skills list / bio (`.md` / `.txt`) | Certifications, tools, side projects, publications |

Extract everything factual — every bullet, every metric, every tool name. This is your raw material. **Do not invent anything not present in these files.**

### Resume markdown format specification

The markdown file must follow this exact format. `md_to_docx.py` parses it structurally — any deviation will produce wrong or missing output.

```markdown
Full Name
Email | Phone | LinkedIn | Location

SUMMARY
Two to three sentences summarizing the candidate.

CORE SKILLS
List of skills, tools, and technologies relevant to this role.

EXPERIENCE
Job Title — Company Name | City, ST | Jan 2022 – Present
• Accomplished X by doing Y, resulting in Z
• Another bullet point with a metric

Job Title — Company Name | City, ST | Jun 2019 – Dec 2021
• Bullet point
• Bullet point

EARLIER EXPERIENCE
Earlier Role — Company, Year–Year
Another Earlier Role — Company, Year–Year

EDUCATION
University Name — Degree, Major (Year)
```

**Parsing rules the script enforces — follow these exactly:**

| Element | Rule |
|---------|------|
| Line 1 | Full name, plain text, no `#` heading marker |
| Line 2 | Contact info, pipe-separated |
| Section headers | ALL CAPS, no `##` — exactly `SUMMARY`, `CORE SKILLS`, `EXPERIENCE`, `EARLIER EXPERIENCE`, `EDUCATION` |
| Job header | `Title — Company \| Location \| Date range` — separator is ` — ` (em dash with spaces), fields separated by ` \| ` |
| Bullets | Start with `•` or `-`, one per line |
| Earlier experience | One line per entry: `Role — Company, Years` |
| Education | One line per entry: `University — Degree` |

**What the script handles automatically:**
- More jobs than template slots → clones the last job's formatting
- Fewer jobs than template slots → removes unused placeholders
- Same logic for bullets, earlier experience, and education entries

### Step 2 — Write resume markdown
Tailor bullet points to match the JD keywords. Prioritize:
- Skills explicitly mentioned in JD
- Quantified achievements relevant to the role
- Asset classes, systems, or methodologies named in JD

Save to: `$RESUME_OUTPUT_DIR/${USER_FIRST_NAME}_<Company>_<Title>_Resume_2026.md`

### Self-check before converting to docx

Before running `md_to_docx.py`, verify the markdown against these rules:

```bash
# Line 1 must be plain name (no # prefix)
head -1 resume.md

# Line 2 must contain pipes (contact info)
sed -n '2p' resume.md | grep '|'

# Section headers must be ALL CAPS with no ## prefix
grep -E '^[A-Z ]+$' resume.md

# Job headers must match: Title — Company | Location | Date
grep -E '^.+ — .+ \| .+ \| .+$' resume.md

# Bullets must start with • or -
grep -E '^[•\-]' resume.md
```

If any check fails, fix the markdown before proceeding — a malformed file will silently produce an incomplete docx.

### Step 3 — Write cover letter markdown
Three paragraphs max:
1. Why this role + company
2. Most relevant experience match (2–3 specific points)
3. Brief close

Save to: `$RESUME_OUTPUT_DIR/${USER_FIRST_NAME}_<Company>_<Title>_Cover_Letter_2026.md`

### Step 4 — Update tracker
Change status to `md_ready`. Record md file paths.

### Step 5 — Generate docx files

**Resume** — use `md_to_docx.py` with the template:
```bash
python3 "$MD_TO_DOCX_SCRIPT" \
  --input "$RESUME_OUTPUT_DIR/${USER_FIRST_NAME}_<Company>_<Title>_Resume_2026.md" \
  --template "$RESUME_TEMPLATE" \
  --output "$RESUME_OUTPUT_DIR/${USER_FIRST_NAME}_<Company>_<Title>_Resume_2026.docx"
```

**Cover letter** — use python-docx directly (plain text, no template):
```python
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# Add paragraphs from cover letter md content
for para in cover_letter_paragraphs:
    p = doc.add_paragraph(para)

doc.save(f"{output_dir}/{os.environ['USER_FIRST_NAME']}_<Company>_<Title>_Cover_Letter_2026.docx")
```

### Step 6 — Verify docx

**"Text looks right" is not the same as "file is deliverable."** Both conditions must pass:

1. **Content check** — open the docx and compare section by section against the md:
   - No missing sections
   - No leftover `{{PLACEHOLDER}}` strings anywhere in the document
   - Company name and job title are correct throughout
2. **File check** — the docx must open without errors, have non-zero file size, and be saved to `$RESUME_OUTPUT_DIR`
3. **URL check** — validate the job URL from the tracker is still reachable

Do not call partial verification "good enough." If any check fails, fix and re-verify before updating the tracker.

### Step 7 — Update tracker
- Success → `resume_ready`, record docx paths
- Cannot reliably complete → `error`, write reason

### Step 8 — Report
After each job, report: company, title, files produced, any issues.

## File naming convention

```
${USER_FIRST_NAME}_<CompanyName>_<JobTitle>_Resume_2026.docx
${USER_FIRST_NAME}_<CompanyName>_<JobTitle>_Cover_Letter_2026.docx
```

Spaces → underscores. Keep company and title short (≤ 20 chars each if possible).

## Tracker status flow

```
shortlist → md_ready → resume_ready
                    ↘ error
```

## Known failure modes to avoid

- Do not call partial verification "good enough"
- Do not treat "text looks right" as equivalent to "docx is deliverable"
- Do not spend more than 30 minutes on a single job without reporting status
- Do not write a generic script to handle all cases; get the md layer working first

## Scope

Resume tailoring only. Do not submit applications. Hand off `resume_ready` entries to the `jobautopilot-submitter` skill.

## Support

If Job Autopilot saved you time: paypal.me/ZLiu308
