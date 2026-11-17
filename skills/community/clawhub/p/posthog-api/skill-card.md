## Description:

Guides agents in using authenticated PostHog APIs to query product analytics, manage feature flags, inspect session recordings, and support experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to investigate PostHog events and user behavior, work with feature flags and experiments, and retrieve session recordings when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person records and session recordings can reveal sensitive user information.

Mitigation: Prefer aggregate, narrowly scoped queries; access recordings only when requested and avoid sharing identifiers or replay content.

Risk: Broad account access or unapproved changes can affect PostHog data and settings.

Mitigation: Use OAuth with read-only scopes where possible and confirm each new connection or write with the user.

Risk: Hosted functions, triggers, or destinations can run or forward data persistently.

Mitigation: Obtain separate approval before creating automation or forwarding, including its destination and the data it may send.

## Reference(s):

- [PostHog API documentation](https://posthog.com/docs/api)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)
- [PostHog skill on ClawHub](https://clawhub.ai/byungkyu/skills/posthog-api)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PostHog API access requires an authorized Maton connection; writes and new connections require user confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
