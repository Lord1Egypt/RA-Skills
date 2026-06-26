## Description: <br>
Design and operate communication patterns between two OpenClaw instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClawdPI-AI](https://clawhub.ai/user/ClawdPI-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to design auditable OpenClaw-to-OpenClaw communication for alerts, task dispatch, result handoff, approval requests, and scheduled reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook, chat, or cron bridges can become real data-sharing paths between systems. <br>
Mitigation: Use trusted authenticated endpoints, define explicit trust boundaries, and keep payloads minimal. <br>
Risk: Secrets or sensitive operational data could be exposed through webhooks, logs, or chat relay messages. <br>
Mitigation: Send summaries instead of raw secrets, avoid secrets in payloads and logs, and verify failure paths for leakage. <br>
Risk: Publishing endpoints, changing firewall rules, or adding persistent cron delivery can expand the deployment's exposure. <br>
Mitigation: Require explicit approval before exposure changes and test messages before production use. <br>
Risk: Assuming native OpenClaw-to-OpenClaw federation or shared session state could lead to unreliable designs. <br>
Mitigation: Use only documented OpenClaw commands and delivery modes, and make ownership, retries, and idempotency explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClawdPI-AI/openclaw-peer-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bridge design memos, message schemas, cron payload definitions, webhook contracts, rollout plans, and troubleshooting checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation snippets and approval gates; no automatic system changes] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
