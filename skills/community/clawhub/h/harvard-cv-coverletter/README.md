# Harvard CV & Cover Letter Skill

A Claude skill that produces professional, Harvard-standard CVs (resumes) and cover letters as `.docx` files, following the official **Harvard Office of Career Services (OCS)** guidelines.

---

## What It Does

- Guides you through a structured intake process to collect your information
- Produces a polished `.docx` resume in **bullet format** or **paragraph format**
- Produces a **cover letter** as a separate `.docx` file
- Enforces Harvard OCS formatting rules exactly: section ordering, action-verb language, reverse-chronological structure, two-column tab-stop layout, proper bullet rendering
- Includes the full Harvard action verb bank (Leadership, Communication, Research, Technical, Teaching, Quantitative, Creative, Helping, Organizational)

---

## What It Will Never Do

This skill is hardcoded to **never hallucinate, infer, or invent** any information about you — not your job titles, dates, responsibilities, achievements, skills, or anything else. It works exclusively from what you tell it. If something is missing, it asks.

---

## Trigger Phrases

Install this skill and Claude will activate it when you say things like:

- "Write my resume"
- "Help me with my CV"
- "Draft a cover letter for this job"
- "Update my resume"
- "I'm applying for a job and need a cover letter"
- "Create a professional resume from my background"

---

## File Structure

```
harvard-cv-coverletter/
├── SKILL.md                        # Main skill engine
└── references/
    └── harvard-rules.md            # Full Harvard OCS ruleset + action verb banks
```

---

## Requirements

This skill depends on:

- **`docx` npm package** — installed automatically via `npm install -g docx`
- **`docx` public skill** — must be available at `/mnt/skills/public/docx/SKILL.md` in your Claude environment

---

## Resume Formats Supported

| Format | Description |
|--------|-------------|
| **Bullet** (default) | Each experience entry uses bullet points starting with action verbs |
| **Paragraph** | Each experience entry is written as a short action-verb-led paragraph |

Both formats follow the same Harvard layout and language rules.

---

## Harvard OCS Rules Enforced

**Language:**
- Specific, active, fact-based
- No personal pronouns (I, We, My)
- No narrative style, no slang, no flowery language
- Every bullet/sentence starts with an action verb

**Structure:**
- Reverse chronological order within each section
- Sections ordered by relevance to target role
- No photos, age, gender, or references included

**Cover Letter:**
- Maximum one page
- Addressed to a specific person
- Three-paragraph structure: opening → relevant experience → closing
- Same font as resume
- References the job description explicitly

---

## Output

Both documents are delivered as `.docx` files ready to submit or convert to PDF.

---

## Source

Based on the official [Harvard Office of Career Services Resume & Cover Letter Guide](https://ocs.fas.harvard.edu).

---

## License

Free to use and adapt. Attribution appreciated.
