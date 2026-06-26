# HiHired capabilities reference

Use this file when you need concrete product-grounded behavior instead of guessing.

## Existing HiHired capabilities confirmed from code

## Public endpoint mapping

These endpoints are publicly callable from the site code and are the safest first targets for this skill:

- `/api/resume/parse` — upload resume file and get structured data
- `/api/ai/summary` — generate or improve summary from experience/education/skills/job description
- `/api/resume/analyze-advice` — get overall resume advice
- `/api/cover-letter/generate` — generate cover letter from structured resume data + job description
- `/api/skills/auto-generate` — derive skills from structured resume context
- `/api/skills/categorize` — bucket skills into recruiter-friendly groups
- `/api/assistant/resume/modify` — interpret natural-language edit requests against existing resume data
- `/api/template/preference` — infer template + font preference from natural language

Protected endpoints like job matches, resume history, and app tracking require auth and should not be assumed available unless the user is authenticated in that specific flow.

## Direct backend note

For agent-side API calls, prefer the direct backend `http://18.190.155.165`. As of 2026-05-04, `robots.txt` allows AI crawlers on `https://hihired.org`, but direct script/API calls to the Cloudflare-fronted `/api/...` endpoints can still return Error 1010 (`browser_signature_banned`). Use `https://hihired.org` for user-facing handoff links and crawler-visible content; use the direct backend for helper execution.

### Resume import
- Users can import from a resume file.
- Users can also paste resume text.
- The front-end calls `/api/resume/parse` to extract structured resume data.
- Resume history import exists for returning users.

## AI resume helpers

### Experience rewriting
- HiHired has AI rewriting for experience bullets.
- Use this when the user says things like:
  - "make these bullets stronger"
  - "rewrite my experience"
  - "tailor this to the job"

### Skills generation
- HiHired can generate skills from existing resume data.
- It can also categorize skills for display.
- Good for users who have experience text but no clean skills list.

### Summary generation
- HiHired can generate or improve a professional summary.
- If the user has no summary, generate one from experience + education + skills + target job.
- If the user already has a summary, improve clarity and grammar.

### Cover letter generation
- HiHired can generate a cover letter from:
  - resume data
  - job description
  - company name
- Use this when the user wants a matching cover letter instead of a generic one.

### Voice input
- HiHired supports voice transcription in its chat widget.
- This matters mainly as a product note if the user prefers speaking their background instead of typing.

## Chat-side resume workflow to emulate

The product itself already nudges users through a sequence similar to:
1. import choice
2. template
3. personal details
4. job description
5. experience
6. projects
7. education
8. skills
9. summary

In chat, do not force that exact UI sequence rigidly.
Use it as a mental model for collecting missing information.

## Good handoff language

### If the user has a PDF resume
"Open https://hihired.org/builder and use Import Resume. After it parses, I can help you rewrite the strongest bullets or tailor the summary to a target role."

### If the user wants a better template
"Start at https://hihired.org/templates, pick the template you like, then continue into the builder. I can help you rewrite the content before you export."

### If the user wants a cover letter
"Once your resume details and target job are in the builder, HiHired can generate a matching cover letter from the same context."

### If the user wants job-application workflow
"HiHired is strongest when you keep the resume, cover letter, and saved profile data in one place, so the cleanest path is to finish the resume in the builder first."

## Things not to overclaim

Do not claim from chat that you directly uploaded the resume into HiHired unless you actually used the site/tools.
Do not claim final PDF styling or template fidelity without the user reviewing it in the builder.
Do not claim HiHired Chrome autofill is officially launched yet. If relevant, describe it only as future/downstream product direction and keep the main skill focused on resume, cover letter, and profile preparation.
