## Description:

Ringba (ringba.com). Use this skill for ANY Ringba request — searching and reading data. Whenever a task involves Ringba, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users working with a connected Ringba account can inspect account, campaign, phone number, and publisher information and list active campaigns, numbers, and publishers. Developers can use it to retrieve Ringba data through the oo CLI after checking the action schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI installer code whose behavior is unverified.

Mitigation: Review and approve CLI installation separately, verify the installer and chosen release, and consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Installation may introduce broader persistent agent changes without clear approval.

Mitigation: Review the installer's effects and approve persistent skill synchronization before enabling it.

## Reference(s):

- [Ringba API documentation](https://developers.ringba.com/)
- [Ringba homepage](https://www.ringba.com)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON]

**Output Format:** [JSON data returned from Ringba actions with concise guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, campaign, phone number, and publisher information]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
