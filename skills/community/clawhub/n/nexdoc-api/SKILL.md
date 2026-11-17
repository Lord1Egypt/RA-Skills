---
name: nexdoc-api
description: >-
  Generate, iterate, preview, export, and publish production-ready designs
  (landing pages, slide decks, reports, invoices, resumes, business cards,
  social cards, email newsletters, and 30+ formats) by calling the NexDoc
  Design REST API with an NXD_API_KEY — from curl, Python, Node, a backend,
  CI, or a custom agent. Use when the user wants a design generated
  programmatically and no NexDoc MCP tools are connected. Never publish
  unless asked.
homepage: https://nexdoc.design
metadata:
  openclaw:
    homepage: https://nexdoc.design
    primaryEnv: NXD_API_KEY
    requires:
      env:
        - NXD_API_KEY
      bins:
        - curl
      anyBins:
        - jq
    envVars:
      - name: NXD_API_KEY
        required: true
        description: API key from https://app.nexdoc.design/keys (nxd_live_…).
---

# NexDoc Design via REST API

You are a client of the NexDoc Design engine. Send content, instructions, and a format slug; NexDoc generates and validates the HTML/CSS and returns a preview URL. **Do not hand-write the final HTML.**

```bash
API="https://api.nexdoc.design"
AUTH="Authorization: Bearer $NXD_API_KEY"   # nxd_live_… from https://app.nexdoc.design/keys
```

If `NXD_API_KEY` is missing, send the user to `https://app.nexdoc.design/keys`. Never print a key.

Prefer the **nexdoc-mcp** skill when NexDoc MCP tools are connected. Full endpoint catalog: [reference.md](reference.md).

## Model

**Job** = one design, with history. **Run** = one generation on a job (the first run creates; later runs edit). Every completed run has a `commit_hash`, a `viewer_url`, and a `charge_usd`.

Run states: `queued` → `preparing` → `running` → `validating` → `uploading_outputs` → `completed` | `failed` | `cancelled`.

## Persist IDs

**Save `job_id` and `run_id` as soon as `POST …/runs` returns** — before polling, before timeouts, before talking to the user. Keep them in your notes and **repeat both IDs** after create and after every later call. They are the only way to resume, edit, export, or request email later.

- `job_id` — the design. Reuse it for all edits. Never create a second job for the same request.
- `run_id` — this generation. Needed to poll, cancel, notify, export, or publish that version.
- If a poll times out, you still have the IDs: poll the same run or `POST …/notify-email`. Never start a duplicate run.

## How long generation takes

Tell the user the wait up front so they do not think the request hung.

| Kind of work | Typical wait |
|--------------|--------------|
| Simple card, one-page layout, short landing page | **1–5 minutes** |
| Pitch deck, multi-page report, image-heavy or tightly branded work | **10–20 minutes**, sometimes longer |

Complex formats (`report`, `proposal`, `whitepaper`, `slide-deck`, `pitch-deck`, `lookbook`) take the longest. Plan to wait, or set `notify_email: true` and return with the saved IDs.

## Create

```bash
# 1) Job
JOB=$(curl -sS -X POST "$API/v1/jobs" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name":"Loop pitch deck"}' | jq -r .job_id)

# 2) Run — multipart when you have files (content.md, logos, photos, PDFs)
RUN_ID=$(curl -sS -X POST "$API/v1/jobs/$JOB/runs" -H "$AUTH" \
  -F "format=pitch-deck" \
  -F "instructions=Seed-round pitch for logistics investors. 10-12 slides, one idea per slide. Dark navy, electric-green accent #22C55E, Inter. Use logo.png on the title slide." \
  -F "content=@./content.md;type=text/markdown;filename=content.md" \
  -F "files=@./logo.png;type=image/png;filename=logo.png" | jq -r .run_id)

# 2b) JSON when everything is inline
curl -sS -X POST "$API/v1/jobs/$JOB/runs" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"format":"landing-page","instructions":"Dark editorial. Hero + 3 features + pricing + FAQ.","content":"# Acme\n\nAPI-first design for product teams.\n\n- Fast\n- Brand-aware\n- Export to PDF/HTML"}'
```

`POST …/runs` returns **202** `{job_id, run_id, status:"queued", notify_email}`. **Record both IDs immediately** and show them to the user.

## Wait for completion

**Polling** works when the client can wait 1–20 minutes. **Email notification** is the better fit when tool timeouts would cut you off — NexDoc emails the account address on the API key.

```bash
# On create
curl -sS -X POST "$API/v1/jobs/$JOB/runs" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"format":"landing-page","instructions":"…","content":"…","notify_email":true}'

# After a run has already started
curl -sS -X POST "$API/v1/jobs/$JOB/runs/$RUN_ID/notify-email" -H "$AUTH"
```

If `POST …/notify-email` returns `sent: true`, the email went out (or was already sent). If it returns `warning` with `sent: false` on a terminal run, mail failed — fetch the run and report `status` / `viewer_url` / `error`.

Poll when you can hold the connection:

```bash
for i in $(seq 1 240); do                       # 240 × 5 s = 20 min
  R=$(curl -sS "$API/v1/jobs/$JOB/runs/$RUN_ID" -H "$AUTH")
  S=$(echo "$R" | jq -r .status)
  case "$S" in completed|failed|cancelled) break;; esac
  sleep 5
done
echo "$R" | jq '{status, charge_usd, viewer_url, error, log_tail}'
```

Do not treat a long wait as a failure. `webhook_url` is accepted on the run body but delivery is not guaranteed — do not block on a callback. Prefer `notify_email` or polling, and always keep the IDs.

## Deliver

1. **Always** return `viewer_url` (preview and click-to-edit text). Links last 24 hours; remint anytime with `GET /v1/jobs/$JOB/viewer/session`. The design is never “gone”.
2. **Download** when a file is wanted:

```bash
curl -sS -X POST "$API/v1/jobs/$JOB/export" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"format\":\"pdf\",\"run_id\":\"$RUN_ID\"}" | jq -r .download_url     # or "html" / "png" → ZIP
```

   `pdf` for print, slides, cards, resumes, invoices. `html` for `landing-page`, `portfolio`, `link-in-bio`, `email-newsletter`, `dashboard`. `png` for a ZIP of PNG images (one per sheet/slide/artboard). `download_url` expires in about one hour.

3. **Publish only on explicit request** (“publish”, “make it public”, “live link”):

```bash
curl -sS -X POST "$API/v1/jobs/$JOB/publish" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"run_id\":\"$RUN_ID\"}" | jq -r .public_url          # undo: POST …/unpublish
```

## Update (same job)

```bash
curl -sS -X POST "$API/v1/jobs/$JOB/runs" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"format":"pitch-deck","instructions":"Tighten slide 3 to three bullets; make the closing CTA green. Keep everything else.","content":""}'
```

Instructions are a **diff**. Leave `content` empty unless copy changes. Keep the same `format` unless the user wants a different medium. New assets: multipart `files` or `file_ids` as in [reference.md](reference.md#files).

## Allowed uploads

These types are accepted on multipart `files` and `POST /v1/files/request-upload`. Originals are stored; the worker converts them before the design agent runs.

| Kind | Extensions | `content_type` | Agent sees |
|------|------------|----------------|------------|
| Image | `.png` | `image/png` | as-is |
| Image | `.jpg` / `.jpeg` | `image/jpeg` | as-is |
| Image | `.gif` | `image/gif` | as-is |
| Image | `.webp` | `image/webp` | PNG |
| Image | `.heic` / `.heif` | `image/heic` / `image/heif` | PNG |
| Image | `.svg` | `image/svg+xml` | PNG |
| Document | `.pdf` | `application/pdf` | page PNGs + extracted text |
| Text | `.md` / `.txt` / `.csv` / `.json` | `text/markdown`, `text/plain`, `text/csv`, `application/json` | inlined into `content.md` (brand-kit JSON → `brand-kit.json`) |

Office formats (`.docx`, `.pptx`, …) return **400**. You may also put brand colors and fonts in `instructions`.

## Writing `content` and `instructions`

**`content`** — the facts in clean markdown: headings, lists, tables, real names, numbers, dates, prices. Keep everything the user gave; invent nothing. NexDoc re-authors for the medium, so supply substance, not layout. Reference uploaded images by filename: `![Logo](logo.png)`.

**`instructions`** — the design brief, one paragraph or bullets:

- **Audience and purpose** — “Series A investors”, “walk-in menu”, “internal Q3 review”
- **Aesthetic direction** — specific mood, palette, type (“dark editorial, warm serif headlines, generous whitespace”). Avoid “modern and professional”.
- **Brand tokens** inline — `Brand: primary #2563EB, accent #F59E0B, fonts Inter; logo.png in nav.` Stated colors and fonts are authoritative.
- **Structure** — “hero + 3 features + pricing + FAQ + footer”, “≤ 12 slides”, “single A4 page”
- **Must-haves** — CTA text, contact block, legal line, page numbers
- **Slide decks** — the downloadable PDF is the native print export. Instruct: `%` of the 1280×720 stage (never `vw`/`vh`); ≥48px inset for type, labels, and footers; inspect the exported PDF for edge clipping.

## Format selection

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

## Errors

| Code / state | Action |
|--------------|--------|
| `402` | Wallet empty or past due. `GET /v1/credits` → send the user to `https://app.nexdoc.design` (minimum $10). No retry loops, no workarounds. |
| `concurrency_notice` | Pay-as-you-go: one run at a time. Show the notice; Pro is $20/mo for 5 concurrent. Do not open a second job to bypass the queue. |
| `401` | Missing or invalid `NXD_API_KEY`. Direct the user to `https://app.nexdoc.design/keys`. |
| `400` | Read `detail` — usually an unsupported upload type or a malformed field. |
| `404` | Wrong `job_id` / `run_id` / `file_id`, or it belongs to another organization. |
| `409` | Cancel on a finished run. |
| `503` | Queue unavailable; retry once after 10 seconds on the **same** `job_id` (create a run on the existing job). Do not `POST /v1/jobs` again. |
| Run `failed` | Show `error` + `log_tail`; fix inputs; retry **once** as a new run on the **same** `job_id`. Never create a second job for the same request. Failed runs are not charged. |

## Report to the user

After every run (and again after export or publish): **`viewer_url`**, **`job_id`**, **`run_id`**, `status`, `charge_usd`. After export: `download_url`. After a *requested* publish: `public_url`. Never fabricate URLs. Always persist and restate `job_id` and `run_id` — previews expire, IDs do not.
