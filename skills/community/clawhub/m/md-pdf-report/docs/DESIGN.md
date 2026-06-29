# Design Rationale

Why md-pdf-report exists, why weasyprint, why "MD as single source of truth", why auto-delivery to chat.

---

## The Problem We're Solving

Every AI agent long-form workflow ends the same way:

1. Agent writes a long Markdown report (research, fact-check, scheme, comparison).
2. User wants a PDF for viewing / sharing / printing.
3. User is on a different device (phone, another computer, Feishu mobile).
4. Agent has to use workarounds: base64 PDFs in chat, screenshot-to-PDF, or "the file is at `/tmp/xxx.pdf`" (which the user can't open).

This is a small but recurring pain point — and the standard "fix" (generate the PDF, save it locally, give the user a path) is broken for the common case.

**md-pdf-report** solves all three problems at once.

---

## Three Design Principles

### 1. Markdown is the single source of truth

The same content needs to serve three audiences:

| Audience | Wants | Format |
|----------|-------|--------|
| User, viewing the final report | PDF | `.pdf` |
| User, editing the report later | MD | `.md` |
| Other agents, processing the report | MD (parseable, structured) | `.md` |

If PDF were the source, you'd lose editability and parseability. If both were generated independently from a shared template, they'd drift. So: **MD is canonical, PDF is derived.**

This is the same principle as "Jinja templates → HTML output" or "Markdown → rendered web page". Source is the structured text, output is the presentation.

### 2. PDF is generated FROM the Markdown, not authored separately

There's no parallel `report.pdf` source. There's no `templates/`-driven content authoring. The user (or the agent) writes Markdown; the PDF falls out of it.

This means:
- The Markdown you write IS what shows up in the PDF, character-for-character
- No risk of "the PDF has text that isn't in the MD" or vice versa
- Editing the MD and regenerating the PDF is a one-command operation

### 3. Auto-delivery to chat is mandatory, not optional

The "必做最后一步" rule in the skill says: **you must send both files to the chat via `MEDIA:`**, not just save them locally. The user's local file path is useless across devices.

This is enforced in the skill definition (top callout) AND in the verification checklist. The skill is not "done" until both files are in the chat.

---

## Why weasyprint (not reportlab, not pandoc)?

The full comparison is in [`references/pdf-engine-comparison.md`](../references/pdf-engine-comparison.md). Summary:

| Engine | Code Complexity | CJK | Install | Output Size | Style Control |
|--------|----------------|-----|---------|-------------|---------------|
| **weasyprint** ⭐ | Low (HTML+CSS) | ✅ | Needs `brew install pango` | 2-3 MB/page | ⭐⭐⭐⭐⭐ |
| reportlab | Medium (Python API) | ✅ | Pure pip | 0.3 MB/page | ⭐⭐⭐ |
| pandoc + LaTeX | Lowest (pure MD) | ✅ | MacTeX 5GB+ | 1-2 MB/page | ⭐⭐⭐⭐ |

We chose weasyprint because:

- **CSS is 10× more readable than reportlab's `ParagraphStyle` API.** When you want to style a callout, you write `.callout { background: #FEF2F2; }` — not 5 lines of Python with a custom ParagraphStyle class.
- **No 5GB LaTeX install.** The user's machine is a Mac, not a build server. MacTeX is too heavy.
- **MD → HTML → PDF is a clean pipeline.** Easy to debug (we keep the intermediate HTML with `--keep-html`), easy to extend (add CSS, change HTML), and aligned with the rest of the web ecosystem.
- **The 2-3 MB/page output cost is fine** for one-off research reports. Feishu/Telegram handle it.

The one downside is the weasyprint C library dependency. `references/weasyprint-bootstrap.md` documents the one-time `brew install pango` setup. After that, `md2pdf.py` auto-bootstraps the library path on import.

---

## Why "auto-deliver to chat"?

Because the user is on a different device. Local file paths are useless across machines. The `MEDIA:` prefix in a chat message is the **only** reliable cross-device file delivery mechanism in Hermes / Feishu / Telegram.

The "必做最后一步" rule is the keystone of this skill. Without it, the PDF generation is academic — the user can't actually get the file.

---

## What we deliberately did NOT do

### Did not implement a custom DSL or templating language

A custom DSL (e.g. "write your report in `!callout` tags" or "use the `@table` directive") would be more expressive but also more error-prone. Markdown is the lingua franca of agent output — using it directly means the user can preview, edit, version, and share their report in any Markdown viewer.

### Did not embed the font subsetting in the default path

Font subsetting (using `pyftsubset` to embed only the characters the document uses) would shrink PDFs by 50-80%. But it's an extra dependency and the unsubsetted 2-3 MB/page is still perfectly shippable. We left it as a `pip install fonttools brotli` advanced option in troubleshooting.

### Did not auto-detect output intent

Some users want a quick HTML preview, some want a PDF, some want both. We always generate PDF, and the `--keep-html` flag adds HTML. We don't try to guess — the user's instruction is the source of truth.

### Did not support arbitrary input formats

No DOCX → PDF, no Notion → PDF, no Google Docs → PDF. Markdown in, PDF out. The scope is narrow on purpose.

---

## Future ideas (not implemented)

- **Theme presets**: a few built-in visual themes (corporate, academic, hacker) selectable via flag.
- **TOC support**: markdown-toc extension is already enabled, just needs a CSS styling pass.
- **Mermaid diagrams**: render mermaid blocks to SVG before PDF generation.
- **Code syntax highlighting**: requires pygments integration in the CSS.
- **PDF outline / bookmarks**: weasyprint supports this; would be nice for long reports.

These are all easy to add later. The current scope (Markdown in, PDF out, native CJK, auto-deliver) is the highest-value core.

---

## Acknowledgments

The `.ttc` vs `.ttf` font issue was the biggest gotcha. macOS's PingFang.ttc, STHeiti Medium.ttc, etc. all use PostScript outlines (CFF/Type 2), which Python's font libraries cannot load. The fix is to use the `.ttf` files in `/System/Library/AssetsV2/.../AssetData/` — but these are buried deep in Apple's font asset bundles, with paths that include opaque hashes.

`references/macos-cjk-fonts.md` documents the exact working paths and a `find` command to verify them on any macOS install.
