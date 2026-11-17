## Description:

Design and operate auditable webhook, cron, chat-relay, and local-to-remote communication patterns between two OpenClaw instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdpi-ai](https://clawhub.ai/user/clawdpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design explicit, auditable communication between OpenClaw deployments for alerts, task handoffs, audit summaries, workflow callbacks, and local-to-remote coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may propose endpoint exposure, firewall changes, credential placement, cron setup, or webhook delivery changes.

Mitigation: Review and approve endpoint, firewall, credential, and schedule changes before applying them.

Risk: Bridge messages can leak secrets or create hard-to-audit cross-instance behavior if payloads are too broad.

Mitigation: Send summaries instead of raw secrets, keep payloads explicit and idempotent, and preserve append-only logs with acknowledgements.

Risk: Assuming native OpenClaw federation, shared memory, shared sessions, or shared auth state can lead to designs that do not work in the target deployment.

Mitigation: Use only documented commands and delivery modes, and verify the bridge end to end with test messages before production use.

## Reference(s):

- [OpenClaw Peer Bridge on ClawHub](https://clawhub.ai/clawdpi-ai/skills/openclaw-peer-bridge)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional JSON schemas, webhook contracts, cron payload definitions, rollout plans, and troubleshooting checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on reversible, auditable communication designs and avoids unsupported peer-to-peer or shared-session claims.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
