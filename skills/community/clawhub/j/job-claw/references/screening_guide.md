# JobClaw Screening Guide

Reference for AI agents scoring jobs against a candidate profile.

## Scoring Dimensions (100 pts total)

| Dimension          | Weight | Notes |
|--------------------|--------|-------|
| ML Technical Fit   | 35%    | Core ML/AI content relevance |
| Skill Match        | 30%    | Python, frameworks, domain |
| Career Potential   | 20%    | Growth, research, team quality |
| Salary Signal      | 15%    | Competitiveness for seniority |

## Hard Filters (auto-exclude)

- Location outside UK/Europe/Remote unless config says otherwise
- No ML/AI/Data Science technical content
- Pure management, pure design, pure BI/analytics (no model work)
- Internship if user doesn't want internships

## Score Bands

| Score | Label     | Action |
|-------|-----------|--------|
| 85–100 | Strong match | Priority apply; highlight immediately |
| 70–84  | Good match   | Apply; standard priority |
| 55–69  | Weak match   | Save but deprioritise |
| < 55   | Poor match   | Skip (filtered out by default) |

## Interview Type Classification

| Type             | Description | Example roles |
|------------------|-------------|--------------|
| Research Talk    | 20–40 min presentation + Q&A; no coding | Postdoc, Research Scientist at labs |
| No Leetcode      | Behavioral + ML knowledge; Python basics | Bupa, Prolific, Kraken |
| Case Study       | Business/ML case + presentation | McKinsey, BCG, GSK, Deloitte |
| Take-Home        | 1-3 day ML task; Jupyter notebook | Many startups, Oura, Cleo |
| Fair Coding      | Basic Python + ML deep-dive; not competitive DSA | Anthropic, Microsoft Applied |
| Standard Coding  | LeetCode medium; data structures | Most mid-size tech |
| Heavy Leetcode   | LeetCode hard; graphs, DP | DeepMind, Amazon, Meta |
| Unknown          | Not enough info to classify | — |

## ML Direction Tags

Use these in the `ml_direction` column:

- `General ML/AI` — broad data science/ML
- `NLP/LLM` — language models, NLP, text
- `Computer Vision` — images, video, detection
- `Multimodal` — fusion of modalities
- `Healthcare AI` — clinical, biomedical, pharma
- `Wearable/IoT` — sensors, HAR, ubicomp
- `FinTech` — fraud, risk, finance
- `RL/Robotics` — reinforcement learning, robotics
- `ML Platform` — MLOps, infrastructure
- `Affective Computing` — emotion, sentiment, physiological

## AI Search Prompt Template

When using an AI agent (Claude Code, etc.) to search and score jobs, use this prompt pattern:

```
You are running a job search for [USER_NAME].

Background: [USER_BACKGROUND]
Target roles: [TARGET_ROLES]
Key skills: [SKILL_KEYWORDS]

Search [PLATFORM] for:
  Keywords: [KEYWORDS]
  Location: [LOCATIONS]
  Limit: 25 per keyword

For each job, output:
  - Company, Role, Location, Work Mode, Salary (if shown)
  - Match Score (0-100) with brief reasoning
  - Interview Type (from the classification above)
  - ML Direction
  - Seniority

Only include jobs with Score >= [MIN_SCORE].

End with:
  SUMMARY_[MODE]: Added X jobs. Top match: [Company] [Role] (Score: XX)
```

## Scoring Calibration Tips

- Adjust `min_score` in config.json if too many/few jobs are found
- Add domain keywords to `user.skill_keywords` in config to boost relevant results
- The `job_category` field (`coding` / `noncoding`) controls which search mode found the job
- Keyword scoring is additive: each matching positive keyword adds ~5 pts from a base of 50
