## Description:

Create OpenClaw agents and onboard Feishu routing with explicit multi-step confirmations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[absolins](https://clawhub.ai/user/absolins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create OpenClaw agents, bind them to specific Feishu conversations, validate the resulting routing configuration, and prepare rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect Feishu account or peer fields can route conversations to the wrong agent.

Mitigation: Review the final agent details, peer.id, accountId, and binding snapshot before approving any write.

Risk: The workflow reads and may modify local OpenClaw configuration.

Mitigation: Run it only where local OpenClaw config access is permitted, capture the current bindings before changes, and validate after every write.

Risk: Broad account-level bindings or missing peer fields can cause messages to fall back to the main route.

Mitigation: Prefer peer-specific bindings, keep precise rules before fallback rules, and run the included Feishu binding validator.

## Reference(s):

- [Command examples and rollback snippets](artifact/references/commands.md)
- [Chinese runbook and confirmation checklist](artifact/references/usage-zh.md)
- [Feishu binding validation script](artifact/scripts/validate_feishu_bindings.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes step-by-step confirmation prompts and validation or rollback guidance for local OpenClaw configuration changes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
