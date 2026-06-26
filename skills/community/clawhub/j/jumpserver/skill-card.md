## Description: <br>
JumpServer Skills helps agents query and analyze JumpServer V4.10 assets, accounts, users, permissions, audit logs, governance signals, and usage reports through formal read-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibuler](https://clawhub.ai/user/ibuler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security administrators use this skill to investigate JumpServer inventory, permissions, access paths, audit activity, and usage trends. It is intended for read-oriented operations, diagnostics, and HTML usage reports rather than business-object or permission changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles JumpServer credentials and sensitive audit or administrative data. <br>
Mitigation: Use a dedicated least-privilege JumpServer account, prefer scoped AK/SK credentials, and protect or delete generated .env and report files. <br>
Risk: TLS verification is documented as disabled by default. <br>
Mitigation: Set JMS_VERIFY_TLS=true unless connecting only to a reviewed and controlled endpoint. <br>
Risk: The runtime may install Python dependencies automatically. <br>
Mitigation: Install dependencies yourself in a controlled virtual environment before deployment. <br>
Risk: Reports and queries can run against the wrong organization if scope is unclear. <br>
Mitigation: Specify the target organization for reports and block execution when candidate organizations or objects remain ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ibuler/jumpserver) <br>
- [README.en.md](README.en.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Routing Playbook](references/routing-playbook.md) <br>
- [Report Template Playbook](references/report-template-playbook.md) <br>
- [Runtime](references/runtime.md) <br>
- [Safety Rules](references/safety-rules.md) <br>
- [Capability Metadata](references/metadata/capabilities.json) <br>
- [Daily Usage Report Template Fields](references/metadata/daily_usage_report_template_fields.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, HTML files, guidance] <br>
**Output Format:** [Markdown responses with command summaries, JSON-backed diagnostics, configuration guidance, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written as HTML files for date or time-range usage analysis; normal queries return summaries and blocking guidance when inputs are ambiguous.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
