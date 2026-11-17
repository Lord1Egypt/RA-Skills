## Description:

Browse webpages with Playwright to wait for page loading, capture full-page or element screenshots, and extract text content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrchenkuan](https://clawhub.ai/user/mrchenkuan)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to capture webpage screenshots and extracted text for browsing, documentation, QA, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-line entry point can execute code from a developer-specific path outside the package.

Mitigation: Review and fix the CLI import so it loads the packaged crawler file before installation or use.

Risk: The skill can browse arbitrary URLs and write screenshots and extracted text to user-selected directories.

Mitigation: Use only explicitly trusted URLs and output directories, and avoid authenticated, private, internal, or sensitive pages until URL and output path controls are documented and enforced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrchenkuan/skills/playwright-controller)

## Skill Output:

**Output Type(s):** [text, shell commands, code, files]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript API examples; runtime output includes PNG screenshots and text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Playwright/Chromium; writes screenshots and extracted text to the selected output directory.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, CHANGELOG, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
