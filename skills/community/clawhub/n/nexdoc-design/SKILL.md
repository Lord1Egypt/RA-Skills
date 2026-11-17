---
name: nexdoc-design
description: >-
  Generate, iterate, preview, export, and publish production-ready designs
  (landing pages, slide decks, reports, invoices, resumes, business cards,
  social cards, email newsletters, and 30+ formats) with NexDoc Design.
  Use when the user wants a design, layout, deck, PDF, page, or card generated
  or edited. Prefer MCP tools when connected; otherwise call the REST API.
  Never publish unless asked.
homepage: https://nexdoc.design
metadata:
  openclaw:
    homepage: https://nexdoc.design
    envVars:
      - name: NXD_API_KEY
        required: false
        description: API key for REST/stdio paths (nxd_live_…). Not needed for remote MCP OAuth.
---

# NexDoc Design

NexDoc Design is a hosted design engine. You supply source copy, a design brief, and a format slug. NexDoc generates and validates the HTML/CSS and returns a preview URL. **Do not hand-write the final HTML.**

| Service | URL |
|---------|-----|
| REST API | `https://api.nexdoc.design` |
| MCP | `https://mcp.nexdoc.design/mcp` |
| Dashboard and API keys | `https://app.nexdoc.design` |

## Choose an integration

1. **MCP tools are available** (`create_design`, `update_design`, `wait_for_run`, `export_design`, and related tools) — follow the **nexdoc-mcp** skill.
2. **Otherwise** — call the REST API with `NXD_API_KEY` (`nxd_live_…` from `https://app.nexdoc.design/keys`). Follow the **nexdoc-api** skill (endpoint catalog in that skill’s `reference.md`).

If MCP is not connected and the user is in Claude, ChatGPT, Cursor, or another MCP client, offer to add the remote server `https://mcp.nexdoc.design/mcp` (**OAuth 2.1**, no API key). In ChatGPT / Cowork, if the installer asks for a key or offers Token vs OAuth, choose OAuth and do not collect a key. Desktop clients can instead run `npx -y @nexdoc/mcp-server` with `NXD_API_KEY`.

Never print an API key.

## Model

- **Job** — one design and its history. Reuse the same `job_id` for every edit. Never create a second job for the same request.
- **Run** — one generation on a job. Needed to poll, cancel, notify, export, or publish that version.

Run states: `queued` → `preparing` → `running` → `validating` → `uploading_outputs` → `completed` | `failed` | `cancelled`.

## Persist IDs

Save **`job_id` and `run_id` as soon as a run is created**, before waiting or talking to the user. Repeat both IDs after create and after every later step. If a poll or tool times out, resume the **same** run. Never start a duplicate.

## How long generation takes

Tell the user the wait up front so they do not think the request hung.

| Kind of work | Typical wait |
|--------------|--------------|
| Simple card, one-page layout, short landing page | **1–5 minutes** |
| Pitch deck, multi-page report, image-heavy or tightly branded work | **10–20 minutes**, sometimes longer |

Complex formats (`report`, `proposal`, `whitepaper`, `slide-deck`, `pitch-deck`, `lookbook`) take the longest. If you cannot wait, request email notification and keep the IDs.

## Operating rules

1. Always return `viewer_url` after a completed run (humans preview and click-to-edit text). Preview links last 24 hours; remint anytime. The design is not gone when a link expires.
2. Offer a download: `pdf` for print, slides, cards, resumes, invoices; `html` (ZIP) for `landing-page`, `portfolio`, `link-in-bio`, `email-newsletter`, `dashboard`; `png` (ZIP of PNGs) when they want images.
3. Publish to a public URL **only** when the user explicitly asks (“publish”, “make it public”, “live link”).
4. On `402`, send the user to `https://app.nexdoc.design` (minimum top-up $10). Do not retry in a loop and do not work around billing.
5. Failed runs are not charged. Show `error` and `log_tail`, fix the inputs, and retry **once** on the **same** `job_id` (`update_design` / new run). Never create a second job for the same request.

## Writing `content` and `instructions`

**`content`** — facts in clean markdown: headings, lists, tables, real names, numbers, dates, prices. Keep everything the user supplied; invent nothing. NexDoc re-authors for the medium. Reference uploaded images by filename: `![Logo](logo.png)`.

**`instructions`** — the design brief (create) or a **diff** (update):

- Audience and purpose
- Aesthetic direction (specific mood, palette, type — not “modern and professional”)
- Brand tokens inline, treated as authoritative: `Brand: primary #2563EB, accent #F59E0B, fonts Inter; logo.png in nav.`
- Structure constraints and must-haves (CTA, contact, legal, page counts)
- Slide decks: 1280×720 stages sized in `%` (never `vw`/`vh`); readable content ≥48px from edges; inspect the exported PDF for clipped type

On updates, leave `content` empty unless copy changes. Keep the same `format` unless the user wants a different medium.

## Allowed uploads

`.png`, `.jpg`/`.jpeg`, `.gif`, `.pdf` only. SVG, WebP, JSON, and brand-kit files are rejected (`400`). Put colors and fonts in `instructions`.

## Formats

| Need | Slug |
|------|------|
| Marketing / product page | `landing-page` |
| Personal site, links hub | `portfolio`, `link-in-bio` |
| Slides | `pitch-deck`, `slide-deck` |
| Long print document | `report`, `proposal`, `whitepaper`, `case-study` |
| Flyer / A4 poster | `poster`, `brochure` |
| Business paperwork | `invoice`, `receipt`, `contract`, `nda` |
| Career | `resume` / `cv`, `cover-letter` |
| Single image / card | `business-card`, `social-card`, `og-image`, `banner` |
| Events | `invitation`, `ticket`, `certificate`, `menu` |
| Email | `email-newsletter` |
| Data / structure | `infographic`, `dashboard`, `timeline`, `roadmap`, `org-chart` |

All 37 slugs: `landing-page` `link-in-bio` `portfolio` `lookbook` `slide-deck` `presentation` `pitch-deck` `invoice` `receipt` `resume` `cv` `cover-letter` `proposal` `case-study` `report` `contract` `nda` `certificate` `whitepaper` `brochure` `menu` `social-card` `og-image` `banner` `business-card` `poster` `ticket` `boarding-pass` `coupon` `voucher` `invitation` `email-newsletter` `infographic` `timeline` `roadmap` `org-chart` `dashboard`.

## Report to the user

After every run (and again after export or publish): **`viewer_url`**, **`job_id`**, **`run_id`**, `status`, `charge_usd`. After export: `download_url`. After a *requested* publish: `public_url`. Never fabricate URLs. Previews expire; IDs do not.
