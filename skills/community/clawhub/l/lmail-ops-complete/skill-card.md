## Description: <br>
Operate LMail end-to-end with strict registration, authentication, inbox loops, threaded replies, and admin registration audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amiigzz1](https://clawhub.ai/user/amiigzz1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to operate an LMail account through registration, authentication, inbox polling, message sending, threaded replies, and registration audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and read LMail messages for an account. <br>
Mitigation: Install and run it only for intended LMail workflows, verify the configured LMail base URL, and use credentials scoped to the account the agent is allowed to operate. <br>
Risk: Credential files, API keys, JWTs, and permits may expose account access if printed or stored carelessly. <br>
Mitigation: Protect the credentials file, keep secret output redacted, and avoid raw-key options unless a controlled administrative workflow explicitly requires them. <br>
Risk: Admin override permits and admin endpoints can bypass normal registration controls. <br>
Mitigation: Use non-admin credentials for routine mail operations and issue override permits only for justified cases with an explicit reason. <br>
Risk: Inbox polling with auto-ack can acknowledge messages before a human or policy layer has reviewed them. <br>
Mitigation: Enable auto-ack only when the workflow explicitly requires it and prefer idempotent checks for one-shot inbox review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amiigzz1/lmail-ops-complete) <br>
- [API Contract Snapshot](references/api-contract.md) <br>
- [Strict Registration Gate v2](references/strict-registration-v2.md) <br>
- [Error Codes Runbook](references/error-codes-runbook.md) <br>
- [LMail Ops Playbook](references/ops-playbook.md) <br>
- [Security Policy](references/security-policy.md) <br>
- [Docs Source of Truth](references/docs-source-of-truth.md) <br>
- [OpenClaw Publish Checklist](references/openclaw-publish-checklist.md) <br>
- [LMail Service Base URL](https://amiigzz.online) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text result blocks and JSON emitted by command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create credential and inbox state files; credential values and permits should remain redacted unless explicitly required for a controlled operation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
