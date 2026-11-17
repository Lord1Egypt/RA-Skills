## Description:

Take a screenshot (PNG) of any website in a headless way (no GUI) to verify it's rendering/working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to capture headless PNG screenshots for visual page checks, uptime verification, and confirming that a website renders correctly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap downloads Playwright and Chromium dependencies before screenshots can run.

Mitigation: Run installation only in an approved environment that allows those package and browser downloads.

Risk: Screenshots can capture private or sensitive page content and write it to disk.

Mitigation: Avoid private authenticated pages unless the output path and resulting PNG are handled as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-web-snapshot)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime produces PNG screenshot files and prints the output path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports --out, --full-page, --wait-ms, and --timeout-ms options; default viewport is 1365x768.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
