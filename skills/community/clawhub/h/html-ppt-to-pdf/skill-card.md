## Description:

Converts HTML slide decks that use the `section.slide` convention into high-fidelity, vector-text PDFs with selectable text, embedded font subsets, corrected slide numbers, and fixed page sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtacheng](https://clawhub.ai/user/dtacheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and content authors use this skill to convert compatible HTML slide decks from html-ppt, frontend-slides, frontend-design, or hand-written sources into printable PDF files while preserving vector text and slide layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted HTML decks may execute JavaScript or make network requests during browser-based conversion.

Mitigation: Convert only trusted decks, or run the conversion in a sandbox or container with restricted outbound network access.

Risk: Browser or dependency drift can affect conversion fidelity and production repeatability.

Mitigation: Use a pinned Playwright install, keep a clean lockfile, and verify page count, page size, slide numbers, and selectable text before relying on the PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtacheng/skills/html-ppt-to-pdf)
- [Troubleshooting guide](artifact/README.md)
- [DeckTape](https://github.com/astefanutti/decktape)
- [Google Webfonts Helper](https://gwfh.mranftl.com/fonts)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF file plus command-line status output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a single vector PDF from a local HTML slide deck; default page size is 1920 x 1080 pixels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
