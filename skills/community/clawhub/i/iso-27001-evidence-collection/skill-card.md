## Description: <br>
Collect, organize, and validate evidence for ISO 27001 and SOC 2 audits using API-first commands and structured, timestamped evidence packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Security, compliance, and engineering teams use this skill to identify missing or stale ISO 27001 and SOC 2 evidence, collect platform exports, and organize auditor-ready packages before review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected audit evidence can contain sensitive access, configuration, and control data. <br>
Mitigation: Store evidence in a protected or encrypted location, redact copies shared outside the audit need, and define retention and deletion rules. <br>
Risk: Evidence collection commands may access production cloud, identity, source-control, or endpoint data through existing local credentials. <br>
Mitigation: Run commands only when authorized, use least-privilege read-only accounts where possible, and scope exports narrowly. <br>
Risk: Screenshots and exported reports may expose user identities, roles, or security settings. <br>
Mitigation: Limit sharing to the audit audience and keep clean originals separate from redacted or annotated review copies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/iso-27001-evidence-collection) <br>
- [API export commands by platform](artifact/rules/api-exports.md) <br>
- [Evidence types by control domain](artifact/rules/evidence-types.md) <br>
- [Screenshot evidence guide](artifact/rules/screenshot-guide.md) <br>
- [Internal ISO Audit](https://internalisoaudit.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and evidence index templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides collection of local JSON, CSV, text, image, PDF, and markdown evidence files when commands are followed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
