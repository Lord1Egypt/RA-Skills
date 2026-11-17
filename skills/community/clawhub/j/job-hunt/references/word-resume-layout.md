# Word resume layout

`render_cv.py --format docx` uses the reviewed black-and-white layout: centered
name/contact block, serif text, full-width rules under section headings, bold
organization/role labels, right-aligned date columns and hanging bullet indents.
Body text defaults to 11 pt: Times New Roman for English and SimSun (宋体)
for Chinese, including Chinese titles. English body text is
left-aligned so justification cannot stretch word spacing.
Rules are native paragraph borders, not underlined trailing spaces or pictures.
Within a bullet, bold only an explicit opening label ending in a colon
(`Label:` or `标签：`). Leave the remaining text plain. If there is no opening
label and colon, leave the entire bullet plain; do not infer emphasis from its
first clause, keywords or numbers. Do not add labels merely to enable bolding.
The label must describe the entire bullet, not just its first fact. For example,
leave `GPA: ...; courses ...; research ...` wholly plain: the rest of the bullet
is not an explanation of GPA. A colon alone does not justify bold emphasis.

The page size, section order, translated/custom headings, links and personal-data
rules still come from the existing profile contract. Internships remain entries
in `experience`; set an entry's `section: internships` to preserve a separate
internship heading in a supplied template. Other candidates need not use the
example's section order. Photos are absent
from the examples, but an explicitly supplied photo still follows market policy.
When delivering Word and PDF, export the final DOCX with Word/LibreOffice and
deliver that exact PDF. Save the export under `raw/layout/word-export.pdf` and
bind it to the final DOCX in the layout review. A separately generated LaTeX PDF
uses a different template and cannot stand in for the Word export. Check actual
fonts, sizes, margins and all pages using `references/layout-review.md`.

Fictional, editable examples and their inputs:

- [English profile](../assets/word-resume/en.yaml) · [Word output](../assets/word-resume/en.docx)
- [Chinese profile](../assets/word-resume/zh.yaml) · [Word output](../assets/word-resume/zh.docx)

Regenerate from the repository root:

```sh
python scripts/render_cv.py assets/word-resume/en.yaml --format docx --out cv-en.docx
python scripts/render_cv.py assets/word-resume/zh.yaml --format docx --out cv-zh.docx
```

The examples contain no source resume, photo, private contact details or personal
history. Do not put a user's original reference in the repository when adapting
this layout. Inspect the final export, not only the Word editing view: paragraph
markers and pagination squares are non-printing UI aids, not resume bullets.

A supplied template takes precedence over these default fonts and sizes.

For translated versions of the same example, reuse its approved template, section
order, paragraph styles, margins, rules and date columns. Translate the content
inside that layout; do not switch the English version to a different default
template. Use concise, faithful wording where English runs longer and inspect
both final exports together without stretching preview images or shrinking text.

Inspect its document defaults, styles and direct run formatting, including the name font
and mixed body sizes. Preserve the actual font families (Songti SC is not SimSun)
and remove inherited theme overrides when setting them. Verify the fonts embedded
in the exported PDF; readable Chinese alone does not prove template fidelity.
If the source font exists in the installed office suite, make that exact font
available to the exporter. Do not shrink body text merely to force one page.

Aim for a balanced, well-filled page using the supplied content. A largely blank
lower third is not an acceptable first draft when existing content can be
grouped more clearly or spacing redistributed naturally. When the user requests
a full page, expand supported points and adjust paragraph spacing, then record
`minimum_content_bottom_pt` in the format requirements and verify the final PDF
against it. Keep the selected font sizes; avoid duplicate facts, filler wording,
oversized gaps or empty paragraphs. Where space
permits, separate section headings with at most one blank line (prefer paragraph
spacing over empty paragraphs); never stack blank lines or invent content to
fill the page. Verify pagination after adjusting spacing. For report PDFs, use
English Times New Roman and Chinese SimSun when following an explicitly selected
template or font; verify actual exported fonts. Without an explicit report font
selection, the bundled report renderer may use its embedded fallback fonts as
described below. Never describe those as Times New Roman or SimSun. A newer
explicit user typography request overrides the reference template.
Record a requested Chinese font in `meta.cjk_font` of the workspace profile.
Where Pandoc and Tectonic/XeLaTeX are installed, delivery uses it for the report
before its bundled fonts, and a selected font that fails is reported instead of
silently substituted. Without that toolchain delivery uses the bundled fonts and
prints `NOTICE_REPORT_FONT_NOT_APPLIED`; prepare the toolchain if the client asked
for that font in the report, or tell them which font the report uses. Without an explicit selection,
the bundled report renderer remains available without a TeX installation.

## Prevent source syntax in Word

The YAML prose fields are plain text, not Markdown or LaTeX input. Word does not
interpret `$...$`, `\times`, `\text{...}`, `**...**`, backticks or Markdown
links when these strings are passed to `add_run` / `add_paragraph`.

Before rendering, fix such content in the tailored copy, keeping the original
profile and all facts intact. For example, write `8 × H200` instead of
`$8 \times \text{H200}$`; retain the original training steps, duration and
benchmark results. Never remove formula syntax by dropping its enclosed content
or indiscriminately deleting punctuation. Preserve `C#`, `C++`, `A*`, code
identifiers, currency and ordinary mathematical signs.

Use the existing Word heading/list styles and approved label emphasis. Put links
in the structured link fields or native Word hyperlinks, not `[label](url)`
strings. When an actual formula is necessary, use a native Word equation (OMML)
and inspect it in the Word export; do not insert raw LaTeX as ordinary text.

The three bundled Word renderers refuse detected source syntax with `DOCX_MARKUP`
and a part/paragraph location. `check_layout.py` checks the final CV bytes, and
`deliver.py` checks every selected Word file before copying any deliverables,
including externally authored reports and statements. Tables, split text runs,
text boxes, headers and footers are included. Native Word equations are allowed.
Fix the indicated source or native formatting, re-render, re-export any paired
PDF and repeat the visual review. A text check supplements page-by-page review;
it cannot identify every ambiguous notation or replace inspection of the output.

## Native export dialogs

For native Word/LibreOffice export, complete ordinary save and print dialogs directly with the host's available UI tools. Disabled document controls can mean a modal dialog is waiting, not that the application is frozen. Before asking the user to restart or take over, inspect the current app windows and accessibility state; if the dialog is absent from that view, inspect a screenshot and use the host's supported interaction method. Save a separately named output when checking another renderer so existing artifacts remain intact, then verify that the file exists and inspect its text and page layout before reporting success.

Request user intervention only for an observed blocker the available tools cannot resolve or an action that requires human participation under the host's rules. State what is actually visible and what was attempted; do not diagnose a crash from grey controls or one unchanged tool response. This document-export guidance does not change the login, verification or refusal rules for job websites.

For reports, an explicitly selected font/template wins; otherwise the portable
renderer may use its embedded fonts. Any added gap before a section heading is at
most one blank line.
