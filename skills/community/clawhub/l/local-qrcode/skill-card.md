## Description:

Generate QR codes locally from text/URL to PNG image or ASCII art. Pure local generation using qrcode library. No API key required. Use when users need to create QR codes for links, text, or any content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alone86136](https://clawhub.ai/user/alone86136)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate QR codes from text or URLs as local PNG files or terminal ASCII output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change behavior or affect reproducibility across installations.

Mitigation: Install the skill in a dedicated virtual environment and pin qrcode and Pillow versions when reproducible output matters.

Risk: PNG output is written to the caller-provided path, so an incorrect path could overwrite an intended local file.

Mitigation: Review the output path before execution and write generated QR images to a dedicated output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alone86136/skills/local-qrcode)
- [ClawHub publisher profile](https://clawhub.ai/user/alone86136)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are PNG files or terminal ASCII text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG generation writes only to the caller-provided output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
