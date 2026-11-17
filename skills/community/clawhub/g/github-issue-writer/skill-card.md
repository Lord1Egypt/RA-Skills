## Description:

Generate structured GitHub issue cards for the WeBuddhist team when backend, frontend, or app developers need to document new, changed, or fixed API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-lo](https://clawhub.ai/user/tech-lo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn OpenAPI specs, natural language endpoint descriptions, inline API details, or existing issue context into consistent GitHub issue cards for API integration work. The skill also guides the user through review, repository selection, project-board selection, and issue creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe GitHub CLI command construction with user-derived issue titles and bodies.

Mitigation: Validate repository and project selections, pass issue bodies through a safe body file or structured API call, and avoid interpolating untrusted title or body text directly into shell commands.

Risk: Generated issue cards may omit or misstate endpoint details when inputs are incomplete.

Mitigation: Keep the required human review step before issue creation and use [TBD] for unknown behavior instead of inventing details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tech-lo/skills/github-issue-writer)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown issue-card content with optional GitHub CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review before issue creation; marks missing endpoint details as [TBD].]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
