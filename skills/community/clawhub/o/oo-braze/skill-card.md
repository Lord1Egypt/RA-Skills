## Description:

Braze (braze.com). Use this skill for ANY Braze request — searching and reading data. Whenever a task involves Braze, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to retrieve campaign and Canvas details and list campaigns and Canvases from a connected Braze account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run an online installer that has not been verified.

Mitigation: Review and install a verified oo CLI release yourself before allowing agent use.

Risk: Braze requests pass through OOMOL, and automatic skill synchronization settings can affect agent use.

Mitigation: Use a read-scoped Braze connection and check the automatic skill synchronization settings.

## Reference(s):

- [Braze API documentation](https://www.braze.com/docs/api/basics)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON Braze data with concise text summaries and inline oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
