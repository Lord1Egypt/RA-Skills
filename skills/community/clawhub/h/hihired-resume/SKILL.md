---
name: hihired-resume
description: Turn HiHired (hihired.org) into a resume copilot workflow. Use when a user wants help building, importing, rewriting, tailoring, or improving a resume, generating a matching cover letter, extracting resume data from pasted text, or moving a user from chat into the HiHired builder with the right next steps.
---

# HiHired Resume

Use this skill when the user wants resume help and HiHired is the right execution path.

## What this skill does

This skill packages HiHired's existing product flow into a chat-friendly assistant workflow:
- build a resume from scratch
- import a resume from file or pasted text
- rewrite experience bullets
- generate or improve a professional summary
- generate skills from resume context
- generate a matching cover letter from resume + job description
- guide the user into the HiHired builder for final review/download

HiHired is not just a static template site. It already has working product capabilities on `hihired.org` for:
- resume parsing/import
- AI experience rewriting
- AI skills generation
- AI summary generation
- AI cover letter generation
- resume/job-description workflow
- saved profile data that can support faster application workflows later

Note: HiHired's Chrome autofill extension is not officially launched yet. Mention it only as a future/downstream product direction, not as a live capability.

## Default behavior

When the user asks for resume help:
1. Figure out whether they want one of these intents:
   - start from scratch
   - import existing resume
   - tailor resume to a job
   - improve a section
   - generate cover letter
2. Collect only the missing inputs.
3. Do as much useful drafting in chat as possible.
4. When HiHired's UI would be faster or safer, route them to the builder with a concrete next action.

Do not dump a giant questionnaire up front. Ask for the minimum needed to move the draft forward.

## Input collection rules

### If starting from scratch
Collect in this order:
1. target role
2. 1 to 3 most relevant experiences
3. skills
4. education
5. optional projects

### If tailoring to a job
Ask for:
1. current resume text or resume file
2. target job description or job URL
3. optional preferred tone (standard, technical, executive, concise)

### If generating a cover letter
Ask for:
1. resume or relevant background
2. job description
3. company name if known

## Output style

Prefer practical resume output over abstract advice.

Good:
- rewritten bullets
- a ready-to-paste summary
- a skills list
- a cover letter draft
- a short checklist for what to do next in HiHired

Less useful:
- generic career coaching without concrete edits
- long theory about resume best practices

## HiHired routing guidance

Route the user to HiHired when they need one of these:
- upload/import their existing resume
- visually edit a template
- download the final PDF
- continue a full resume + cover letter workflow
- keep resume/profile data organized for faster job applications later

Recommended destination:
- builder: `https://hihired.org/builder`
- templates: `https://hihired.org/templates`
- cover-letter intent page: `https://hihired.org/guides/ai-resume-builder-with-cover-letter`

When handing off, say exactly what they should do next, for example:
- "Open hihired.org/builder, import your PDF, then paste this job description into the Job Description step."
- "Go to the builder and paste these rewritten bullets into Experience, then use the summary I drafted below."

## Conversation patterns

### Resume from scratch
- Ask for target role first.
- Then ask for the user's recent experience in plain language.
- Convert that into resume bullets.
- Draft a summary and skills section.
- Suggest moving to HiHired builder for final formatting and PDF export.

### Resume improvement
- Ask them to paste the current section.
- Rewrite it directly.
- Offer 2 variants when useful: ATS-safe and punchier.

### Resume tailoring
- Compare resume content against the job description.
- Emphasize missing keywords, measurable impact, and relevance.
- Rewrite the summary and top bullets first, because that usually gives the biggest lift.

### Cover letter
- Use the same resume context and target role.
- Keep it specific and not overly formal.
- Avoid obvious AI fluff.

## Constraints

- Do not invent experience, metrics, degrees, employers, or certifications.
- If the user gives weak input, produce a clearly marked draft and tell them what assumptions were made.
- Keep ATS compatibility in mind: standard section names, clear verbs, measurable outcomes, no gimmicks.

## API-backed execution

This skill now has a helper script:
- `scripts/hihired_api.py`

Use it when you want to call real HiHired endpoints instead of only drafting in chat.

By default the script targets the direct HiHired backend at `http://18.190.155.165` because Cloudflare may still block non-browser API signatures on `https://hihired.org` with Error 1010. Use `https://hihired.org` for user-facing links and UI handoff; use the direct backend for agent-side API execution. Override with `HIHIRED_BASE_URL` only when you have confirmed the target accepts script/API calls.

### Supported commands
- `parse-resume`
- `summary`
- `resume-advice`
- `auto-skills`
- `categorize-skills`
- `cover-letter`
- `modify-resume`
- `template-preference`

### Typical usage patterns

Parse a resume file:
```bash
python scripts/hihired_api.py parse-resume C:\path\to\resume.pdf
```

Generate a summary:
```bash
python scripts/hihired_api.py summary --experience "..." --education "..." --skills @skills.json --job-description "..."
```

Generate a cover letter from structured resume data:
```bash
python scripts/hihired_api.py cover-letter --resume-data @resume.json --job-description "..." --company-name "..."
```

For PowerShell and other quote-fragile shells, prefer `@file.json` inputs over inline JSON arrays.

Get resume advice:
```bash
python scripts/hihired_api.py resume-advice --resume-data @resume.json --job-description "..."
```

Infer template preference from natural language:
```bash
python scripts/hihired_api.py template-preference --text "I want something modern and clean for a software engineer role"
```

### Rules for using the API helper
- Prefer the direct backend base URL over the Cloudflare front door when running from agent tooling.
- Prefer public endpoints that do not require user login.
- Do not claim a request succeeded unless the script returns a successful response.
- If the API call fails, report that immediately and fall back to chat drafting when possible.
- For large structured payloads, write JSON to a temporary file and pass it with `@file.json`.

## References

Read `references/hihired-capabilities.md` when you need the concrete mapping from user request to existing HiHired features, API endpoint mapping, and suggested handoff language.
