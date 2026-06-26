## Description: <br>
OpenClaw安全审计与防护 helps agents record sensitive operations, generate audit reports, inspect operation history, analyze security risks, require two-stage confirmation, scan external content, and verify skill file integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangdongmingisok](https://clawhub.ai/user/yangdongmingisok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add audit logging, high-risk operation review, activity reports, content checks, rate monitoring, operation-chain analysis, URL allowlisting, and skill integrity checks to OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive audit, approval, and alert data to fixed Feishu accounts using embedded credentials and recipient identifiers. <br>
Mitigation: Replace embedded Feishu credentials and recipient or chat IDs with secure runtime configuration, disable external reporting by default, and redact sensitive fields before sending notifications. <br>
Risk: Confirmation replies may be ambiguous if they are not bound to a unique request ID. <br>
Mitigation: Require approval replies to include the unique confirmation request ID, reject stale or unmatched replies, and expire pending confirmations on a short timeout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangdongmingisok/openclaw-audit-log) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSONL audit records, Markdown audit reports, Feishu notification content, confirmation state files, hash baselines, URL allowlist checks, and security-review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
