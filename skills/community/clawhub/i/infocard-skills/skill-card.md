## Description:

Generate high-density editorial HTML info cards in a modern magazine and Swiss-international style, then capture them as ratio-specific screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaom](https://clawhub.ai/user/shaom)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and developers use this skill to turn supplied text or core information into screenshot-ready editorial HTML cards and optional PNG captures across supported aspect ratios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot helper launches a local Chrome or Chromium binary to render user-provided HTML.

Mitigation: Review generated HTML before capture, use a trusted browser binary through CHROME_BIN, and run the helper only in an environment where local rendering is acceptable.

Risk: The default template loads Google Fonts during rendering, which may make a network request.

Mitigation: Remove the remote font import or replace it with local fonts when offline-only or locale-neutral rendering is required.

Risk: Dense editorial layouts can become misleading or hard to read if text overlaps or the selected ratio is overloaded.

Mitigation: Apply the built-in self-checks for readability, title/body separation, ratio fit, and visual density before using the HTML or PNG.

## Reference(s):

- [Editorial card prompt spec](references/editorial-card-prompt.md)
- [Supported ratios](references/ratios.md)
- [ClawHub skill page](https://clawhub.ai/shaom/skills/infocard-skills)
- [Default Google Fonts stylesheet](https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700&family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown response with one density sentence, a complete HTML code block, optional screenshot command, and optional PNG file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports fixed ratio presets 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, and 5:2; PNG capture requires a local Chrome or Chromium binary.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
