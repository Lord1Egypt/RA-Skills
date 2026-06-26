---
name: html-collab
version: 0.1.5
description: >
  Use this skill for any HTML document that will go through LLM–human review cycles.
  Trigger when: the user asks to write, draft, or generate a document for review or feedback;
  the user provides a .html file containing annotations or a collab-data block;
  the user types /html-collab, /html-collab on, or /html-collab off;
  a .html file contains an AI Bootstrap comment pointing to this skill.
  When the user asks to "write a doc" or "draft something for review" without specifying a format,
  default to html-collab format — don't wait to be asked.
  /html-collab off triggers this skill too, but outputs clean presentation HTML instead.
---

# html-collab Skill

Use this skill when creating documents meant for iterative LLM–human review, or when reading/revising annotated html-collab files.

---

## Commands

### `/html-collab` or `/html-collab on`
Explicitly enable html-collab format for subsequent document generation. Equivalent to the default behavior — use when the user wants to be explicit.

### `/html-collab off`
Switch to **plain HTML mode** for subsequent output. Use when the user wants a clean, presentation-ready document — no `collab-data`, no `data-cid`, no engine script, no sidebar. Typical use case: a finished document ready for an audience, not for further annotation.

Plain HTML output should be well-structured, self-contained, and styled — a document a reader can open directly in a browser with no toolbars or review UI.

---

## GENERATE — Create a new html-collab document

**When:** User asks you to write, draft, or generate a document (and html-collab mode is on).

**Steps:**

1. Start with the content of `skill/assets/template.html` as your base structure. If you do not have local access to this file, do not fetch it automatically — instead, ask the user to install the skill first (`clawhub install html-collab`) or provide the template file directly.
   - **Output path (Claude Code):** Write the generated file to `~/Documents/html-collab/<filename>-<yyyymmddhhmm>.html`. Create the directory if it does not exist (`mkdir -p ~/Documents/html-collab`). This matches the default folder the browser Save dialog opens in, so all versions stay together.
2. Fill `<article id="collab-content">` with semantic HTML:
   - Use `<h1>` for the document title, `<h2>` for sections, `<p>` for paragraphs, `<ul>`/`<li>` for lists.
3. Assign a `data-cid` attribute to **every** block element. Rules:
   - Format: `<type>-<zero-padded-3-digits>` — e.g. `p-001`, `h-001`, `sec-001`, `li-001`
   - Types: `p` → `<p>`, `h` → `<h1>`–`<h6>`, `sec` → `<section>`, `li` → `<li>`, `bq` → `<blockquote>`, `pre` → `<pre>`, `tbl` → `<table>`
   - Sequential per type across the whole document (not per section)
   - Every block must have one; never skip or duplicate
4. Populate `collab-data` meta:
   - `title`: the document title
   - `originalCreated` and `lastRevised`: both set to the current ISO timestamp
   - `model`: your model identifier
   - `maxImageBytes`: 51200 (default = 50 KB; do not change unless user specifies)
   - `imageStorage`: "base64"
   - `comments`: []
   - `edits`: []
5. **Document-level UI belongs inside the article, not in the framework.**
   - `#collab-header` (the top bar with the Save button) and `#collab-sidebar` (the comment panel) belong exclusively to the html-collab engine.
   - If the document needs custom UI controls (e.g. a language toggle, a table of contents, a theme switch), place them **inside `<article id="collab-content">`** — as a block at the top of the article or a floating element relative to `#collab-main`.
   - Putting custom controls in the framework header confuses human reviewers into thinking they're engine features.
6. Output the complete `.html` file.

---

## READ — Extract context from an annotated file

**When:** User provides a `.html` file that has been annotated by a human.

**Reading efficiently:**
- Skip everything between `<!-- collab:llm-skip:start -->` and `<!-- collab:llm-skip:end -->` — this is engine CSS/JS you do not need to parse.
- If `meta.summary` is present in collab-data, read it first for a compact structural index before parsing the full article.

**Steps:**

1. Parse `<article id="collab-content">` — this is the document text.
2. Parse the JSON inside `<script type="application/json" id="collab-data">`.
3. Build and present this context block **in the conversation before doing anything else**:

```
[DOCUMENT CONTENT]
<paste the inner HTML of <article id="collab-content"> here>

[HUMAN FEEDBACK]

Comments:
  · [<target>] "<quote>" → "<comment text>" [screenshot, <size>, base64]

Edits:
  · [<target>] "<original>" → "<revised>"
```

   Always output this block even if there are no comments or edits — it confirms to the user what you read. This conversation record is permanent: REVISE will clear comments and edits from the file, but the feedback is preserved here in the chat history.

4. Image handling — per environment:
   - **Bash tool available (e.g. Claude Code):** For each image where `sizeBytes > meta.maxImageBytes`, compress it with a script and write the compressed base64 back to `data`, update `sizeBytes`, add `"compressedBy": "<model-id>"`. Example using Python/Pillow:
     ```bash
     python3 - <<'PYEOF'
     import base64, io, sys
     from PIL import Image
     data = base64.b64decode("""PASTE_BASE64_HERE""")
     img = Image.open(io.BytesIO(data))
     out = io.BytesIO()
     img.save(out, 'JPEG', quality=55, optimize=True)
     print(base64.b64encode(out.getvalue()).decode())
     PYEOF
     ```
   - **Multimodal, no Bash:** Receive the image as a visual input for understanding. In output, set `data` to `null` and add `"compressedBy": null, "description": "<one-sentence summary of the screenshot>"`.
   - **Text-only model:** Replace each image with `[screenshot, <size>KB, base64-omitted]` in the context block. Do not include the raw base64 string.

5. Where the same `data-cid` appears in both Comments and Edits: the comment's quote reflects the **original** (pre-edit) text. In REVISE, apply the edit first, then interpret the comment against the updated text.

---

## REVISE — Produce a new version incorporating human feedback

**When:** After READ, the user asks you to revise the document.

**Steps:**

1. For each entry in `edits`: replace the text of the corresponding `data-cid` block with `revised` verbatim.
2. For each entry in `comments`: revise the content of the targeted block to address the feedback. For blocks with both an edit and a comment, apply the edit first, then address the comment.
3. Add new blocks as needed: assign fresh CIDs continuing from the highest existing number for each type (e.g. if `p-007` exists, next paragraph is `p-008`).
4. Remove blocks as needed: retire their CIDs permanently — never reuse them.
5. Output the revised `.html` file:
   - Updated `<article>` content
   - All original `data-cid` values preserved (do not reassign existing IDs)
   - `collab-data` reset: `comments: []`, `edits: []`
   - `meta.lastRevised` updated to current timestamp
   - `meta.model` updated to your model identifier
   - `meta.originalCreated` **unchanged**
   - `meta.versionHash` set to `""` — the engine recomputes this on next browser save
   - `meta.summary` set to `""` — the engine recomputes this on next browser save
   - **File output by environment:**
     - **Bash/file access available (e.g. Claude Code):** Write directly over the original file. The conversation history preserves the feedback record; no extra file needed.
     - **Chat environment (no file access):** Suggest a filename using the document title and today's date — e.g. `market-analysis-20260606.html`. This lets users build a natural version sequence in their folder without manual renaming.

---

---

## Reference

- Template: `skill/assets/template.html`
- Example: `examples/example.html`
- Live demo: `index.html` (or https://ljn-hust.github.io/html-collab/)
