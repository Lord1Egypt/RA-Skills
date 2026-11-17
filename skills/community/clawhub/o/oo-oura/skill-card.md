## Description:

Oura (ouraring.com). Use this skill for ANY Oura request — searching and reading data. Whenever a task involves Oura, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve sleep, readiness, activity, heart-rate, and other Oura account data through their connected OOMOL account. The skill provides read-only Oura connector actions to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded software and make broader agent changes without a clear approval step; OOMOL may also handle sensitive Oura health data.

Mitigation: Review and approve the CLI installation, consider whether OOMOL should handle the account's health data, and review the CLI controls before use. OO_SKILLS_SYNC_DISABLED disables startup skill synchronization. The installer and hosted implementation were not verified and may change.

## Reference(s):

- [Oura API documentation](https://developer.ouraring.com/)
- [Oura](https://ouraring.com)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured Oura API response data in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, sleep, activity, and wellness data returned by the requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
