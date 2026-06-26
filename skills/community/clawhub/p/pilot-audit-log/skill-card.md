## Description: <br>
Comprehensive audit trail of all Pilot Protocol activity for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers using Pilot Protocol use this skill to create local audit records for trust decisions, connections, incident review, and compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs may contain sensitive trust decisions, agent identifiers, and connection history. <br>
Mitigation: Set restrictive permissions on ~/.pilot/audit before collecting logs and limit access to users who need audit data. <br>
Risk: Audit logs can persist beyond compliance or privacy requirements if retention is not enforced. <br>
Mitigation: Choose a retention period and add a cleanup process for ~/.pilot/audit before relying on the logs for compliance. <br>
Risk: Handshake examples can interact with agents chosen by the operator. <br>
Mitigation: Run handshake examples only against agents you intentionally select and trust for the audit scenario. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-audit-log) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit-log setup guidance, command wrappers, JSONL event examples, and report-generation snippets for ~/.pilot/audit; requires pilotctl, a running Pilot daemon, and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
