## Description:

OpenClaw Contract Review routes contract review requests through the OpenClaw Contract Review Plugin and enforces intent, authentication, submission, progress, and result-handling gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renzhiping](https://clawhub.ai/user/renzhiping)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and teams use this skill to submit contracts for review, authenticate when required, track progress, add follow-up requirements, and retrieve results through the contract_review tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published bundle metadata has provenance and integrity problems.

Mitigation: Install only after the publisher republishes or explains the bundle metadata and confirms distributed-file checksums match.

Risk: The workflow depends on the required contract_review plugin for contract files, authentication, and Feishu-style progress notifications.

Mitigation: Confirm trust in the plugin and its handling of uploaded contracts, login flow, and notification delivery before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renzhiping/skills/openclaw-contract-review)
- [OpenClaw Contract Review Plugin design](https://your-domain.example/docs/openclaw-contract-review-plugin-skill-design)
- [Intent routing rules](artifact/references/intent-routing.md)
- [Authentication gate](artifact/references/auth-gate.md)
- [Execution rules](artifact/references/execution-rules.md)
- [Interaction examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API Calls]

**Output Format:** [Markdown or plain text responses with contract_review tool invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openclaw-contract-review-plugin >= 0.1.0 and plugins.entries.openclaw-contract-review-plugin.enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
