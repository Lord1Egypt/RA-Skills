# Weekly report preview — API reference

## Endpoint

`GET https://www.nichestarter.ai/api/public/weekly-report-preview`

## Example response (shape)

```json
{
  "generated_at": "2026-04-07T12:00:00.000Z",
  "report": {
    "id": "uuid",
    "report_title": "Top pain points — Week of ...",
    "summary": "Multi-line markdown or plain text...",
    "created_at": "2026-04-07T00:00:00.000Z",
    "total_pain_points_in_report": 30
  },
  "top_pain_points": [
    {
      "rank": 1,
      "id": "uuid",
      "title": "...",
      "description": "...",
      "mentioned_times": 12,
      "tags": ["..."],
      "overall_score": 8,
      "insight_url": "https://www.nichestarter.ai/insights/pain-points/uuid",
      "primary_source_url": "https://reddit.com/...",
      "subreddits": ["SaaS"]
    }
  ],
  "cta": {
    "website": "https://www.nichestarter.ai",
    "sign_in_url": "https://www.nichestarter.ai/",
    "dashboard_weekly_reports_url": "https://www.nichestarter.ai/dashboard#weeklyreport",
    "public_insights_url": "https://www.nichestarter.ai/insights",
    "message": "Sign in at www.nichestarter.ai ..."
  },
  "notes": []
}
```

## Alignment with app data

- `report_weekly` rows match what signed-in users see in **Dashboard → Weekly Reports** (`reports-client.tsx`): `report_title`, `summary`, `painpoints` (id list), `created_at`.
- `top_pain_points` are the **first five ids** in `painpoints`, in report order (same idea as `getLatestWeeklyReport` preview in `reports.ts`).
- Full detail, opportunities, and email preferences require **authentication** in the app.

## System prompt snippet

```markdown
You summarize NicheStarter's latest weekly pain-point report using only JSON from
GET https://www.nichestarter.ai/api/public/weekly-report-preview.
Output: short brief + top 5 list + sign-in CTA + free weekly email CTA.
Never invent pain points or numbers.
```

## Sample cron (server)

Run every Monday at 08:00 (server local time). Replace the curl + mail parts with your agent webhook or OpenClaw trigger.

```bash
0 8 * * 1 curl -sS "https://www.nichestarter.ai/api/public/weekly-report-preview" -o /tmp/ns-weekly.json || exit 1
# Next: invoke your agent with SKILL.md + /tmp/ns-weekly.json, or pipe JSON into a script that formats and sends email.
```

## Sample GitHub Actions (weekly)

Use `on.schedule` with `cron: '0 13 * * 1'` (UTC Monday 13:00). In the job: `curl` the API, then call your notification step (Slack, email, OpenClaw API) with the response body.

## Deduplication state

Store in a file or secret-backed store:

```json
{ "last_sent_report_id": "uuid-of-report_weekly-row" }
```

Compare to `report.id` in each response before sending.
