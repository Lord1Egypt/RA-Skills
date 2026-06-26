# HireMe Pro

**Your personal AI career coach. Perfect resumes, tailored cover letters, zero monthly fees.**

Stop paying $24/month to Zety or Resume.io. HireMe Pro is a Free and open-source. that gives you everything those subscription services charge for — and more.

---

## What You Get

- **Instant Resume Building** — Paste your LinkedIn, drop your old resume, or just chat about your experience. HireMe Pro handles the rest.
- **4 Premium Templates** — Clean, Modern, Executive, and Creative. All ATS-optimized so your resume actually gets past the robots.
- **Job Match Scoring** — Paste a job posting and see exactly how well you match, which keywords you're missing, and how to fix the gaps.
- **Tailored Resumes** — One click to customize your resume for a specific job. Your master resume stays untouched.
- **Cover Letter Generator** — Paste a job description, get a cover letter that actually references the company and role. Not generic fill-in-the-blank garbage.
- **Interview Prep** — HireMe Pro analyzes the job and company, then quizzes you with the questions they're most likely to ask. Includes suggested answers based on YOUR experience.
- **Application Tracker** — Keep track of where you applied, what version of your resume you sent, and when to follow up.
- **Salary Research & Negotiation** — Know what the role pays and get talking points for your offer negotiation.
- **Beautiful PDF Export** — Professional, recruiter-approved PDFs that look like a design agency made them.

---

## How It Works

1. **Drop your history** — Paste your LinkedIn profile, upload an old resume, or just tell the agent about your work experience.
2. **Refine** — Tell it what kind of job you want. It rewrites your bullets to highlight exactly what employers are looking for.
3. **Export** — Pick a template, get a beautiful ATS-friendly PDF instantly.

That's it. Three minutes from "I need a resume" to "here's your PDF."

---

## 🛡️ Codex Security Verified

This skill has been audited for safety:
- ✅ **No data exfiltration** — Your resume data never leaves your machine
- ✅ **No external API calls** — Everything runs locally
- ✅ **No hardcoded secrets** — Clean, safe code
- ✅ **Prompt injection defended** — Job descriptions and pasted content can't hijack your agent
- ✅ **PII protection** — Your personal info (name, phone, address) is handled with care

See `SECURITY.md` for the full audit report.

---

## Setup

See `SETUP-PROMPT.md` for one-copy-paste installation.

**Requirements:**
- An AI agent (OpenClaw, Claude, or similar)
- Playwright for PDF generation (`pip3 install playwright && playwright install chromium`)

---

## What's Included

```
hireme-pro/
 SKILL.md — The skill (your agent reads this)
 README.md — You're reading it
 SETUP-PROMPT.md — Installation instructions
 SECURITY.md — Security audit report
 config/
 hireme-config.json — Your preferences
 scripts/
 generate-resume-pdf.sh — PDF rendering engine
 templates/
 clean.html — Clean template
 modern.html — Modern template
 executive.html — Executive template
 creative.html — Creative template
 examples/
 resume-tailoring.md
 cover-letter-generation.md
 interview-prep.md
 dashboard-kit/
 DASHBOARD-SPEC.md — Build spec for the visual dashboard add-on
```

---
