## Description:

OpenShow turns Markdown, Word, PDF, text, local HTML, and URL inputs into a single full-screen playable HTML slideshow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumacoder](https://clawhub.ai/user/lumacoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent users use OpenShow to convert documents, notes, PDFs, local HTML, or web articles into offline, full-screen HTML decks that can be opened in a browser or OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated slides from untrusted local HTML or web pages may carry unsafe or misleading content into the browser.

Mitigation: Use trusted documents and public URLs, review generated HTML before presentation, and avoid automatic opening for untrusted inputs.

Risk: Outbound URL and image fetching can retrieve unexpected remote content or leave retained remote URLs when image download fails.

Mitigation: Prefer trusted local files for sensitive work, verify external media sources, and check the generated deck for missing or remote assets.

Risk: Installing runtime dependencies directly into a shared Python environment can affect other projects.

Mitigation: Install dependencies in a virtual environment before running the converter.

## Reference(s):

- [OpenShow ClawHub listing](https://clawhub.ai/lumacoder/skills/open-show)
- [OpenShow README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown response with shell commands, generated HTML file paths, and presentation controls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a single self-contained HTML slideshow file; optional flags can open it in a browser or OpenClaw.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter says 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
