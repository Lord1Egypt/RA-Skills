## Description:

Automates extraction of data from dynamic web pages by using Playwright browser automation, screenshots, and OCR to produce structured CSV or JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to collect chart, dashboard, and visual web data that requires browser interaction plus OCR. It can generate screenshots and structured CSV or JSON extraction outputs for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs broad browser automation with weak containment.

Mitigation: Install and run it only in an isolated, unprivileged environment; remove --no-sandbox where possible.

Risk: Screenshots and OCR outputs may capture sensitive content from authenticated or logged-in pages.

Mitigation: Avoid sensitive pages unless capture scope, output paths, and retention are explicitly reviewed before execution.

Risk: Setup examples include scheduled execution and optional upload paths that could move extracted data automatically.

Mitigation: Do not add cron jobs, sudo setup commands, or upload configuration until dependencies, permissions, and destinations are reviewed and pinned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/playwright-ocr)
- [Configured example target: OpenRouter apps](https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F)
- [Configured example target: OpenRouter rankings](https://openrouter.ai/rankings)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with bash commands; generated CSV, JSON, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, python3, Playwright, pytesseract, pillow, and paddleocr; scripts write outputs to configured output directories.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
