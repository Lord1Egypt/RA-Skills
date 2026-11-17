## Description:

Use Codemagic through a connected OOMOL account to inspect apps, teams, users, and builds, and to start or cancel builds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect Codemagic users, teams, apps, and builds, and to start or cancel builds through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run an installer whose contents and broader local changes were not verified.

Mitigation: Review and approve CLI installation separately, verify the chosen release, and review automatic skill synchronization using the documented OO_SKILLS_SYNC_DISABLED control when appropriate.

Risk: Starting or cancelling a build changes Codemagic state through the connected account.

Mitigation: Inspect the live action schema and confirm the exact write payload or cancellation target before running the action.

## Reference(s):

- [Codemagic REST API documentation](https://docs.codemagic.io/rest-api/codemagic-rest-api/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository (referenced by the skill)](https://github.com/oomol-lab/oo-cli)
- [Codemagic](https://codemagic.io)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Analysis]

**Output Format:** [JSON action results and concise text summaries; command examples are Markdown with inline shell code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
