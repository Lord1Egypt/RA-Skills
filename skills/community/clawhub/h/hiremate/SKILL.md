---
name: hiremate
description: >
  AI recruiting assistant for generating job descriptions, resume screening criteria,
  interview questions, candidate scoring, match analysis, salary reports, and interview evaluations.
  Use when the user asks to: create a job description (JD), write a job posting, generate interview questions,
  screen resumes, evaluate candidates, analyze candidate-job fit, check salary benchmarks/compensation data,
  create interview scorecards, or build recruiting workflows. Supports both free features (JD generation,
  screening criteria, interview questions) and premium features (resume scoring, candidate matching,
  salary reports, interview evaluations). Triggers on phrases like "job description", "JD", "招聘",
  "interview questions", "screen resume", "candidate match", "salary report", "compensation",
  "interview evaluation", "hire", "recruit".
---

# HireMate — AI Recruiting Assistant

Complete recruiting toolkit: generate JDs, screen resumes, create interview questions, score candidates, analyze matches, benchmark salaries, and evaluate interviews.

## Free Features

### Generate Job Description
```bash
python3 <skill_dir>/scripts/generate_jd.py \
  --role <role_template> --company <name> --seniority <level> \
  --location <loc> --language <lang> --framework <fw> \
  --industry <ind> --years <n> [--output file.md]
```
Roles: `software_engineer`, `product_manager`, `data_scientist`, `ux_designer`, `marketing_manager`, `sales_representative`

### Generate Screening Criteria
```bash
python3 <skill_dir>/scripts/generate_screening_criteria.py \
  --role <role> --years <n> --languages "Py,Go" \
  --frameworks "Django" --industry <ind> [--format json]
```

### Generate Interview Questions
```bash
python3 <skill_dir>/scripts/generate_interview_questions.py \
  --role <role> --level <junior|mid|senior|all> \
  --num-tech 5 --num-behavioral 3 [--seed <n> for reproducibility]
```

## Premium Features

### Score Resume
```bash
python3 <skill_dir>/scripts/score_resume.py \
  --resume "<text>" --keywords skill1 skill2 skill3 \
  --min-years 3 --education <bachelors|masters|phd>
```
Resume can be text or `@file_path`. Returns weighted score (keyword 40%, experience 25%, education 15%, tech skills 20%).

### Candidate-Job Match Analysis
```bash
python3 <skill_dir>/scripts/match_candidate.py \
  --candidate-skills a b c --candidate-years 5 \
  --candidate-edu bachelors --candidate-location "SF" \
  --job-skills a b d --job-min-years 3 \
  --job-role software_engineer --job-seniority mid
```
Returns skill overlap, experience gap, education match, and salary context.

### Salary Market Report
```bash
python3 <skill_dir>/scripts/salary_report.py \
  --role <role> --region <us|europe|uk|asia_pacific> \
  --seniority <junior|mid|senior|staff>
```
Includes regional comparisons and market notes.

### Interview Evaluation Report
```bash
python3 <skill_dir>/scripts/interview_evaluation.py \
  --candidate "Name" --role "Role" \
  --technical 85 --problem-solving 80 --communication 75 \
  --cultural-fit 90 --experience 80 --learning 85 \
  --strengths "Strong X" "Great Y" \
  --concerns "Needs Z"
```
Weighted scoring: technical 30%, problem-solving 20%, communication 15%, cultural fit 15%, experience 10%, learning 10%.

## Reference Data

- `references/jd_templates.json` — JD templates for 6 role types
- `references/interview_questions_db.json` — 50+ questions across 6 categories
- `references/salary_data.json` — Global salary benchmarks (US, EU, UK, APAC)

## Usage Notes

- All scripts support `--format markdown` (default) and `--format json`
- Use `--output file.md` to save to file instead of stdout
- Use `--seed` for reproducible interview question sets
- Salary data should be updated quarterly with latest market data
- For roles not in templates, use the AI to generate custom JDs based on the template structure
