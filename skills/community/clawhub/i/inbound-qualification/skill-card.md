## Description:

Helps teams qualify website demo requests by company and ICP fit, record inbound leads, notify Slack, and offer a booking link or thank-you response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales development, and go-to-market engineers use this skill to add an inbound demo form that qualifies work-email submissions against their ICP, records leads, alerts the sales team, and offers qualified visitors a booking link. An optional research workflow summarizes qualified leads after submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visitor-provided form text can appear as unescaped Markdown in an internal Slack channel.

Mitigation: Render visitor values as plain text or escape Markdown, and enforce server-side length limits before posting.

Risk: A public form collects personal data and may spend enrichment credits on submissions.

Mitigation: Keep the reviewed privacy-page requirement and strict site-origin allowlist; require explicit approval before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/inbound-qualification)
- [Project homepage listed in release metadata](https://github.com/getcargohq/gtm-skills)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides adaptation of the inbound form and optional lead-research workflow.]

## Skill Version(s):

0.2.2 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
