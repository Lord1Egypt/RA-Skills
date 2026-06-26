## Description: <br>
Run an ISO 27001 internal audit by walking through controls by domain, identifying gaps, collecting evidence, and generating findings with corrective action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, security, and audit teams use this skill to scope and run structured ISO 27001:2022 internal audits, assess ISMS and Annex A controls, collect evidence, and draft audit findings with corrective actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected audit evidence can include employee, customer, access-control, and security posture details. <br>
Mitigation: Store evidence only in approved, access-controlled storage and redact unnecessary sensitive details before sharing. <br>
Risk: Evidence collection may require credentials for administrative systems. <br>
Mitigation: Use read-only or least-privilege credentials and prefer API exports over screenshots. <br>
Risk: The optional MCP server sends audit queries to an external endpoint. <br>
Mitigation: Configure the MCP server only if the organization trusts that endpoint; otherwise use the embedded reference files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/iso-27001-internal-audit) <br>
- [Internal ISO Audit](https://internalisoaudit.com) <br>
- [Internal ISO Audit MCP endpoint](https://internalisoaudit.com/api/mcp) <br>
- [Connector setup](CONNECTORS.md) <br>
- [Access control rules](rules/access-control.md) <br>
- [ISMS management rules](rules/isms-management.md) <br>
- [Incident response rules](rules/incident-response.md) <br>
- [Encryption rules](rules/encryption.md) <br>
- [Change management rules](rules/change-management.md) <br>
- [Logging and monitoring rules](rules/logging-monitoring.md) <br>
- [Business continuity rules](rules/business-continuity.md) <br>
- [People controls rules](rules/people-controls.md) <br>
- [Supplier management rules](rules/supplier-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with audit checklists, findings templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an optional compliance MCP server for live control guidance; otherwise uses embedded reference files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
