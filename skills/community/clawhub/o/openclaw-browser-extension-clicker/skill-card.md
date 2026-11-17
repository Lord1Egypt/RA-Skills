## Description:

Automates clicks on browser extension icons, including OpenClaw Browser Relay, by using desktop GUI automation for toolbar, extension, and menu interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbinhihi](https://clawhub.ai/user/binbinhihi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to locate and click browser extension toolbar icons with coordinates, calibration, template matching, dry-run checks, and optional screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop automation can click the wrong browser control or another foreground window.

Mitigation: Use dry-run or calibration first, keep the intended browser focused, and verify coordinates before allowing an actual click.

Risk: Optional screenshots can capture passwords, documents, or other sensitive on-screen content.

Mitigation: Avoid visible sensitive material when screenshots are enabled and remove generated screenshots after calibration or review.

Risk: The skill requires desktop automation and screen-recording permissions and installs Python GUI dependencies.

Mitigation: Grant only the permissions needed for the run and prefer pinned dependency versions inside an isolated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbinhihi/skills/openclaw-browser-extension-clicker)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run a Python desktop automation command that clicks the focused browser and can optionally save a screenshot.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
