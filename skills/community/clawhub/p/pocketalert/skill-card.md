## Description:

The Pocket Alert (pocketalert.app) skill for OpenClaw enables OpenClaw agents and workflows to send push notifications to iOS and Android devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akellacom](https://clawhub.ai/user/akellacom)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send Pocket Alert push notifications from OpenClaw agents, automated workflows, CI/CD jobs, and background monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a Pocket Alert CLI binary whose installation source should be trusted before use.

Mitigation: Install the CLI only from a trusted Pocket Alert source and verify the binary before allowing an agent to run it.

Risk: Pocket Alert API keys can grant notification and administrative access if exposed or over-scoped.

Mitigation: Use least-privilege API keys and avoid pasting secrets into prompts, logs, or shared command output.

Risk: Administrative commands can delete resources or change webhooks, API keys, and the configured base URL.

Mitigation: Require human approval before delete operations, API-key changes, webhook changes, or base_url changes, and restrict agents to send/list operations unless administration is explicitly needed.

## Reference(s):

- [Pocket Alert](https://pocketalert.app)
- [Pocket Alert CLI](https://info.pocketalert.app/cli.html)
- [ClawHub skill page](https://clawhub.ai/akellacom/skills/pocketalert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Pocket Alert CLI commands and operational guidance for sending, listing, and managing notifications, applications, devices, webhooks, and configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
