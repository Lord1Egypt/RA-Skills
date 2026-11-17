---
name: nexdoc-mcp
description: >-
  Generate, iterate, preview, and export production-ready designs (landing
  pages, slide decks, reports, invoices, resumes, business cards, social cards,
  email newsletters, and 30+ formats) through the NexDoc Design MCP tools
  (create_design, update_design, wait_for_run, notify_run_email, export_design).
  Use whenever the user asks to design, lay out, make a deck, PDF, page, or
  card, or to edit an existing NexDoc design, and MCP tools are available.
  Never publish unless asked.
homepage: https://nexdoc.design
metadata:
  openclaw:
    homepage: https://nexdoc.design
    requires:
      anyBins:
        - npx
    envVars:
      - name: NXD_API_KEY
        required: false
        description: Required only for stdio MCP (npx @nexdoc/mcp-server). Remote MCP uses OAuth instead.
---

# NexDoc Design via MCP

You are a client of the NexDoc Design engine. Write clean source copy and a clear design brief; NexDoc generates the HTML/CSS, validates it, and returns a preview URL. **Do not hand-write the final HTML.**

## Connect (once)

If NexDoc tools (`create_design`, `export_design`, and related tools) are already available, skip this section.

**Remote MCP (recommended for Claude, ChatGPT, Cursor, and other remote-MCP clients).** Add a remote MCP server named `nexdoc` at:

```
https://mcp.nexdoc.design/mcp
```

The client opens a browser for OAuth 2.1. **Never ask the user for an API key** on this path. In ChatGPT / Cowork, if the installer offers Token vs OAuth, choose OAuth.

**stdio MCP (desktop clients with an API key).** Cursor, Claude Desktop, and Claude Code can run the published server as a process:

```json
{
  "mcpServers": {
    "nexdoc": {
      "command": "npx",
      "args": ["-y", "@nexdoc/mcp-server"],
      "env": {
        "NXD_API_KEY": "nxd_live_..."
      }
    }
  }
}
```

Create a key at `https://app.nexdoc.design/keys`. Never print or echo a key.

## Tools

| Tool | When to use |
|------|-------------|
| `create_design` | First design for a request. Creates a job and starts a run. **Do not** pass `wait: true`. Immediately tell the user `job_id` and `run_id`. Omitting `job_id` always creates a **new** job — call at most once per request. Photos: pass `file_ids` after upload. |
| `update_design` | Any change to an existing design (`job_id`). Instructions are a **diff**. New photos: `file_ids` (preferred) or `asset_paths` (stdio). Same wait policy as create. Also use this (or `create_design` **with** `job_id`) to retry a failed run — never a bare second `create_design`. |
| `request_file_upload` | Mint a presigned URL. **Preferred for photos.** PUT original bytes to `upload_url`, then `check_file`. Do not base64 or compress. |
| `check_file` | Confirm `file_id` status is `ready` before starting a run. |
| `upload_file` | stdio only: read a local path and upload; returns a ready `file_id`. |
| `wait_for_run` | **One short poll** after create/update (default ~45 s, max 90 s). If `still_running`, **stop** — do not call again unless the user asks to keep waiting. |
| `notify_run_email` | Email the account owner when the run finishes. If they asked to be emailed (including in the original request), set `notify_email: true` on create **or** call this immediately. Safe after the run is terminal: sends now if not already sent. |
| `check_run` | One-shot status; also mints a fresh `viewer_url`. |
| `refresh_preview` | The preview link expired or returns 401. |
| `export_design` | The user wants a file: `pdf`, `html` (ZIP of the site), or `png` (ZIP of PNG pages/slides/artboards). Returns `download_url` (valid ~1 hour). |
| `publish_design` | **Only** when the user explicitly says publish, make public, or live link. |
| `unpublish_design` | The user asks to take a published design down. |
| `list_runs` | Compare versions of a job. |
| `list_formats` | You are unsure which format slug fits. |
| `get_balance` | A tool failed with `API 402`, or the user asks about cost or balance. |

## Persist IDs

**Save `job_id` and `run_id` as soon as a run is created** — before waiting, before timeouts, before talking to the user. Store them in conversation state and **repeat both IDs** after create and after every later step. They are the only way to resume, edit, export, or request email later.

- `job_id` — the design. Reuse it for all edits. Never create a second job for the same request.
- `run_id` — this generation. Required for `wait_for_run`, `check_run`, `notify_run_email`, and a specific export or publish.
- If a tool times out, use the **same** pair. Never start a duplicate run. Do not loop `wait_for_run`; offer email instead.
- If `create_design` errors after a `job_id=` appears in the message, that job already exists — retry with that `job_id` or `update_design`. Do **not** call `create_design` again without `job_id` (that creates a twin job with the same name).

## How long generation takes

Tell the user the wait up front so they do not think the tool hung.

| Kind of work | Typical wait |
|--------------|--------------|
| Simple card, one-page layout, short landing page | **1–5 minutes** |
| Pitch deck, multi-page report, image-heavy or tightly branded work | **10–20 minutes**, sometimes longer |

Complex formats (`report`, `proposal`, `whitepaper`, `slide-deck`, `pitch-deck`, `lookbook`) take the longest. Do **not** poll in a loop — that blocks the conversation and usually times out anyway.

**Wait policy**

1. After `create_design` / `update_design`, call `wait_for_run` **once**.
2. If the run is terminal, report `viewer_url` as usual.
3. If the result has `still_running: true`, **stop polling**. Tell the user the `job_id` and `run_id`, that designs can take several minutes. If they already asked to be emailed, `notify_email` should already have been `true` on create. Otherwise offer: *I can email you at your NexDoc account when it is ready so you can keep working.* Call `notify_run_email` when they say yes. If they asked to be emailed at the start, set `notify_email: true` on create immediately — do not wait until after `wait_for_run`.
4. Call `wait_for_run` again only if they explicitly ask to keep waiting. Never raise `timeout_sec` to “wait it out.”

If `notify_run_email` returns `sent: true`, the email went out (or was already sent). If it returns a `warning` with `sent: false`, the run is terminal but mail failed — call `check_run` and report the result.

## Workflow

```
1. Pick a format slug            → table below (call list_formats only if unsure)
2. Write content + instructions  → guidance below
3. create_design { format, instructions, content, name [, notify_email:true if they asked] }  — no wait
4. Immediately save and tell the user job_id + run_id
5. wait_for_run { job_id, run_id }  — once only
6. If still_running: stop. Offer email unless they already asked (then notify_email should already be true). Do **not** share a previous viewer_url.
   If terminal: report **this run's** viewer_url, job_id, run_id, charge_usd
7. Offer export_design (pdf | html | png). Publish ONLY on explicit request.
8. Edits: update_design { job_id, format, instructions [, file_ids] } — same job, same format.
   New photos/logos **must** be uploaded first (request_file_upload + PUT, or upload_file), then referenced. Then wait_for_run on the **new** run_id. The previous preview is the old design.
```

### Assets (logos, photos, PDFs, docs)

**Accepted:** `.png`, `.jpg`/`.jpeg`, `.gif`, `.webp`, `.heic`/`.heif`, `.svg`, `.pdf`, `.md`, `.txt`, `.csv`, `.json`. The worker converts exotic images and PDFs to PNG (and inlines text docs) before the design agent runs. Office formats (`.docx`, `.pptx`) are rejected with `400`. Brand colors/fonts may also go in `instructions`.

**Preferred (any size, especially photos):** upload first, then reference — never base64 a large image into a tool call, and never compress or generate a replacement.

1. `request_file_upload { filename, content_type, size_bytes }`
2. PUT the **original** file bytes to `upload_url` (`curl --data-binary @file -H "Content-Type: …"`). Same Content-Type as step 1. Do not base64.
3. `check_file { file_id }` until `status` is `ready`
4. `create_design` / `update_design` with `file_ids: ["file_…"]` and instructions that name the file (e.g. “use the uploaded headshot in the hero”).

- **stdio MCP shortcut:** `upload_file { path }` does steps 1–3, then pass `file_ids`. Small local files may still use `asset_paths` on the design call.
- **Remote MCP:** the server cannot read `/mnt/user-data/uploads/…`. Use the PUT flow above. `asset_files` (base64) is a last resort for tiny icons only.
- If a tool error says the file is not ready (`409`) or a path cannot be read, retry the **same** job with `file_ids` after a successful PUT — never start a second job. Do not paste base64 into `content`.

## Writing `content` and `instructions`

**`content`** — the facts, in clean markdown. Headings, lists, tables, real names, numbers, dates, prices. Preserve everything factual from the user; invent nothing. NexDoc re-authors for the medium (condenses prose into slides, expands bullets into landing-page sections, maps prose into invoice fields), so give substance, not layout.

**`instructions`** — the design brief. Cover, in one short paragraph or bullets:

- **Audience and purpose** — “Series A investors”, “restaurant walk-in menu”, “internal Q3 review”
- **Aesthetic direction** — mood, palette, typography (“dark editorial, warm serif headlines, generous whitespace”). Be specific; avoid “modern and professional”.
- **Brand tokens** — write them inline: `Brand: primary #2563EB, accent #F59E0B, fonts Inter; use logo.png in the nav.` Stated colors and fonts are authoritative.
- **Structure** — “one idea per slide, ≤ 12 slides”, “hero + 3 features + pricing + FAQ + footer”, “single page A4”
- **Must-haves** — CTA text, contact block, legal line, page numbers
- **Slide decks** (`slide-deck` / `pitch-deck` / `presentation`) — the downloadable PDF is the native print export, not the browser view. Require: 1280×720 stages sized with `%` (never `vw`/`vh`); readable content ≥48px from all edges; inspect the exported PDF for clipped labels and footers.

**Update instructions are a diff.** “Make the hero darker and swap the CTA to *Start free trial*; keep everything else.” Do not resend the whole brief. Omit `content` unless copy actually changes. Keep the same `format` unless the user wants a different medium.

### Example

User: *“Make me a pitch deck for Loop, a B2B returns-logistics startup. Here are our notes…”*

```json
create_design {
  "name": "Loop pitch deck",
  "format": "pitch-deck",
  "instructions": "Seed-round pitch for logistics and e-commerce investors. 10–12 slides, one idea per slide, terse headlines, big numbers as callouts. Dark navy background, electric-green accent (#22C55E), Inter. Closing slide with contact: hello@loop.example.",
  "content": "# Loop\n\n## Problem\nReturns cost US retailers $743B in 2023...\n\n## Traction\n- 42 merchants\n- $1.2M ARR, +18% MoM\n..."
}
```

Tell the user `job_id` and `run_id` immediately, then `wait_for_run` once. If it is still running, offer email rather than polling again. A deck like this often takes 10–20 minutes. When complete, report `viewer_url` and offer `export_design { format: "pdf" }`.

## Format selection

| Need | Slug |
|------|------|
| Marketing / product page | `landing-page` |
| Personal site, links hub | `portfolio`, `link-in-bio` |
| Slides | `pitch-deck` (investor/sales), `slide-deck` (general) |
| Long print document | `report`, `proposal`, `whitepaper`, `case-study` |
| Flyer / A4 poster | `poster`, `brochure` |
| Business paperwork | `invoice`, `receipt`, `contract`, `nda` |
| Career | `resume` / `cv`, `cover-letter` |
| Single image / card | `business-card`, `social-card`, `og-image`, `banner` |
| Events | `invitation`, `ticket`, `certificate`, `menu` |
| Email | `email-newsletter` |
| Data / structure | `infographic`, `dashboard`, `timeline`, `roadmap`, `org-chart` |

Export: `pdf` for print, slides, cards, certificates, resumes, invoices. `html` for `landing-page`, `portfolio`, `link-in-bio`, `email-newsletter`, `dashboard`. `png` when the user wants images (ZIP of PNGs).

## Errors

| Signal | Action |
|--------|--------|
| `API 402` | Call `get_balance`, then send the user to `https://app.nexdoc.design` (minimum $10). Do not retry in a loop. |
| `concurrency_notice` | Pay-as-you-go accounts run **one design at a time**. Show the reminder and offer Pro ($20/mo, 5 concurrent). Do not start a second job to work around the queue. |
| `API 401` | Reconnect the MCP server (OAuth) or replace `NXD_API_KEY`. |
| Run `failed` | Read `error` and `log_tail`; fix the input; retry **once** via `update_design` (or `create_design` **with** the same `job_id`). Never omit `job_id` on retry — that creates a duplicate job. Failed runs are not charged. |
| `API 409` on cancel | The run already finished. |
| Preview link expired | `check_run` or `refresh_preview`; the design is not gone. |
| `still_running` or tool timeout | Use the saved `job_id` / `run_id`. Do **not** call `wait_for_run` again. Offer `notify_run_email` if they have not already asked. Never call `create_design` again without `job_id`. |

## Report to the user

After create (even while still generating): **`job_id`** and **`run_id`**. Do not invent or reuse a `viewer_url`. After a **completed** run (and again after export or publish): **`viewer_url` from that run** (it includes `?run=`), **`job_id`**, **`run_id`**, `status`, `charge_usd`. After an edit, never paste the previous run's preview — wait until the new run is `completed` and use its `viewer_url`. After export: `download_url`. After a *requested* publish: `public_url`. Never invent URLs. Always persist and restate `job_id` and `run_id` — previews expire, IDs do not.
