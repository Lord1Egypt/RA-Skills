## Description:

Use Postalytics to search and read campaigns, delivery statistics, contacts, contact lists, and direct-mail templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with a connected Postalytics account use this skill to find campaigns, review delivery and engagement metrics, and look up contacts, lists, and templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may execute downloaded code whose effects are not verified in the supplied artifact.

Mitigation: Review the CLI installation separately, prefer a verified fixed release, and check whether the installer adds agent skills before proceeding.

Risk: Connecting Postalytics allows OOMOL to mediate access to account data.

Mitigation: Connect the account only when that access is intended, and review the connection's permissions.

## Reference(s):

- [Postalytics API authentication documentation](https://docs.postalytics.com/getting-started/authentication-0)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Postalytics skill on ClawHub](https://clawhub.ai/oomol/skills/oo-postalytics)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON action payloads and returned account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only campaign, statistics, contact, contact-list, and template lookups]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
