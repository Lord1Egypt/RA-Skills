## Description:

Mediastack (mediastack.com). Use this skill for ANY Mediastack request — searching and reading data. Whenever a task involves Mediastack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users with an OOMOL-connected Mediastack account can search live news and news sources through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes remote code that has not been verified.

Mitigation: Review CLI installation separately and prefer a verified, pinned release.

Risk: The CLI can automatically change other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to prevent automatic skill deployment.

Risk: The skill relies on OOMOL-managed credentials and an unverified hosted connector implementation.

Mitigation: Review the connector and credential handling before use.

## Reference(s):

- [Mediastack](https://mediastack.com)
- [Mediastack API documentation](https://mediastack.com/documentation)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Search guidance and oo CLI commands with JSON request payloads; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Mediastack account and provider response.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
