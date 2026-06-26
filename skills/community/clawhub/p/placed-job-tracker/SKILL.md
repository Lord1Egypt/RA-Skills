---
name: placed-job-tracker
description: This skill should be used when the user wants to "track job applications", "add a job application", "update application status", "view my job pipeline", "get application analytics", "delete job application", or wants to manage their job search using the Placed career platform at placed.exidian.tech.
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "📋", "homepage": "https://placed.exidian.tech" } }
tags: "job-tracker,job-applications,application-tracker,job-pipeline,job-search,career,kanban,job-management,placed,exidian,application-status"
---

# Placed Job Tracker

Track and manage your job applications via the Placed API. No MCP server required — all calls are made directly with curl.

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

| Tool                        | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| `add_job_application`       | Add a new job application                            |
| `list_job_applications`     | View all applications, optionally filtered by status |
| `update_job_status`         | Move an application to a new stage                   |
| `delete_job_application`    | Remove an application                                |
| `get_application_analytics` | Pipeline analytics and conversion rates              |

## Usage Examples

**Add a job application:**

```bash
placed_call "add_job_application" '{
  "company": "Stripe",
  "position": "Senior Software Engineer",
  "job_url": "https://stripe.com/jobs/123",
  "status": "APPLIED",
  "notes": "Referral from John"
}'
```

**List all applications:**

```bash
placed_call "list_job_applications"
```

**Filter by status:**

```bash
placed_call "list_job_applications" '{"status":"INTERVIEWING"}'
```

**Update application status:**

```bash
placed_call "update_job_status" '{
  "job_id": "job_abc123",
  "status": "OFFER",
  "notes": "Offer: $200K base + equity"
}'
```

**Get analytics:**

```bash
placed_call "get_application_analytics" '{"date_range":"30d"}'
# Returns: total count, breakdown by status, response rates
```

**Delete an application:**

```bash
placed_call "delete_job_application" '{"job_id":"job_abc123"}'
```

## Application Statuses

- `WISHLIST` — Saved for later
- `APPLIED` — Application submitted
- `INTERVIEWING` — In interview process
- `OFFER` — Offer received
- `REJECTED` — Application rejected
- `WITHDRAWN` — Withdrew application

## Job Search Tips

1. Apply to 5-10 roles per week for best results
2. Add applications immediately after submitting — tracking works best when complete
3. Use `placed-resume-optimizer` to tailor your resume before each application
4. Follow up after 1-2 weeks if no response
5. Use analytics to identify which pipeline stages need improvement
6. Aim for a 20%+ phone screen rate; if lower, improve your resume

## Additional Resources

- **`references/api-guide.md`** — Full API reference with all parameters and response schemas
