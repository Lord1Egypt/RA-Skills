## Description:

Convert Markdown to presentations via CLI. Output HTML, PDF, PowerPoint (PPTX), and images (PNG/JPEG).

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers, educators, and documentation authors use this skill to convert Markdown slide decks into HTML, PDF, PPTX, PNG, JPEG, and presenter-note outputs with Marp CLI. It also supports preview, watch, server, and batch conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server mode can expose slide content if intentionally bound beyond localhost.

Mitigation: Prefer localhost-only server use; avoid HOST=0.0.0.0 unless the service is intentionally exposed with firewall and authentication controls.

Risk: Local file access can expose files when processing untrusted Markdown or assets.

Mitigation: Do not enable --allow-local-files or persistent allowLocalFiles settings for untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killgfat/skills/marp-cli)
- [Marp CLI documentation](https://github.com/marp-team/marp-cli)
- [Marp website](https://marp.app/)
- [Marp Core](https://github.com/marp-team/marp-core)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the marp command; browser-backed conversions require Chrome, Edge, or Firefox.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
