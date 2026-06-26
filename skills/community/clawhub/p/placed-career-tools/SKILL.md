---
name: placed-career-tools
description: This skill should be used when the user wants to "match resume to job", "generate cover letter", "optimize resume for job", "get interview questions for company", "generate LinkedIn profile", "check application status", "get salary insights", "negotiate salary", "research company", "analyze resume gaps", or wants to use AI career tools from the Placed platform at placed.exidian.tech.
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "🧭", "homepage": "https://placed.exidian.tech" } }
tags: "career,cover-letter,linkedin,salary,salary-negotiation,company-research,job-match,career-tools,placed,exidian,job-search,ai-career-coach"
---

# Placed Career Tools

Comprehensive AI career toolkit: job-resume matching, cover letters, LinkedIn optimization, salary insights, negotiation scripts, and company research — all via the Placed API. No MCP server required.

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

### Resume-Job Matching

| Tool                      | Description                                        |
| ------------------------- | -------------------------------------------------- |
| `match_job`               | Score how well a resume matches a job description  |
| `analyze_resume_gaps`     | Find missing keywords and skills for a target role |
| `optimize_resume_for_job` | Tailor resume content to a specific job            |

### AI Writing Tools

| Tool                        | Description                                       |
| --------------------------- | ------------------------------------------------- |
| `generate_cover_letter`     | Generate a tailored cover letter                  |
| `generate_linkedin_profile` | AI-optimized LinkedIn headline and About section  |
| `get_interview_questions`   | Get likely interview questions for a company/role |

### Salary & Negotiation

| Tool                                 | Description                              |
| ------------------------------------ | ---------------------------------------- |
| `get_company_salary_data`            | Market salary data by role and company   |
| `generate_salary_negotiation_script` | Personalized salary negotiation script   |
| `analyze_offer`                      | Analyze a job offer against market rates |

### Company Research

| Tool               | Description                                     |
| ------------------ | ----------------------------------------------- |
| `research_company` | Company overview, culture, news, interview tips |

## Usage Examples

**Match resume to job:**

```bash
placed_call "match_job" '{
  "resume_id": "res_abc123",
  "job_description": "Senior Software Engineer at Stripe — distributed systems, Go, Kubernetes..."
}'
# Returns: match score, matched keywords, missing keywords, recommendations
```

**Analyze resume gaps:**

```bash
placed_call "analyze_resume_gaps" '{
  "resume_id": "res_abc123",
  "job_description": "..."
}'
```

**Generate cover letter:**

```bash
placed_call "generate_cover_letter" '{
  "resume_id": "res_abc123",
  "company_name": "Airbnb",
  "job_title": "Staff Engineer",
  "job_description": "...",
  "tone": "professional"
}'
```

**Get salary data:**

```bash
placed_call "get_company_salary_data" '{
  "company_name": "Google",
  "position": "Senior Software Engineer",
  "location": "San Francisco, CA"
}'
```

**Generate negotiation script:**

```bash
placed_call "generate_salary_negotiation_script" '{
  "current_offer": 200000,
  "target_salary": 240000,
  "justification": [
    "6 years distributed systems experience",
    "Led 3 high-impact projects",
    "Market rate for this role in SF is $230-260K"
  ]
}'
```

**Generate LinkedIn profile:**

```bash
placed_call "generate_linkedin_profile" '{"resume_id":"res_abc123"}'
```

**Research a company:**

```bash
placed_call "research_company" '{"company_name":"Databricks"}'
```

## Common Workflows

**Before applying:**

1. `match_job` — check resume-job fit score
2. `analyze_resume_gaps` — find missing keywords
3. `optimize_resume_for_job` (via placed-resume-optimizer) — tailor resume
4. `generate_cover_letter` — write tailored cover letter

**Negotiate an offer:**

1. `get_company_salary_data` — benchmark the offer
2. `analyze_offer` — get full market comparison
3. `generate_salary_negotiation_script` — get negotiation talking points

## Additional Resources

- **`references/api-guide.md`** — Full API reference with all parameters and response schemas
