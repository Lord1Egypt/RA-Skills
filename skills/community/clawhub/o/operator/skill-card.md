## Description:

Operator helps agents manage an Operator fleet of OpenClaw instances, including authentication, instance lifecycle, secrets, automations, webhooks, and agent messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promptrotator](https://clawhub.ai/user/promptrotator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate to Operator and manage OpenClaw agent instances, including monitoring, messaging, lifecycle operations, secrets, automations, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Operator fleet control can create, delete, restart, configure, and message instances, and can manage secrets, automations, webhooks, and workspace files.

Mitigation: Require explicit confirmation before deletes, restarts, secret grants, file writes, automations, webhooks, or other lasting changes.

Risk: Operator API keys stored in local configuration can grant powerful access if exposed or used with an untrusted origin.

Mitigation: Restrict permissions on ~/.operator and its config file, keep operatorAppUrl pinned to a trusted HTTPS Operator origin, and mask API keys in outputs.

## Reference(s):

- [Operator service](https://www.operator.io)
- [Operator ClawHub listing](https://clawhub.ai/promptrotator/skills/operator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell and Python command snippets, configuration examples, API requests, and SSE parsing output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should mask raw Operator API keys and treat lasting fleet changes as confirmation-gated actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
