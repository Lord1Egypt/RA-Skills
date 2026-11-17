## Description:

Operate Devin sessions through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect Devin identity and sessions, create sessions, send messages, and terminate sessions through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and enable automatic skill synchronization whose broader changes are not disclosed.

Mitigation: Review setup first, use a reviewed and pinned CLI installation, and check or disable automatic skill synchronization.

Risk: The OOMOL-hosted connector and installer are outside the bundled artifact and remain unverified; the connector mediates Devin requests and credentials.

Mitigation: Inspect the action schema and retain confirmation before creating, resuming, or terminating sessions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Devin](https://devin.ai)
- [Devin API authentication documentation](https://docs.devin.ai/api-reference/authentication)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Devin action responses with user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Devin action.]

## Skill Version(s):

1.0.4 (source: artifact SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
