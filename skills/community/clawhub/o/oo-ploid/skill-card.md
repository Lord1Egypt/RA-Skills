## Description:

Use the oo CLI to access Ploid account, people, LinkedIn, dataset, and monitoring features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an assistant can retrieve and manage Ploid data, search and enrich people or company information, and create datasets or scheduled monitors through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI installer, CLI binaries, and hosted connector implementation were not verified.

Mitigation: Review and approve CLI installation separately, using a pinned, verified release.

Risk: Startup skill synchronization may make automatic changes to other agent skills.

Mitigation: Decide whether this behavior is acceptable; set OO_SKILLS_SYNC_DISABLED to prevent startup synchronization.

Risk: People searches, enrichment, and scheduled monitors can use credits, and scheduled monitors continue until disabled.

Mitigation: Grant only the needed Ploid permissions, set spending limits, and disable monitors when they are no longer needed.

## Reference(s):

- [Ploid homepage](https://ploid.com)
- [Ploid API documentation](https://ploid.com/documentation/getting-started/authentication)
- [oo CLI commands and environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Ploid skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-ploid)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Text]

**Output Format:** [JSON results and natural-language summaries, with oo CLI commands for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the connected Ploid account, granted permissions, selected action, and account spending limits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
