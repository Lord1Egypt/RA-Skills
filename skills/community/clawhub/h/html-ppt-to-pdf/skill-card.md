## Description: <br>
Convert HTML slide decks that use the `<section class="slide">` convention into high-fidelity, vector-text PDFs using Playwright and Chromium PDF rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dtacheng](https://clawhub.ai/user/dtacheng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and slide authors use this skill to convert HTML-based presentation decks into selectable-text PDFs while preserving slide sizing, pagination, fonts, and page numbers. It is intended for HTML slide decks that follow the documented slide selector convention, not ordinary web pages, Markdown, or PPTX files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter renders local HTML in a browser context, so untrusted decks can execute active web content or attempt network access during rendering. <br>
Mitigation: Only convert HTML from trusted sources, or run the converter in a sandboxed environment with network access blocked for sensitive or untrusted decks. <br>
Risk: Remote fonts or assets may fail to load, especially when network access depends on a proxy. <br>
Mitigation: Prefer local fonts and local assets for sensitive or production decks; use a trusted proxy only when needed. <br>
Risk: Bundled Chromium may have PDF rendering issues for some reveal-style slide layouts. <br>
Mitigation: Use system Chrome or Microsoft Edge when available and verify page count, page size, page numbers, and selectable text after conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dtacheng/html-ppt-to-pdf) <br>
- [Troubleshooting README](artifact/README.md) <br>
- [DeckTape](https://github.com/astefanutti/decktape) <br>
- [Google Webfonts Helper](https://gwfh.mranftl.com/fonts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce a PDF file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single vector PDF from a local HTML slide deck and can optionally emit a debug PNG.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
