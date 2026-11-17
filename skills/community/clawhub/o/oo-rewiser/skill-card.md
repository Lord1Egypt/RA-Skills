## Description:

Use Rewiser to read, create, and update data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Rewiser users can list folders, review recent transactions, and create transactions through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can make persistent changes to other agent apps through cross-app skill synchronization.

Mitigation: Review the CLI before setup, inspect its synchronization behavior, and set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if needed.

Risk: The remote installers and server-side implementation have not been verified, and the connected account can access Rewiser data.

Mitigation: Review the CLI installation before setup, connect only the intended Rewiser account, and inspect each transaction payload before confirming it.

## Reference(s):

- [Rewiser](https://rewiser.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Rewiser skill release](https://clawhub.ai/oomol/skills/oo-rewiser)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads; action results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction creation changes Rewiser data and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
