## Description:

Connect to SaaS tools via Maton AI with a Clawdbot Gateway dashboard for configuring API keys and managing OAuth app connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot Gateway operators use this skill to add Maton SaaS OAuth connection management, configure MATON_API_KEY, and manage connected apps such as Gmail, Slack, Notion, and HubSpot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration handles sensitive MATON_API_KEY credentials and OAuth authority.

Mitigation: Protect MATON_API_KEY like a password and avoid committing or syncing the Clawdbot config file.

Risk: OAuth connection flows can direct users to authorization destinations outside the dashboard.

Mitigation: Verify OAuth destinations before authorizing apps and consider URL allowlisting for production gateways.

Risk: Connection deletion can remove SaaS access configuration.

Mitigation: Add confirmation prompts for deletion in production deployments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/maverick-software/skills/maton-agent-tools)
- [Maton website](https://maton.ai)
- [Maton control API](https://ctrl.maton.ai)
- [Reference implementation guide](artifact/reference/README.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with TypeScript reference code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Clawdbot Gateway RPC handlers, Lit UI components, and API key/OAuth connection setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
