## Description:

Enforce email safety policies at the network level with NemoClaw, covering setup, the Outlook preset, and policy enforcement for production email agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to configure NemoClaw network policies for MCP-based email agents, especially Microsoft 365 and Outlook workflows that need read, draft, and send controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Outlook preset leaves Microsoft Graph send-capable POST access open while being presented as an email send guardrail.

Mitigation: Review the Outlook preset before relying on it for send prevention, and use a custom policy that blocks send-capable access when send prevention is required.

Risk: MCP-level recipient controls may not protect deployments that also allow direct Microsoft Graph clients.

Mitigation: Use least-privilege Graph scopes, avoid Mail.Send for read/draft agents, and enforce recipient approval in a component that direct Graph clients cannot bypass.

Risk: An unverified NemoClaw installation source can add supply-chain risk to the email policy layer.

Mitigation: Pin or verify the NemoClaw installation source before using this policy in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/nemoclaw-email-policy)
- [email-agent-mcp GitHub repository](https://github.com/UseJunior/email-agent-mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup, verification, troubleshooting, and policy-hardening guidance; does not execute commands.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
