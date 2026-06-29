---
name: hr-resume-evaluation
description: Use when a recruiter wants to batch-evaluate resumes, run general resume quality checks, optionally match resumes to a JD and company background, and produce evidence-backed Markdown and CSV review reports.
---

# HR Resume Evaluation

## Core Rule

Use this Skill only as a recruiter review aid. Never present scores as final hiring, rejection, elimination, or admission decisions.

## Before Use

1. Put resumes in a local input folder. Supported resume formats: Markdown, TXT, PDF, DOCX.
2. Optionally prepare a JD file and company background file in Markdown or TXT.
3. Set the API key environment variable configured in `config/model.yaml`, default `DEEPSEEK_API_KEY`.
4. Read `references/scoring-rubric.md`, `references/role-family-taxonomy.md`, `references/compliance-policy.md`, and `references/output-schema.md`.

## Command

```powershell
python scripts/evaluate_resumes.py `
  --resumes input/resumes `
  --jd input/jd.md `
  --company input/company.md `
  --output reports `
  --config config/evaluation.yaml `
  --model-config config/model.yaml
```

Omit `--jd` and `--company` for general resume quality review only.

## Required Outputs

- One Markdown report per successfully evaluated resume.
- One batch summary Markdown report.
- One CSV summary file.
- Clear failure records for unreadable or invalid files.

## Safety Rules

- Do not score protected or job-irrelevant traits.
- Do not infer missing resume facts.
- Do not perform background investigation.
- Do not automatically reject or approve candidates.
- Treat model output as advisory until reviewed by a human recruiter.
