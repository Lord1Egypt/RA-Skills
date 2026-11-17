## Description:

Operate Segment through an OOMOL-connected account to send alias, batch, group, identify, page, screen, and track events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to send Segment identity, group, page, screen, and event data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security assessment says helper software can execute unverified online code and install persistent instructions in other agent applications.

Mitigation: Review the CLI installation separately; set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if you do not want skill synchronization, and review any installed instructions.

Risk: Segment write actions change account data.

Mitigation: Fetch the live action schema, review the exact payload and effect, and obtain user confirmation before running each write action.

Risk: Segment payloads pass through OOMOL.

Mitigation: Understand and approve this data path before sending Segment payloads.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-segment)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Segment HTTP API documentation](https://www.twilio.com/docs/segment/connections/sources/catalog/libraries/server/http-api)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch the live action schema before building payloads; require user confirmation before write actions.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
