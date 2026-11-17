## Description:

Route each incoming message to the right Bankr/OpenClaw model or to a zero-LLM path based on task type, risk, and cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to select a Bankr/OpenClaw model or zero-LLM workflow for a single incoming message based on task type, risk, and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing, transfer, approval, or fund-movement requests may be routed to a low-scrutiny zero-LLM path.

Mitigation: Require independent high-stakes checks before accepting any routing recommendation for wallet, treasury, signing, approvals, or fund movement.

Risk: The skill output is a routing recommendation and not an authorization or safety gate.

Mitigation: Keep transaction approval, signing, and policy enforcement in separate controls that override deterministic routing.

## Reference(s):

- [Routing table](references/routing-table.md)
- [Bankr models available to aaigotchi](references/bankr-models.md)
- [Model Brain on ClawHub](https://clawhub.ai/aaigotchi/skills/model-brain)
- [aaigotchi publisher profile](https://clawhub.ai/user/aaigotchi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, shell-style environment lines, or summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a recommended route, optional fallback route, risk level, task type, and short reason.]

## Skill Version(s):

0.1.2 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
