---
name: md-to-linkedin
description: >
  Convert a Markdown article into rich text for LinkedIn's article editor,
  which has no Markdown and renders no tables. Headings, bold, italics, lists,
  quotes, links and fenced code become real HTML; tables become bullet lists,
  because the editor cannot draw one, or screenshot to PNG when the grid matters.
  Writes an HTML file beside the article for the browser copy path. Use when the user wants to publish a markdown draft as
  a LinkedIn article, asks for LinkedIn rich text, or needs the article editor
  formatting preserved.
---

# md-to-linkedin — Markdown into LinkedIn's article editor

LinkedIn's long-form editor has no Markdown mode. Paste raw Markdown and you get literal asterisks. Paste HTML and the editor applies its own formatting to what it recognises. This skill produces that HTML from your article, hands it to the clipboard, and writes a file for the browser fallback.

Policy: **preserve everything, degrade nothing by default.** Whether the editor keeps a pasted table or a code block is version-dependent and cannot be tested from outside it, so the converter emits the real thing and gives you a flag to flatten it only after a paste shows it was dropped.

## Run it

```sh
scripts/md2rich.py docs/261108-hermes-guest-hardening.md
```

Output:

```
html:    docs/261108-hermes-guest-hardening-linkedin.html
clipboard: rich text ready — paste into the article editor
```

The HTML lands **beside the article**, named `<article>-linkedin.html`, so the source and its LinkedIn rendering sit together. Both artefacts are gitignored (`*-linkedin.html`, `imgs/linkedin-tables/`) — they are regenerable, and only the Markdown belongs in history.

Then in the article editor: click into the body, `Ctrl+V`.

## What the editor can hold

| Construct | Result | Why |
|---|---|---|
| headings, paragraphs, bold, italic, lists, quotes, links | kept | native |
| fenced code | kept as `<pre>` | works; `--degrade-code` if a paste collapses it |
| tables | **bullet list**, or a **PNG** with `--tables image` | the editor has no table |
| images | placeholder + checklist | the clipboard cannot carry files |

A flattened table keeps every value; it loses the grid. When the grid *is* the point — a comparison, a matrix — screenshot the table and upload it as an image, because no amount of markup will make LinkedIn draw cells.

## Flags

| Flag | Effect |
|---|---|
| `--tables flatten` | default: each table becomes a bullet list |
| `--tables image` | screenshot each table to PNG, leave a placeholder to upload at |
| `--tables keep` | emit `<table>` markup, for a target that renders it |
| `--degrade-code` | flatten code blocks into quotes |
| `--docx` | also write a `.docx` via `soffice`, for pasting from Writer |
| `--out PATH` | write the HTML somewhere other than beside the article |
| `--image-dir PATH` | where table PNGs go (default `imgs/linkedin-tables/`) |
| `--print` | print the fragment to stdout instead of writing a file |
| `--no-clip` | do not touch the clipboard (for inspection only) |
| `--base URL` | base for relative links (default: the `j3ffyang` docs URL) |

The script declares its own dependencies inline, so `uv run` fetches `markdown` and `beautifulsoup4` per invocation. Nothing is installed, no venv is created, and the system Python is untouched.

## What travels

| Markdown | In the fragment |
|---|---|
| `#`–`####`, paragraphs, `**bold**`, `*italic*`, links, `- ` / `1.` lists | identical semantics |
| `> quote` | `<blockquote>` |
| tables | bullet list; `--keep-tables` emits `<table>` instead |
| fenced code | `<pre><code>` with newlines and indentation intact |
| inline `` `code` `` | `<code>` |
| `![alt](path)` | `[Image: alt]` placeholder plus an upload checklist entry |
| `---` | `<hr>` |

Relative links are rewritten to absolute `j3ffyang` URLs, so they still resolve after the article leaves the repo.

## Images are manual

The clipboard cannot carry files. Every image becomes a placeholder and a numbered line in the report:

```
images to upload by hand, in order:
  1. Three layers: control plane, capability, identity  (../imgs/261108-....png)
```

Upload each at its placeholder, then delete the placeholder line.

## Rules

- **Never edit the source article to suit LinkedIn.** Convert, and report what changed; the Markdown stays the source of truth.
- **Do not pre-emptively degrade.** Flatten only after a paste proves the editor dropped the structure, and say which flag you used.
- **Do not paste images.** They do not travel; the checklist is the only path.
- **Re-run, do not retype.** If a heading or list lands plain, rerun the converter and try the next step instead of hand-fixing the draft.

## Known edges

- **A code block used to end with a blank line in LinkedIn.** The cause was the newline a fenced block keeps before its closing fence: `<pre>` ignores it, but the editor treated it as an empty paragraph inside its code chrome. The converter strips trailing newlines from every `<pre>`, and the blank line is gone (verified 2026-11-11). Do not re-add one for spacing.
- **The written file is the paste payload, not a document.** Copying a full HTML document (`<!doctype>`, `<title>`, `<style>`) makes the editor paste the head as literal text above the article — the title and the whole CSS rule set showed up as the first paragraph. The fragment has no head by construction; `--styled` writes the preview document separately, and that one must never be pasted.
- **Tables exist only as images.** The editor has no table model; a flattened list keeps the values, a PNG keeps the grid.
- **The clipboard needs an owner.** A `wl-copy` started from an agent session is reaped when the turn ends; run it in your own terminal with `-f`, or copy from Firefox.

## Verify

```sh
scripts/md2rich.py <file> --no-clip --print | grep -o '<table>\|<pre>' | sort | uniq -c
wl-paste -n --type text/html | head -c 200
```

Also check that the clipboard still has an owner: `pgrep -a wl-copy`. A Wayland clipboard lives only as long as the client serving it, and the script prints the pid it started (`wl-copy -f`, detached into its own session). If that process is gone, the paste will find nothing — rerun the converter rather than debugging LinkedIn.

The first line tells you whether the structures are actually in the payload — `261108` gives 4 tables and 8 code blocks. Use `wl-paste -n`: without it, `wl-paste` appends a newline the clipboard never held, which looks like a stray blank line.

The fragment carries no newlines between blocks, so the paste cannot gain empty paragraphs. After pasting, check three things: the first heading is large, a numbered list kept its numbers, one table still has cells.
