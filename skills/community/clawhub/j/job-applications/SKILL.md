# Job Application Automation Skill

## Overview
Automated job search and application system for Abed Mir. Searches Indeed for matching jobs, analyzes fit, tailors resume, and applies via ATS platforms (Greenhouse, Lever, Workday, Indeed Easy Apply).

## Directory Structure
```
job-applications/
├── config.json              # Search criteria, filters, settings
├── resume-source/
│   ├── resume.json          # Structured resume data (source of truth)
│   └── resume.tex           # LaTeX template
├── scripts/
│   └── tailor_resume.py     # Resume tailoring + LaTeX generation
├── tailored-resumes/        # Generated PDFs per application
├── tracking/
│   └── applications.json    # Application log
└── logs/                    # Run logs
```

## Workflow (Per Run)

### 1. Search Jobs
- Open Indeed in browser (pinned tab)
- Search each target title from config.json
- Filter: Remote or DFW hybrid, posted in last 24h
- Collect job URLs, titles, companies

### 2. Deduplicate
- Check each job against tracking/applications.json
- Skip already-applied or already-skipped jobs

### 3. Analyze Fit
For each new job:
- Navigate to the job posting, read full description
- Check against avoid_industries and avoid_keywords
- Score fit based on skills match, experience alignment
- Prioritize AI/agent roles highest

### 4. Tailor Resume
For jobs that pass fit check:
- Use resume.json as base
- Reorder bullet points to lead with most relevant experience
- Emphasize matching skills/technologies
- DO NOT fabricate experience or skills
- Generate PDF via LaTeX compilation

### 5. Apply
Detect ATS platform from the application URL:
- **Greenhouse** (boards.greenhouse.io): Single page form — name, email, phone, resume upload, optional fields
- **Lever** (jobs.lever.co): Single page — similar to Greenhouse
- **Workday** (myworkday*.com): Multi-step wizard — create account or sign in, then fill each step
- **Indeed Easy Apply**: Quick apply through Indeed's interface

Fill all required fields from config.json candidate data. Upload tailored PDF.

### 6. Log
Record in applications.json:
```json
{
  "id": "uuid",
  "date": "ISO timestamp",
  "company": "Company Name",
  "title": "Job Title",
  "url": "application URL",
  "platform": "greenhouse|lever|workday|indeed",
  "status": "applied|skipped|failed",
  "skip_reason": null,
  "resume_version": "tailored-resumes/company-title.pdf",
  "notes": ""
}
```

## Cron Schedule
Runs 3x daily:
- 8:00 AM CT — Morning sweep (catch overnight postings)
- 12:00 PM CT — Midday sweep
- 5:00 PM CT — Evening sweep (catch same-day postings)

## ATS Form Filling Reference

### Greenhouse
- URL pattern: `boards.greenhouse.io/*` or `job-boards.greenhouse.io/*`
- Fields: First Name, Last Name, Email, Phone, Resume (file upload), Location, LinkedIn (optional), Website (optional)
- Sometimes has custom questions (dropdown, text, checkbox)
- Submit button usually at bottom

### Lever
- URL pattern: `jobs.lever.co/*`
- Fields: Full Name, Email, Phone, Resume (file upload), LinkedIn (optional), Website (optional), Current Company (optional)
- May have additional questions
- "Submit application" button

### Workday
- URL pattern: `*.myworkdayjobs.com/*` or `*.wd5.myworkdayjobs.com/*`
- Multi-page: Sign in/Create account → My Information → My Experience → Application Questions → Review → Submit
- Requires parsing each page and filling iteratively
- Most complex — may need human intervention for unusual fields

### Indeed Easy Apply
- Indeed session is logged in on the openclaw browser (abedmir31@gmail.com)
- If session expires, navigate to https://secure.indeed.com/auth, enter abedmir31@gmail.com, and ask Abed for the email code in #job-applications Discord channel
- Fields pre-filled from Indeed profile
- May ask additional screening questions
- Click "Apply now" → fills in the Indeed Easy Apply modal
- Quick submit

### Indeed Session Notes
- Login uses email verification code (no password)
- Session persists in the openclaw browser context
- If you see "Sign in" in the nav instead of "Welcome, Abed", the session expired

### LinkedIn Easy Apply
- LinkedIn session is logged in on the openclaw browser (Abed Mir profile)
- Navigate to https://www.linkedin.com/jobs/search/ to search for jobs
- Filter by Easy Apply, Remote, Date Posted
- Click "Easy Apply" button on a job listing
- LinkedIn Easy Apply modal pre-fills most info from profile
- Upload resume, answer any additional questions, submit
- If session expires, navigate to https://www.linkedin.com/login and ask Abed for credentials in #job-applications

### LinkedIn Session Notes
- Login uses email + password (stored in browser session)
- Session persists in the openclaw browser context
- If you see the login page instead of the feed, the session expired

## Important Rules
- NEVER lie on applications — only reorder/emphasize existing experience
- Skip haram industries (banking, mortgage, lending, alcohol, gambling, etc.)
- Log EVERY job encountered (applied or skipped with reason)
- If an application fails mid-form, log as "failed" and move on
- Report summary to #job-applications Discord channel after each run
- **ALWAYS close browser tabs after completing an application** — use `browser(action="close")` or navigate away to prevent memory buildup and tab clutter
