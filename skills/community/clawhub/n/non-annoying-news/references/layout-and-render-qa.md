# Layout and Render QA

## Format

- Build print-oriented HTML/CSS first.
- Use A4 by default; switch to Letter only if the user asks.
- Use multi-page newspaper structure: masthead, issue line, sections, article hierarchy, columns, source notes.
- Use a restrained palette. Avoid dashboard cards, badge-heavy UI, neon labels, and decorative clutter.
- Apply the user's design preset/density from local config when available. See `references/design-presets.md`.

## Rendering

Preferred path:

1. Create one HTML file with `.page` sections or one HTML file per page.
2. Render to PDF with OpenClaw browser PDF tooling or `scripts/render_issue.mjs`.
3. Generate PNG previews/screenshots for every page.
4. Inspect each preview visually.
5. Run text QA with `scripts/qa_text.py` on HTML or extracted PDF text.
6. Validate local config with `scripts/check_config.py` when this is a configured/recurring issue.

If the browser renderer is missing, use Playwright/Chromium if installable. If no renderer is available, deliver HTML only and explain what dependency is missing.

## Page design rules

- Masthead should be calm, readable, and preferably one line.
- Use serif fonts for body/headlines; sans-serif for metadata/kickers unless the chosen preset says otherwise.
- Use justified body text where it does not create large gaps; short side briefs may be left aligned.
- One strong image on the front page is fine. Inside images should be smaller and source-relevant.
- Images should come from sources or be clearly treated as illustrations. Do not reuse old issue images as generic placeholders.
- Side rails should feel deliberately edited: usually 4–7 useful briefs per front-page rail depending on density.
- Empty lower thirds, half-height rails, and orphan side boxes are failures, not "breathing room".

## Premium polish gate

Before delivery, ask:

- Would this page make the user want the next issue?
- Is the visual hierarchy obvious in three seconds?
- Does the page have a lead, supporting stories, and useful side material?
- Are rails and article grids balanced enough to feel intentional?
- Does any label, box, or sidebar exist only because the layout had a hole?
- Does the result feel like a compact publication rather than a rendered prompt response?

If the answer is not clearly yes, revise and render again.

## Hard failures

Re-render before delivery if any of these appear:

- clipped text or sentence running off the page;
- half-empty side columns or lower thirds;
- isolated filler boxes at page bottoms;
- repeated generic labels used as padding;
- placeholder/TODO/QA/queue/process text;
- source links as the main content;
- title/masthead broken into awkward orphan words;
- visual artifacts from the browser, UI, or previous drafts;
- unreadably small text after scaling;
- source notes that dominate the page visually.

## Side-column policy

Side columns are editorial space, not packing foam. If space remains, use one of these only when it directly helps the issue:

- concrete number/fact from a source;
- short explanation of a term with immediate article context;
- evidence boundary;
- practical consequence;
- counterpoint or risk;
- short pointer to an inside article;
- "why this was saved" note when it helps explain a bookmark signal.

Do not insert unrelated glossary fragments or vague meta boxes just to fill vertical space.

## Final visual QA checklist

For each page, answer:

- Does the page feel intentionally filled?
- Does every box belong next to its content?
- Are columns balanced enough that no side looks abandoned?
- Are headlines, deck, body, captions, and source notes all readable?
- Does the design match the selected preset/density?
- Would this look acceptable as a compact magazine/newspaper page?

If not, edit and render again.
