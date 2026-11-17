## Description:

Paddle (paddle.com). Use this skill for ANY Paddle request — reading, creating, updating, and deleting data. Whenever a task involves Paddle, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Paddle account use this skill to read and manage customers, products, and prices through the OOMOL-connected account. It explains how to inspect action schemas and requires confirmation before actions that change Paddle data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unchecked remote code and make broader agent changes.

Mitigation: Review setup first; install a reviewed, fixed oo CLI release yourself and inspect or disable managed-skill synchronization instead of using the automatic installer fallback.

Risk: The hosted connector handles credentials and can make changes to Paddle business data.

Mitigation: Connect only the intended Paddle account with necessary permissions, understand that OOMOL handles its credentials and requests, and retain approval for business-data changes.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Paddle API reference](https://developer.paddle.com/api-reference/overview)
- [Paddle](https://www.paddle.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Text and Markdown with oo CLI commands, JSON payloads, and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform account reads or propose customer, product, and price changes; confirmation is required before write or destructive actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
