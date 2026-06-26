---
name: admissions-cv-writing
description: "Writes study abroad admissions CVs and resumes, primarily for master's applications. Covers education, research, internships, publications, and awards. Supports PDF export. Use when asked to create, rewrite, polish, or tailor an admissions CV or resume for graduate school application."
---

# Admissions CV / Resume Writing

## Use When

The user wants to create, rewrite, polish, or export an English graduate admissions CV or resume from their education, research, internship, project, activity, award, and skills background.

## Workflow

Use the user's language for all conversation, questions, explanations, and review notes, but keep the actual CV output in English unless the user explicitly asks otherwise.

### Phase 1: Collect Information

Load ONLY [references/info-requirements.md](references/info-requirements.md), then guide the user using that checklist and the material-mining prompts.

- Show the checklist so the user can provide everything at once if they prefer.
- After receiving input, identify what is already covered and ask follow-up questions only for missing required categories or experiences with thin detail.
- Collect by module in order: education -> experiences (priority: research -> internship -> project -> campus activity -> extracurricular activity) -> awards -> skills.
- Mine each experience for bullet-point material: what the user did, which methods/tools they used, and what outcomes followed.
- Use careful inference only as a questioning strategy. You may suggest likely details in question form, but you must keep only what the user confirms and discard what they reject or skip.
- Optional categories should be asked only when useful; they are not mandatory.

⛔ Do not proceed to Phase 2 until every required category in [references/info-requirements.md](references/info-requirements.md) has been addressed. A category is addressed only when the user has either provided all required sub-fields or explicitly confirmed they have nothing for that category. See the Validation Rules section in that reference.

### Phase 2: Confirm Information and Judge Sufficiency

1. Summarize the collected information by section and ask the user to confirm accuracy and missing items.
2. Evaluate whether the material is sufficient using the criteria in [references/info-requirements.md](references/info-requirements.md).
3. Tell the user clearly whether the material is sufficient or thin, and explain why.
4. If the material is thin, ask whether the user can add more detail such as actions, tools, methods, or measurable outcomes. If they cannot, explain that you can carefully infer draft bullet points for review.
   - If the user chooses to supplement, return to the relevant module in Phase 1 and then repeat Phase 2.
   - If the user chooses to skip supplementation, continue to Phase 3 Branch B.

⛔ Do not proceed to Phase 3 until the user explicitly confirms the summary and, when the material is thin, explicitly chooses whether to supplement or skip.

### Phase 3: Produce the CV (Review Version)

Load [references/writing-instructions.md](references/writing-instructions.md) and [references/cv-format-example.md](references/cv-format-example.md), then follow their drafting rules. The output at this phase is a **clean review version without HTML tags**, intended for human reading and confirmation.

#### Branch A: Sufficient Material

Generate the review version:

1. **User-language summary** — a concise section-by-section synopsis for quick fact-checking.
2. **English full text** — the complete CV content in plain text (no HTML `div` tags), following the structure and writing rules from the references.

#### Branch B: Thin Material

**Step 1: Expand bullet points for review**

Load [references/bullet-expansion-guide.md](references/bullet-expansion-guide.md) and generate at least 3 bullet points per experience from the available material.

- Output each bullet in English plus a short explanation in the user's working language when that helps review.
- Clearly mark inferred content on the explanation line with `[Inferred]`.
- Append a follow-up checklist of details that would still strengthen each experience.

⛔ Do not proceed to Step 2 until the user explicitly confirms or revises the expanded bullet points.

**Step 2: Produce the review version**

After user confirmation, generate the review version:

1. **User-language summary** — same as Branch A.
2. **English full text** — include user-approved content; omit rejected inferred content entirely; strip all markers (`[Inferred]`, `[Needs Detail]`).
3. **AI Notes** — append after the English full text, listing remaining gaps and omitted content.

### Phase 4: Quality Check and User Confirmation

Load [references/quality-checklist.md](references/quality-checklist.md) and run the checklist against the **review version** (user-language summary + English full text).

- Group results by severity: Error / Warning / Pass.
- If there are Error-level issues, fix them and present the revised review version.
- After all errors are resolved, ask the user to confirm the final content.

⛔ Do not proceed to Phase 5 until the user explicitly confirms the review version.

### Phase 5: Export

After user confirmation, ask whether the user wants a PDF. If yes:

1. Generate the **tagged English Markdown** from the confirmed English full text:
   - Add HTML `div` layout tags following the patterns in [references/cv-format-example.md](references/cv-format-example.md).
   - The tagged version is for rendering only — it must not alter, add, or remove any content from the confirmed English text.
2. Save the tagged Markdown as a `.md` file at the user-specified path. If none is given, save to the current working directory with the filename `CV_<Full-Name>_<YYYYMMDD>.md` (e.g., `CV_Zhang_Yuhan_20260403.md`).
3. **Consistency check**: compare the saved tagged Markdown (with tags stripped) against the confirmed English full text.
   - This is a content-level comparison; minor differences in symbols or formatting are acceptable.
   - If a content discrepancy is found, fix the file and re-check.
4. Export to PDF (automatically initializes the environment on first run):
   ```bash
   python3 scripts/export-pdf/run.py <input.md> <output.pdf>
   ```
   - Default font mode is `auto`: prefer bundled fonts when the platform allows packaged font files, otherwise fall back to similar local system fonts.
   - If the platform forbids packaged font files, use `--font-source local-only` to force local-font rendering.
   - If bundled fonts are required for brand consistency, use `--font-source bundled-only` so the export fails fast when font assets are unavailable.

All script paths are relative to the `admissions-cv-writing/` skill directory.

**Prerequisites:** PDF export requires Python 3 and an internet connection (for first-time dependency installation). The Python entrypoint creates an isolated venv and installs `weasyprint` and `markdown` automatically. No global packages are modified. If bundled fonts are unavailable, PDF export still works by falling back to locally installed fonts with a similar style, but line breaks and spacing may vary slightly across platforms.

## Output Format

- **Review version** (shown to user): user-language summary + clean English full text, no HTML tags.
- **Tagged Markdown** (written to file): English full text with HTML `div` layout tags, for PDF rendering only. Never shown directly to the user.
- Branch B review: additionally append an `AI Notes` section after the English full text.
- Quality check: group results as Error / Warning / Pass.
