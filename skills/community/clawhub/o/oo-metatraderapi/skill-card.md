## Description:

Use MetaTraderAPI through an OOMOL-connected account to inspect account information, sessions, symbols, orders, positions, and trading history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read MetaTrader account and session data through the MetaTraderAPI service, and to start or stop sessions when needed. Changes to session state require user approval as documented by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation process runs downloaded code, and the remote installer contents are unverified.

Mitigation: Verify a specific CLI release before installing and using it.

Risk: The CLI may change other installed agent skills through synchronization.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if you do not want it changing installed skills.

Risk: Actions can affect sessions connected to the authenticated trading account.

Mitigation: Connect only the intended account and follow the documented user-approval requirements for session changes.

## Reference(s):

- [MetaTraderAPI ClawHub page](https://clawhub.ai/oomol/skills/oo-metatraderapi)
- [MetaTraderAPI homepage](https://metatraderapi.cloud/)
- [MetaTraderAPI API documentation](https://metatraderapi.cloud/api/documentation/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API responses, JSON, Guidance, Shell commands]

**Output Format:** [JSON API responses with concise natural-language summaries; Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and the selected action.]

## Skill Version(s):

1.0.2 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
