---
name: nichestarter-weekly-report-preview
description: Summarizes the latest NicheStarter weekly pain-point report from the public preview API, lists top five pain points, and guides users to sign in for the full report and free weekly email subscription. Supports scheduled runs (cron, OpenClaw, or other agents) to deliver the digest with a consistent style. Use when the user asks for the weekly report, Monday digest, top pain points this week, teaser content, or automated weekly delivery.
---

# NicheStarter Weekly Report Preview

## Purpose

Turn the **latest weekly pain-point report** into a short, trustworthy teaser:

- Brief summary aligned with `report.summary` and `report.report_title`
- **Top 5 pain points** (title, short description, optional source + insight link)
- Clear CTA: **sign in** for the full report and **subscribe free** for weekly email (Mondays)

## Data source (API-first)

Fetch:

- `GET https://www.nichestarter.ai/api/public/weekly-report-preview`

No authentication. Response includes `report`, `top_pain_points` (5), and `cta` with URLs.

If the API returns 404, say no report is published yet and point to `https://www.nichestarter.ai` to explore insights or sign up.

## Workflow

1. Call the preview endpoint and read `report`, `top_pain_points`, `cta`.
2. Write a **2–4 sentence** executive brief (no hype, no invented stats).
3. List **exactly five** items when present: rank, title, one-line why it matters, optional `primary_source_url`, `insight_url`.
4. Add CTA block:
   - Full report: sign in → Dashboard → Weekly Reports (`cta.dashboard_weekly_reports_url` or `https://www.nichestarter.ai/dashboard#weeklyreport`)
   - Free weekly email: subscribe on the site (`cta.message` + `cta.website`)
5. Do **not** promise paid-only features to free users; use neutral wording (“see full list and features after sign-in”).

## Output format

```markdown
## Weekly pain-point snapshot — [report_title]
**Report date:** [created_at as human-readable]
[Brief summary paragraph]

### Top 5 this week
1. ...
2. ...
...

### Get the full picture
- Sign in: [sign_in_url or www.nichestarter.ai]
- Open **Weekly Reports** in the dashboard: [dashboard_weekly_reports_url]
- **Free** weekly email with more detail (Mondays): mention www.nichestarter.ai
```

## Rules

- English unless the user asks otherwise.
- Do not fabricate pain points, rankings, or subscriber counts.
- Do not expose internal env vars or non-public APIs.
- Treat content as **community signal**, not guaranteed demand.

## Scheduled delivery (cron / OpenClaw / other agents)

Use this skill on a **fixed schedule** so users get the same structure every week.

### When to run

- **Default:** once per week on **Monday**, after your platform’s weekly report is published (align with NicheStarter’s “Monday” weekly email messaging).
- Pick one timezone (e.g. `America/New_York` 08:00) and keep it stable for recipients.

### Cron / scheduler setup (conceptual)

1. Configure the host (OpenClaw, GitHub Actions, `cron`, n8n, etc.) to trigger **one job per week**.
2. Job steps:
   - `GET https://www.nichestarter.ai/api/public/weekly-report-preview`
   - If `404` or empty `top_pain_points`: send a **short fallback** (“No new weekly report yet — check https://www.nichestarter.ai”).
   - Else: follow **Workflow** and **Delivery style** below, then send via your channel (email, DM, Slack, etc.).
3. **Deduplication:** persist the last sent `report.id` from the JSON. If the next run returns the same `report.id`, skip sending (avoids double-send if cron overlaps).
4. **Retries:** on `5xx`, retry with backoff; do not fabricate content if the API never succeeds.

### Delivery style (proper format for end users)

Apply the same structure whether the message is email, chat, or push:

- **Subject / first line (email or thread):**  
  `NicheStarter — Weekly pain points · [YYYY-MM-DD]` or use `report.report_title` shortened to ~60 characters.
- **Opening:** one line context: “Here’s this week’s snapshot from community discussions (teaser).”
- **Body:** use the **Output format** section (headings, numbered top 5, bullets for links).
- **Links:** use full `https://` URLs from `cta` and each `insight_url` / `primary_source_url` (plain text, one URL per line in chat clients if line-wrapping breaks).
- **Tone:** calm, practical, no hype; no emojis required (optional single ✉️ or 📊 if the channel expects it).
- **Length:** keep under ~400 words for email; under ~2500 characters for SMS-style limits if applicable.
- **Footer:** always include `cta.website` and one line: sign in for full report + free weekly subscription on the site.

### OpenClaw (or similar agent) prompt snippet

When scheduling the agent, attach this skill and use a user task like:

```text
Run the NicheStarter weekly report preview skill.
Fetch the API, build the digest using the Output format and Delivery style sections,
then send it to [recipient / channel] with subject line as specified.
If report.id matches [last_sent_report_id], reply only "Skipped (already sent)."
```

Store `last_sent_report_id` in OpenClaw memory, a small file, or your workflow state.

## Additional resources

- Response shape, examples, and sample cron: [reference.md](reference.md)

## Install (Cursor / other agents)

- Raw file URL (production): `https://www.nichestarter.ai/skills/nichestarter-weekly-report-preview/SKILL.md`
- Copy this folder into your agent’s skills directory (or download `SKILL.md` + `reference.md` from the URL above).
