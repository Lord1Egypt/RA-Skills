---
name: outreach-demo
description: Research a business website, produce a concise prospect report, recommend concrete OpenClaw use cases, and draft a tailored outreach email. Use when demonstrating OpenClaw to a business owner, preparing personalized prospecting materials from a website URL + contact email, or turning website research into an approval-gated email draft.
---

# Outreach Demo

Build a draft-first outreach package from three inputs: business name, website URL, and contact email.

Keep the workflow evidence-based, concise, and approval-gated for any email send.

## Workflow

1. **Intake**
   - Collect:
     - business name
     - contact name if available
     - contact email
     - website URL
     - optional business notes
   - If website URL or email is missing, ask only for the missing field.

2. **Website research**
   - Inspect the public website only.
   - Prefer homepage, about, services/products, contact, and selected blog/resources pages.
   - Extract only visible, supportable observations.
   - Do not guess internal systems, revenue, staffing, or pain points.

3. **OpenClaw fit analysis**
   - Propose up to 3 concrete OpenClaw use cases.
   - Rank them by:
     - visible fit
     - likely business value
     - lowest-friction starting point
   - Also produce:
     - one `priority_move`
     - a short `why_it_matters[]` list
   - Phrase uncertain conclusions as “likely”, “appears”, or “suggests”.

4. **Report generation**
   - Use `references/report-format.md` for section shape.
   - For plain operator review, render markdown with:
     - `scripts/render_outreach_report.py --input <json> --output <md>`
   - For visually stronger delivery, render a polished HTML one-page brief with:
     - `scripts/render_outreach_report_html.py --input <json> --output <html>`
   - Preferred showcase artifact: convert the HTML brief to PDF with:
     - `scripts/render_outreach_report_pdf.sh --input <html> --output <pdf>`
   - Prefer PDF for live outreach when visual impact matters.

5. **Email draft generation**
   - Default to the value-first / “free doughnut” framing: give the prospect a small concrete asset before asking for time.
   - Use `references/email-template.md` for default tone and structure.
   - Read `references/value-first-outreach.md` when you need to optimize for scannability, subject lines, or a more enticing value-first CTA.
   - Render a plain-text draft with:
     - `scripts/render_outreach_email.py --input <json> --output <txt>`
   - Render lightweight HTML with:
     - `scripts/render_outreach_email_html.py --input <json> --output <html>`
   - Preferred showcase send mode: **HTML email + attached brief**.
   - Keep email short, specific, and visually scannable.
   - Default to draft-only.

6. **Approval gate**
   - Do not send email automatically.
   - Sending is allowed only after explicit user approval for that recipient/message.
   - Build a preview manifest with:
     - `scripts/render_outreach_preview.py --input <json> --subject <subject> --email-text <txt> --email-html <html> --brief <brief.html> --output <preview.json>`
   - Before send, preview or summarize:
     - recipient
     - subject
     - plain-text fallback body
     - HTML body when used
     - attached brief filename/format when used
   - For actual HTML+brief send, use:
     - `scripts/send_outreach_package.sh --to <email> --subject <subject> --text <txt> --html <html> --attach <brief.pdf>`
   - Use a client-facing attachment name such as:
     - `<Business-Name>-OpenClaw-Brief.pdf`

## Output standard

Produce three artifacts when possible:
- structured JSON summary
- markdown report
- plain-text email draft

Recommended JSON fields:
- `business_name`
- `contact_name`
- `contact_email`
- `website_url`
- `business_summary`
- `likely_audience`
- `website_observations[]`
- `openclaw_fits[]` with:
  - `use_case`
  - `why_it_fits`
  - `likely_value`
  - `starting_point`
- `priority_move` with:
  - `move`
  - `why_first`
  - `expected_benefit`
- `why_it_matters[]`
- `demo_angle`
- `outreach_summary`

## Guardrails

- Research public website content only unless the user supplies additional material.
- Do not claim verified need where only a hypothesis exists.
- Do not overpromise outcomes.
- Do not send email without explicit approval.
- Use the configured sender account and sender identity for outbound workflows; do not hardcode personal branding into public distributions.

## Resources

### references/
- `references/report-format.md` — required report structure
- `references/email-template.md` — default email draft shape and constraints
- `references/value-first-outreach.md` — value-first / “free doughnut” outreach framing, scannability rules, and CTA guidance
- `references/visual-delivery.md` — HTML email + one-page brief delivery guidance and approval-preview checklist
- `references/follow-up-sequence.md` — optional follow-up templates and cadence after the initial brief send

### scripts/
- `scripts/render_outreach_report.py` — render markdown report from structured JSON
- `scripts/render_outreach_report_html.py` — render polished HTML one-page brief from structured JSON
- `scripts/render_outreach_report_pdf.sh` — convert the HTML brief into a client-facing PDF artifact
- `scripts/render_outreach_email.py` — render plain-text outreach email from structured JSON
- `scripts/render_outreach_email_html.py` — render lightweight HTML outreach email from structured JSON
- `scripts/render_outreach_preview.py` — render approval preview manifest for the actual outbound package
- `scripts/send_outreach_package.sh` — send HTML email plus attached brief via Gmail after approval
- `scripts/config.example.json` — example config with sender account and output defaults
