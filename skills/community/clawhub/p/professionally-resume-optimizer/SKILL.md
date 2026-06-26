---
name: resume-optimizer
description: Optimize and rewrite resumes for overseas job applications. Activate when user asks to improve, rewrite, review, or tailor a resume or CV, or mentions 简历/CV/resume/求职. Analyzes ATS compatibility, strengthens bullet points with STAR framework, quantifies achievements, and adapts tone for target role and market (US/UK/Singapore/Australia).
metadata: {"openclaw": {"emoji": "📄"}}
---

# Resume Optimizer

Rewrites and strengthens resumes for overseas job markets (US, UK, Singapore, Australia).

## When to Activate

- User shares resume content and asks to improve / rewrite / review / polish
- User asks to tailor resume for a specific job description
- User asks to make resume ATS-friendly or pass applicant tracking systems
- User mentions "简历", "CV", "resume", "cover letter", "job application", "求职"

## Core Workflow

1. **Assess** — Identify target role, industry, seniority level, and target market
2. **Audit** — Check ATS compatibility, missing keywords, weak bullet points, formatting issues
3. **Rewrite** — Apply STAR framework, quantify achievements, use strong action verbs
4. **Tailor** — Match keywords from job description if provided
5. **Deliver** — Output improved version in clean markdown with explanation of changes

## Rewriting Rules

### Bullet Points (highest priority)

Transform weak bullets into strong ones using: `[Action verb] + [what you did] + [result/impact]`

| Weak (Before) | Strong (After) |
|---|---|
| Responsible for managing team | Led cross-functional team of 8 engineers across 3 time zones |
| Worked on marketing campaigns | Drove 3 product campaigns reaching 2M+ impressions, lifting CTR by 23% |
| Helped improve customer service | Reduced average ticket resolution time from 48h to 6h (-87.5%) |
| Did data analysis | Built automated reporting pipeline saving 12 analyst-hours per week |

**Strong past-tense action verbs by category:**
- Leadership: Led, Managed, Directed, Mentored, Coached, Oversaw
- Building: Built, Developed, Launched, Architected, Engineered, Designed
- Growth: Grew, Scaled, Expanded, Increased, Drove, Boosted
- Improvement: Optimized, Reduced, Streamlined, Automated, Accelerated
- Achievement: Delivered, Exceeded, Achieved, Closed, Won, Secured

**Quantify everything possible:**
- Team size, budget managed, revenue generated, cost saved
- Percentages, timeframes, absolute numbers
- If no numbers available, use relative terms: "top-performing", "first in company", "3× faster"

### ATS Compatibility Checklist

- No tables, text boxes, columns, headers/footers, or graphics
- Standard section headers only: `Experience`, `Education`, `Skills`, `Summary`
- Keywords from job description must appear **verbatim** (not paraphrased)
- Spell out acronyms at least once: "Search Engine Optimization (SEO)"
- Recommend `.docx` or plain text; avoid image-heavy PDFs

### Resume Structure (standard order)

1. Contact info + LinkedIn URL + GitHub (for tech roles)
2. Professional Summary (3–4 lines, keyword-rich, tailored to role)
3. Work Experience (reverse chronological, 3–5 bullets per role)
4. Skills (hard skills grouped by category, then soft skills)
5. Education
6. Optional: Projects, Certifications, Publications, Languages

### Professional Summary Formula

```
[Job title/seniority] with [X years] experience in [domain]. 
Proven track record of [key achievement]. 
Skilled in [top 3 relevant skills]. 
Seeking to [contribution] at [company type/role].
```

## Market-Specific Rules

| Market | Key Rules |
|---|---|
| **USA** | No photo, age, or gender. 1 page (0–5 yrs exp), 2 pages max. Very achievement-focused. |
| **UK** | Called "CV". Include personal profile at top. 2 pages standard. Slightly more formal tone. |
| **Singapore** | Photo optional. Bilingual/multilingual skills valued. 2 pages standard. Include NRIC only if asked. |
| **Australia** | Called "resume". Include referees section ("References available on request" is fine). Conversational tone OK. |

## Output Format

Always structure the response as:

```
## ✅ What's Working
[2–3 strengths in the current resume to preserve]

## 🔧 Key Issues Found
[Top issues ranked by impact, e.g.:]
1. Bullet points lack quantified results (high impact)
2. Missing keywords for target role (high impact)  
3. Summary too generic (medium impact)

## 📝 Rewritten Resume
[Full improved resume in clean markdown]

## 💡 Role-Specific Tips
[3 actionable suggestions specific to the target position/industry]
```

## Handling Missing Information

If the user's resume lacks numbers or context:
- Ask 1–2 targeted questions: "What was the team size?" or "Do you have any metrics for this project?"
- If user can't provide data, use qualitative strengtheners: "top-performing team", "high-visibility initiative"
- Never fabricate numbers

## Additional Resources

- Before/after rewrite examples: [examples.md](examples.md)
- Industry-specific templates: [templates.md](templates.md)
