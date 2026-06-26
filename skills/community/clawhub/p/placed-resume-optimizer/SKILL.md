---
name: placed-resume-optimizer
description: This skill should be used when the user wants to "optimize resume for job", "check ATS score", "improve resume bullets", "analyze resume gaps", "tailor resume to job description", "get ATS compatibility score", "improve bullet points", "match resume to job posting", "fix resume for ATS", or wants to maximize their resume's impact and ATS compatibility using the Placed platform at placed.exidian.tech.
version: 1.0.0
homepage: https://placed.exidian.tech
metadata:
  { "openclaw": { "emoji": "🎯", "homepage": "https://placed.exidian.tech" } }
tags: "ats,ats-checker,ats-optimizer,resume-optimization,keyword-optimization,resume-score,job-match,resume-tailor,ats-score,resume-keywords,placed,exidian,career"
---

# Placed Resume Optimizer

AI-powered resume optimization for ATS compatibility, keyword matching, and bullet point quality — all via the Placed API. No MCP server required.

## API Key

Load the key from `~/.config/placed/credentials`, falling back to the environment:

```bash
if [ -z "$PLACED_API_KEY" ] && [ -f "$HOME/.config/placed/credentials" ]; then
  source "$HOME/.config/placed/credentials"
fi
```

If `PLACED_API_KEY` is still not set, ask the user:

> "Please provide your Placed API key (get it at https://placed.exidian.tech/settings/api)"

Then save it for future sessions:

```bash
mkdir -p "$HOME/.config/placed"
echo "export PLACED_API_KEY=<key_provided_by_user>" > "$HOME/.config/placed/credentials"
export PLACED_API_KEY=<key_provided_by_user>
```

## How to Call the API

```bash
placed_call() {
  local tool=$1
  local args=${2:-'{}'}
  curl -s -X POST https://placed.exidian.tech/api/mcp \
    -H "Authorization: Bearer $PLACED_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['content'][0]['text'])"
}
```

## Available Tools

| Tool                          | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `check_ats_compatibility`     | ATS compatibility score and recommendations               |
| `get_resume_quality_score`    | Overall quality score with section breakdown              |
| `analyze_resume_gaps`         | Missing keywords and skills vs. a job description         |
| `match_job`                   | Score resume-job fit (0-100) with keyword breakdown       |
| `optimize_resume_for_job`     | Tailor resume content to a specific job                   |
| `optimize_resume_section`     | Optimize a specific section (experience, skills, summary) |
| `improve_bullet_point`        | Rewrite a single bullet point with stronger impact        |
| `generate_resume_from_prompt` | Generate a complete resume from natural language          |

## Usage Examples

**Check ATS compatibility:**

```bash
placed_call "check_ats_compatibility" '{"resume_id":"res_abc123"}'
# Returns: ATS score, formatting recommendations
```

**Get quality score:**

```bash
placed_call "get_resume_quality_score" '{"resume_id":"res_abc123"}'
# Returns: overall score, breakdown by section
```

**Analyze gaps vs. a job description:**

```bash
placed_call "analyze_resume_gaps" '{
  "resume_id": "res_abc123",
  "job_description": "Senior Software Engineer at Stripe — Go, distributed systems, Kafka..."
}'
# Returns: critical gaps, keyword gaps, suggestions
```

**Score resume-job match:**

```bash
placed_call "match_job" '{
  "resume_id": "res_abc123",
  "job_description": "..."
}'
# Returns: match score 0-100, matched/missing keywords
```

**Optimize resume for a job:**

```bash
placed_call "optimize_resume_for_job" '{
  "resume_id": "res_abc123",
  "job_description": "Senior Software Engineer at Airbnb..."
}'
# Returns: suggested section improvements
```

**Improve a single bullet:**

```bash
placed_call "improve_bullet_point" '{
  "bullet_point": "Worked on database optimization",
  "context": "Senior SRE at Uber"
}'
# Returns: rewritten bullet with metrics and impact
```

**Optimize a specific section:**

```bash
placed_call "optimize_resume_section" '{
  "resume_id": "res_abc123",
  "section_type": "experience",
  "section_data": "Current bullets here...",
  "job_description": "Target job description..."
}'
```

## Optimization Workflow

Run this before every application:

1. `match_job` — check current fit score
2. `analyze_resume_gaps` — identify missing keywords
3. `check_ats_compatibility` — catch formatting issues
4. `improve_bullet_point` — strengthen weak bullets
5. `optimize_resume_for_job` — get full tailoring suggestions
6. `match_job` again — confirm score improved

## Bullet Point Formula

```
[Action Verb] + [What You Did] + [How/Scale] + [Quantified Result]
```

**Before:** "Worked on database optimization"
**After:** "Optimized PostgreSQL query performance by 40%, reducing p99 latency from 500ms to 300ms for 10M+ daily users"

**Strong action verbs:**

- Technical: Architected, Built, Designed, Optimized, Implemented, Engineered, Migrated
- Leadership: Led, Managed, Mentored, Spearheaded, Directed
- Impact: Improved, Reduced, Increased, Accelerated, Scaled, Transformed

## ATS Compatibility Rules

| Issue                            | Fix                                    |
| -------------------------------- | -------------------------------------- |
| Tables or columns                | Use single-column layout               |
| Graphics or images               | Remove all non-text elements           |
| Unusual fonts                    | Use Arial, Calibri, or Times New Roman |
| Headers/footers with key info    | Move to main body                      |
| Inconsistent date formats        | Use MM/YYYY throughout                 |
| Missing job description keywords | Add naturally to skills and bullets    |

## Tips

- ATS score below 70 → fix formatting first, then keywords
- Run `match_job` before and after optimizing to measure improvement
- Always review `optimize_resume_for_job` suggestions before applying
- Keep a master resume and create tailored copies per application

## Additional Resources

- **`references/api-guide.md`** — Full API reference with scoring rubrics and response schemas
