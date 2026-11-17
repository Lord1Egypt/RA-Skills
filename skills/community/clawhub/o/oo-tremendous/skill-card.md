## Description:

Tremendous (tremendous.com). Use this skill for ANY Tremendous request — reading, creating, and updating data. Whenever a task involves Tremendous, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Tremendous account data and create reward orders or redemption links through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-CLI setup fallback can execute a downloaded installer without prior review.

Mitigation: Install a reviewed oo CLI release yourself and prevent automatic setup.

Risk: Connecting Tremendous gives OOMOL access to the account, including actions that create or change rewards.

Mitigation: Retain the required user confirmation for reward orders and other writes.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Tremendous](https://www.tremendous.com)
- [Tremendous API documentation](https://developers.tremendous.com/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Tremendous action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
