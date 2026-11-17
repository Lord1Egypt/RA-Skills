## Description:

ODSH-Interop helps an OpenClaw agent decide whether to handle a request itself or relay larger execution work to a DeepSeek Harness bridge using task envelopes, bridge zones, notification setup, and an optional read-only audit ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikoribbit](https://clawhub.ai/user/mikoribbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route OpenClaw work between the agent and a DSH execution layer, especially for heavier file, code, retrieval, batch, or optional desktop automation tasks that fit the bridge contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad delegation to an external DSH executor can expose private files, credentials, logged-in browser state, business data, or desktop automation if approvals and shared paths are too permissive.

Mitigation: Define explicit approval rules, restrict the bridge mount and notification channel, disable or tightly control CUA, and review DSH results before persisting them.

Risk: Bridge envelopes or workspace access sent to the wrong target can create execution confusion or cross into areas owned by the other side.

Mitigation: Use the documented DSH target for relayed tasks, write envelopes atomically into the shared input zone, and keep OpenClaw access to the DSH workspace read-only.

## Reference(s):

- [ODSH-Interop ClawHub release](https://clawhub.ai/mikoribbit/skills/odsh-interop)
- [ODSH-Interop skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON envelope examples, shell commands, and optional SQL queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bridge task envelopes and read-only audit queries; results require operator review before sensitive delegation.]

## Skill Version(s):

1.2.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
