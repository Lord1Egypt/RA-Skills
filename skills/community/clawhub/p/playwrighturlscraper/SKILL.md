---
name: render-url
description: Render a URL in headless Chromium and extract structured JSON (title, headings, links, images, meta, text) from the rendered page. Use this whenever the task needs the post-JavaScript content of a web page — SPAs, JS-rendered content, or any page where a plain HTTP fetch would miss content added by client-side JS. Installs the `render-url` CLI from PyPI on first use. Core extraction is deterministic DOM parsing, no LLM/AI involved; an optional `--answer-questions` flag can use an LLM to answer application questions found on the page from a resume.
---

# render-url

A two-stage, deterministic CLI toolchain: render a URL in real Chromium (via Playwright), then extract structured data from the rendered HTML. No crawling, no LLM/AI-based interpretation in the core pipeline — pure browser rendering + structural DOM parsing. An optional, off-by-default `--answer-questions` flag adds LLM-based application-question answering (see below).

## Setup

Install the CLI from PyPI and the Chromium browser it drives. Do this once per environment; skip if `render-url --help` already succeeds.

```bash
pip install render-url
playwright install chromium
```

Only if you'll use `--answer-questions` (optional, LLM-based — see below):

```bash
pip install "render-url[qa]"   # adds the anthropic SDK
```

## Commands

### One-shot: render + extract in a single call (preferred for most tasks)

```bash
render-and-parse "https://example.com"
```

Prints one JSON object to stdout with the extracted structured data (title, headings, links, images, meta, text). Also writes `rendered_page_N.json` (raw render) and `parsed_page_N.json` (extracted data) to the current directory.

Useful flags:
- `--selector "<css>"` — scope extraction to one element (e.g. `--selector "article"`, `--selector "#main-content"`).
- `--timeout <ms>` — navigation timeout (default 30000).
- `--wait-until networkidle` — wait for network idle instead of the default `load` (use only if the page is known to settle onto a quiet network; SPAs with polling/websockets may hang).
- `--no-strip-whitespace` — preserve raw whitespace in extracted text instead of collapsing it.
- `--verbose` — log each pipeline step to stderr.
- `--log-json` — pretty-print the full result JSON to stderr as well.
- `--detect` — run deterministic page classification (see below) before rendering. Useful for job-application URLs, where the page may turn out to be a CAPTCHA, login wall, error page, closed job, or bot/security challenge instead of the actual application. If the page classifies as anything other than `APPLICATION`, parsing is skipped and the classification is returned instead of extracted page data.
- `--answer-questions` — after parsing, use an LLM to identify application/screening questions in the extracted text and answer them from a resume (see below). Off by default; the only flag in this toolchain that calls an LLM or makes network calls beyond rendering the page. **Requires `--detect` also be passed** — `render-and-parse` rejects `--answer-questions` on its own with an `invalid_input` error, before rendering anything.

### Application detection (`--detect`)

Runs entirely deterministic checks (no LLM/AI) against the rendered DOM and HTTP status: CAPTCHA, bot/security challenge (with a short navigate → wait → inspect → wait → inspect retry loop), login wall, HTTP/rendered error, closed/expired job, then an application-form evidence score. Output gains these fields:

```json
{
  "status": "APPLICATION",
  "reason": "application_form_detected",
  "detector": {
    "captcha": false,
    "login": false,
    "bot_challenge": false,
    "error": false,
    "closed_job": false,
    "form_detected": true
  },
  "form": {"count": 1, "inputs": 17, "textareas": 2, "selects": 3, "file_inputs": 1},
  "redirected": true
}
```

`status` is one of `APPLICATION`, `CAPTCHA`, `LOGIN`, `ERROR`, `CLOSED_JOB`, `BOT_CHALLENGE`, `NO_FORM`. When `status` is anything other than `APPLICATION`, `html`/`data` come back `null` — the page was never worth fully parsing. Thresholds, keyword lists, and challenge-wait timing are configurable via the `"detector"` section of `config.json` (see `config.example.json`).

### Answering application questions with an LLM (`--answer-questions`, optional)

The only LLM-calling feature in this toolchain — off by default, and everything above still works without it. When enabled, after parsing it sends the extracted page text to an LLM (Anthropic Claude by default) to identify the application/screening questions on the page and answer each one from a resume.

**Always pass `--detect` together with `--answer-questions`.** The LLM only ever runs on a page `--detect` classified `APPLICATION` — this keeps it from being called (and spending API credits) on a CAPTCHA, login wall, closed job, or bot-challenge page. `render-and-parse --answer-questions` without `--detect` fails immediately with an `invalid_input` error, before Chromium even launches.

```bash
cp .env.example .env     # fill in ANTHROPIC_API_KEY
# write the candidate's resume as Markdown to resume.md (gitignored, never commit it)
render-and-parse "https://example.com/job/123" --detect --answer-questions
```

Flags: `--resume <path>` (default `resume.md`), `--qa-provider` (default/only `anthropic`), `--qa-model` (short name like `sonnet5`, `opus5`, or a full model ID; default `sonnet5`), `--qa-api-key` (falls back to `ANTHROPIC_API_KEY` env/`.env`). Also settable via `"answer_questions"`/`"resume_path"`/`"qa_provider"`/`"qa_model"` in the `"parser"` section of `config.json`.

On success (page classified `APPLICATION`), `data` gains:

```json
{
  "application_questions": ["Are you legally authorized to work in Canada?"],
  "answers": [
    {"question": "Are you legally authorized to work in Canada?", "answer": "Yes."}
  ]
}
```

If the resume can't answer a question confidently, `"answer"` is `null` rather than a guess. If the page wasn't classified `APPLICATION`, or QA fails for any other reason (missing resume, missing API key, LLM error), the deterministic parse result is still returned, with a top-level `"qa_error"` string instead — the gate and any QA failure both leave the parse itself untouched. (Using the two-stage `render-url --detect` → `parse-html --answer-questions` pipeline instead of `render-and-parse`? The same rule applies: `parse-html` reads the `"status"` field `render-url --detect` wrote into its input file, and skips the LLM call the same way if it's missing or not `APPLICATION`.)

### Two-stage: render and parse separately (when you need the raw HTML too)

```bash
render-url "https://example.com"              # -> rendered_page_1.json (includes raw "html" field)
parse-html rendered_page_1.json                # -> parsed_page_1.json (structured extraction)

# or piped, no intermediate file needed:
render-url "https://example.com" | parse-html -
```

`render-url` alone is useful when you need the raw post-JS HTML itself (e.g. to feed a different extraction step), not just the structured fields `parse-html` produces.

### Raw HTML output (`render-url --raw-html`)

Use this when you need the page's rendered HTML itself (clean, pretty-printed `<body>` markup with no scripts or CSS) — to grep it, feed it to your own extraction, or inspect markup the structured parse drops — and don't want to unwrap it from JSON.

```bash
render-url "https://example.com" --raw-html --no-detect > page.html
```

Default recipe: **use `--raw-html --no-detect` together** unless you specifically want the page classified. (`--no-detect` matters because a project `config.json` may set `"detect": true`, which would otherwise turn a plain job-listing page into a `NO_FORM` JSON result.)

Exactly how to use it:
- Pass `--raw-html` to **`render-url`** only (not `render-and-parse` or `parse-html`, which don't accept it). Every other `render-url` flag (`--timeout`, `--wait-until`, `--stabilization`, `--detect`, `--output-dir`, ...) still works alongside it.
- On success, **stdout is the post-JS `<body>` markup and nothing else** — HTML only: no `<head>`, no `<script>`/`<style>`/`<link>`/`<noscript>`/`<template>` elements, and no inline `style`/`on*` attributes. The markup is pretty-printed (one tag per line, indented). Because `<head>` is dropped, `<title>`, meta tags and JSON-LD data are not in this output; use `render-and-parse` (or `render-url` without `--raw-html`) if you need them. It is also saved to `<output-prefix>_N.html` (default `rendered_page_N.html`, auto-incremented). Redirect stdout to a file or read the saved file; don't try to `json.loads` it.
- **Always check what you got.** If no HTML could be produced, stdout is the normal JSON result instead (`{"ok": false, "error": {...}}`, or with `--detect`, a `status` other than `APPLICATION` and `"html": null`), and the saved file is `.json` rather than `.html`. Treat output beginning with `{"ok":` as the failure/classification case and read `error` or `status`/`reason`. Real HTML begins with `<`.
- If the HTML looks like an empty shell for a JS-heavy page, re-run with a larger `--stabilization` (e.g. `3000`) or `--wait-until networkidle`.
- Don't combine with `--detect` unless you want the page gated: with `--detect` (or `"detect": true` in `config.json`), any non-`APPLICATION` page returns JSON, not HTML. If `config.json` enables detect and you need HTML regardless (e.g. a plain job listing page classifies as `NO_FORM`), pass `--no-detect`.
- Clean up the auto-incremented `.html` files when done.

## Output schema (parse-html / render-and-parse)

```json
{
  "ok": true,
  "source_url": "https://example.com",
  "title": "Example Domain",
  "data": {
    "headings": [{"level": 1, "text": "Example Domain"}],
    "links": [{"text": "More information...", "href": "https://iana.org/domains/example"}],
    "images": [{"src": "...", "alt": "..."}],
    "meta": {"viewport": "width=device-width, initial-scale=1"},
    "text": "Example Domain This domain is for use in illustrative examples..."
  },
  "selector_matched": null,
  "error": null
}
```

On failure: `ok: false` and `error: {"type": "...", "message": "..."}`. Error types include `invalid_url`, `navigation_timeout`, `navigation_error`, `missing_html`, `invalid_config`, `parse_error`. Always check `ok` before reading `data`.

## Notes

- Exactly one URL per invocation — no crawling or link-following. To process multiple URLs, call the command once per URL.
- Output files (`rendered_page_N.json`, `parsed_page_N.json`, or `rendered_page_N.html` with `--raw-html`) auto-increment and never overwrite existing files in the working directory — clean these up if not needed after use.
- All output is a single JSON object on stdout (except `render-url --raw-html`, which prints pretty-printed body-only HTML on success); diagnostics only ever go to stderr, so stdout is always safe to parse directly.
- `--answer-questions` is the sole exception to "no LLM/AI" above — it's opt-in and every other command/flag remains deterministic and offline.
