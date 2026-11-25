---
name: md-to-medium
description: >
  Convert a Markdown article into an HTML fragment Medium's story editor accepts
  on paste. Medium deletes any image whose source is a data: URI, silently, so
  this converter never inlines bytes: every image is pointed at a public URL and
  the script refuses to pass until those images are pushed. Tables become hosted
  PNGs, because Medium draws no table. The article's H1 is dropped for the Title
  field. Use when the user wants to publish a markdown draft to Medium, asks for
  Medium rich text, or reports that a LinkedIn payload pasted into Medium lost
  its images.
---

# Skill: md-to-medium

# md-to-medium — Markdown into Medium's story editor

Medium's editor has no Markdown and no import path that keeps a technical article intact. This skill converts an article into an HTML fragment the editor accepts on paste, with every image hosted rather than embedded.

Policy: **host the bytes, never inline them.** Medium deletes an `<img>` whose source is a `data:` URI, with no error and no placeholder — so the LinkedIn converter's payload is the wrong vehicle here. Every image points at a public URL, and the payload is only called ready once those URLs are actually pushed.

## Run it

```sh
scripts/md2medium.py docs/261108-hermes-guest-hardening.md
```

Output:

```
html:    docs/261108-hermes-guest-hardening-medium.html

title:   Hardening a Guest Agent
  type this into Medium's Title field — a paste never fills it

3 image(s), hosted at https://raw.githubusercontent.com/j3ffyang/ai-thoughts/main/:
  1. [hosted] Blueprint-style infographic  imgs/261108-hermes-guest-hardening.png
```

Then in the story editor: type the title, click into the body, `Ctrl+V`.

The HTML lands beside the article, named `<article>-medium.html`. It is gitignored — regenerable. The table PNGs under `imgs/medium-tables/` are **not** gitignored: they are the hosted source, and Medium fetches them by URL. An unchanged table keeps its old bytes across runs, so a committed PNG does not churn.

## The push gate

An image URL only works once the file is committed and pushed. The script checks each image against `j3ffyang/main` and refuses to call the payload ready when one is missing:

| Status | Meaning |
|---|---|
| `hosted` | the blob is in the ref and matches the file on disk |
| `changed since push` | the file is committed but edited after the push; the URL serves the old bytes |
| `not pushed` | the ref does not contain the file; Medium would drop the image |
| `outside repo` | the file cannot be hosted from this repo at all |

Exit code is 1 when anything is blocked. `--allow-unpushed` writes the payload anyway and returns 0 — for inspecting the text before the images exist.

A re-render is not byte-identical, so the script compares pixels: when a table's picture has not changed, the old file is kept and its pushed bytes stay valid. Edit the table and the PNG changes, which is exactly when the gate should fire.

## What Medium can hold

| Construct | Result | Why |
|---|---|---|
| headings, paragraphs, bold/italic, lists, quotes, links | kept | native |
| fenced code | kept as `<pre><code>` | pasting preserves multi-line code; the importer does not |
| tables | **PNG at 2x, hosted** (`--tables image`, default), or bullet list (`--tables list`) | Medium draws no table |
| images | **hosted URL** — never `data:` | the editor deletes inlined bytes silently |
| title | **dropped and printed** | a paste never fills Medium's Title field |
| `h4`–`h6` | demoted to `h3` | the editor offers two body heading sizes |

Two routes reach Medium. **Paste** keeps multi-line code. The **importer** at `medium.com/p/import` flattens `<pre>` to a single line and drops tables, so this skill does not target it. Medium's API is no longer supported.

## Flags

| Flag | Effect |
|---|---|
| `--tables image` | screenshot each table to PNG and host it (default) |
| `--tables list` | flatten tables to bullet lists, no hosting needed |
| `--image-base URL` | public URL prefix for images (default: raw GitHub on `main`) |
| `--remote-ref REF` | the ref the image URLs must exist in (default: `j3ffyang/main`) |
| `--allow-unpushed` | write the payload even when an image is not pushed |
| `--out PATH` | write the HTML somewhere other than beside the article |
| `--image-dir PATH` | where table PNGs go (default: `imgs/medium-tables/`) |
| `--base URL` | base URL for relative links |
| `--clip` | also put the payload on the clipboard with `wl-copy` |
| `--print` | print the fragment to stdout instead of writing a file |

The script declares its own dependencies inline, so `uv run` fetches `markdown` and `beautifulsoup4` per invocation. Nothing is installed.

## What travels

| Markdown | In the fragment |
|---|---|
| headings, paragraphs, bold/italic, lists, quotes, links | identical semantics |
| fenced code | `<pre><code>`, newlines and indentation intact |
| tables | `<img>` pointing at a hosted PNG, or a bullet list |
| images | `<img src="https://…">` — a public URL, never a data URI |
| `---` | `<hr>` |

Relative links are rewritten to absolute GitHub URLs. The first `H1` is removed and reported as the title; any further `H1` becomes an `H2`.

## Rules

- **Never inline image bytes.** Medium deletes a `data:` URI without a word. A hosted URL is the only form that survives.
- **Do not paste an unpushed payload.** The text arrives, the images do not, and nothing warns you. Run the script and read its exit code.
- **Never edit the source article to suit Medium.** Convert, and report what changed.
- **Count the images after pasting.** A dropped image is silent, so the article looks complete when it is not.
- **Keep the browser tab open while you paste.** On Wayland the clipboard is served by the tab that owns it; close it and the paste finds nothing.

## Known edges

- **The title is not in the payload.** Medium's editor never fills its Title field from a paste. Type it, or the story goes out untitled.
- **An image inside a link may be dropped.** Medium's importer is documented to drop an image whose caption carries a link; the editor is less forgiving than its own docs suggest. The script reports the case so it is not a surprise.
- **The importer is not a shortcut.** It flattens code and drops tables. Paste is the only route that keeps a technical article intact.
- **Medium's API is gone.** No publishing endpoint exists to automate this; the editor is the only door.

## Verify

```sh
scripts/md2medium.py <file> --print | grep -o 'data:image' | wc -l   # must be 0
scripts/md2medium.py <file> --print | grep -o '<img ' | wc -l        # images in the article
scripts/md2medium.py <file> --print | grep -o 'raw.githubusercontent' | wc -l
```

A payload with `data:image` in it is the wrong payload. Then, after pasting, count the images in the draft — the editor gives no warning when one goes missing.
