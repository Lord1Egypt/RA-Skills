## Description:

Inspect and manage a workspace's email authentication (DMARC, SPF, DKIM, MTA-STS) in MailGlo through the mailglo command-line tool or MailGlo's MCP server, within the permissions a person gave you.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailglo](https://clawhub.ai/user/mailglo)

### License/Terms of Use:

MIT-0

## Use Case:

MailGlo workspace owners and their authorized agents use this skill to inspect email authentication checks and prepare carefully scoped changes to DMARC, SPF, DKIM, MTA-STS, and BIMI settings. It guides agents to confirm workspace access, gather required details, and leave approval and execution to authorized people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, so some referenced paths were not resolved and the assessment has incomplete evidence.

Mitigation: Review whether the change-plan workflow fits your needs before installing, as the scan guidance recommends.

Risk: An OpenClaw Gateway sign-in is shared with every agent on that Gateway and anyone who can message one, exposing the signed-in person's MailGlo workspace and draft changes.

Mitigation: Use a separate Gateway for each person who needs MailGlo, as the skill instructs.

## Reference(s):

- [MailGlo agent documentation](https://mailglo.com/docs/agents/)
- [MailGlo CLI guide](https://mailglo.com/docs/cli/)
- [MailGlo MCP documentation](https://mailglo.com/docs/mcp/)
- [OpenClaw MCP transport documentation](https://docs.openclaw.ai/cli/mcp/transports)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
