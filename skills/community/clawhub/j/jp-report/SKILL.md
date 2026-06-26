---
name: jp-report
description: Generate a formal Japanese corporate-style HTML document and PDF (日本企業向け正式報告書). Triggered when user asks to create a Japanese business report, compliance document, security overview, or 日本語報告書.
disable-model-invocation: true
argument-hint: [source-file-or-content] [output-folder]
---

Generate a formal Japanese corporate document (日本企業向け正式報告書) from the provided source material.

## INPUTS

If `$ARGUMENTS` is provided, treat it as the source file path or inline content.
Otherwise, ask the user for:
1. **Source material** — file path or pasted content
2. **Document purpose** — e.g. security overview / compliance / product explanation
3. **Japanese title** + English subtitle
4. **Classification level** — 社外秘 / 部外秘 / 社内限り (default: 社外秘)
5. **Output folder path**
6. **Revision number** (default: Rev. 1.0)

---

## STEP 1 — ANALYZE

Read source material. Identify:
- Logical sections → map to 4–6 chapters
- Content types: principles, tables, architecture diagrams, bullet lists
- Brand names / technical terms to preserve verbatim
- Content to exclude (confirm with user if unclear)

---

## STEP 2 — TRANSLATE TO FORMAL JAPANESE

Rewrite all content in 書き言葉・敬体:
- Verb endings: 〜しております / 〜いたします / 〜となっております
- Full grammatical sentences — no fragment bullets inside tables or definitions
- Preserve intact: brand names, acronyms (RBAC, TLS, SSO, BYOK), product names
- Do NOT add certifications (SOC/ISO/GDPR) unless explicitly in source

---

## STEP 3 — PLAN PAGES

Fixed structure:
```
Page 1  —  表紙 (Cover)   : centered layout, one full A4 page
Page 2  —  目次 (TOC)     : dotted leaders + page numbers, one full A4 page
Page 3+ —  本文 (Body)    : chapters distributed, target one chapter per page
```

Numbering: 第１章 / 第２章 … (full-width) · Sections: 1.1 / 1.2 … (decimal)

**Before writing HTML**, calculate content height using the reference in `${CLAUDE_SKILL_DIR}/docs/design-rules.md`.
Usable area per page ≈ **980px**. State the page plan briefly to the user.

---

## STEP 4 — GENERATE HTML

Write a single self-contained `.html` file using:
- CSS from `${CLAUDE_SKILL_DIR}/docs/design-rules.md` (include verbatim in `<style>`)
- Component HTML from `${CLAUDE_SKILL_DIR}/docs/components.md`

Every page must follow this shell:
```html
<div class="page">
  <div class="page-body"> <!-- content --> </div>
  <div class="page-footer">
    <div class="f-l">[Product / Company]</div>
    <div class="f-c">[Document title]　Rev. X.X</div>
    <div class="f-r">[Classification]　｜　[Page #]</div>
  </div>
</div>
```

Cover page body must use:
```html
<div class="page-body" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
```

---

## STEP 5 — GENERATE PDF

Immediately after writing the HTML, run:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py [absolute path to .html]
```

The script handles Chrome invocation and URL-encodes the path automatically.
Report the output line (bytes + path) on success.

---

## QUALITY CHECKLIST

- [ ] Cover: content vertically + horizontally centered
- [ ] TOC: page numbers match actual layout
- [ ] Every `.page` div has a `.page-footer`
- [ ] No bright colors, emoji, or casual language
- [ ] PDF generated successfully (bytes confirmed)
