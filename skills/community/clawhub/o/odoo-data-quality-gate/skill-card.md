## Description: <br>
Audit an Odoo database's data quality with evidence before trusting AI answers, importing, or migrating -- duplicates, missing required values, orphaned references, format anomalies -- and drive remediation through odoo-mcp's gated write workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanle96](https://clawhub.ai/user/tuanle96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ERP operators, and migration teams use this skill to audit Odoo data quality before relying on AI answers, imports, or migrations. It guides evidence-based remediation planning and gated write approval through odoo-mcp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect sensitive Odoo business records through odoo-mcp. <br>
Mitigation: Install only for environments where this database access is intended, and respect redacted fields and field ACLs in tool responses. <br>
Risk: Remediation proposals could change production records if write gates are enabled and approved without review. <br>
Mitigation: Keep writes disabled by default, require previewed diffs for exact record-id batches, and confirm each approved batch before execution. <br>
Risk: A partial audit could be mistaken for a complete data-quality verdict when checks error or access is limited. <br>
Mitigation: Report errored checks and access-diagnosis results explicitly, and re-run the data-quality report after remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanle96/skills/odoo-data-quality-gate) <br>
- [Publisher profile](https://clawhub.ai/user/tuanle96) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and remediation plans with inline tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-model verdicts, issue evidence, batch remediation proposals, and before/after issue counts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
