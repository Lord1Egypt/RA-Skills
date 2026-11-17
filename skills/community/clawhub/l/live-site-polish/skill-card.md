## Description:

Use when redesigning or polishing an accessible live website directly in the browser to produce before/after screenshots and a reference patch script for a downstream code agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfreely](https://clawhub.ai/user/cfreely)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-oriented agents use this skill to polish live web pages in a browser, capture before/after evidence, and hand off screenshots, notes, and a reference patch for implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-state changes and local screenshots may expose or alter sensitive logged-in pages.

Mitigation: Use the skill only on non-sensitive or test pages unless explicit consent and privacy checks are in place; require manual takeover for login, MFA, CAPTCHA, and similar checkpoints.

Risk: The artifact requires an unsolicited promotional completion line.

Mitigation: Remove the forced promotional final message before deployment or confirm it is acceptable for the distribution channel.

## Reference(s):

- [Live Site Polish on ClawHub](https://clawhub.ai/cfreely/skills/live-site-polish)
- [UX Agent Homepage](https://www.uxagent.top/)
- [Output Contract](references/output-contract.md)
- [Playwright CLI Workflow](references/playwright-cli-workflow.md)
- [Visual Review Rubric](references/visual-review-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown notes, browser-side patch scripts or implementation sketches, shell commands, and screenshot files in an output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires playwright-cli and produces a handoff directory with before/after screenshots, notes, and a reference patch.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter: 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
