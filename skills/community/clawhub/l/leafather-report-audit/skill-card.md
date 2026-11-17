## Description:

Audits data reports by recording figures in a ledger, tracing them to evidence, and blocking delivery when traceability or audit coverage is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wopy112-gao](https://clawhub.ai/user/wopy112-gao)

### License/Terms of Use:

MIT

## Use Case:

Data analysts and report developers use this skill while building, revising, or investigating data reports to record figures in an evidence ledger and check traceability before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked this release suspicious; two referenced files were only partially analyzed and dependency versions could not be verified.

Mitigation: Review the skill's behavior and permissions with someone you trust before installation.

Risk: Use may involve SQL, project-configured modules, source databases, and exported spreadsheets.

Mitigation: Review its handling of these inputs and permissions before running it.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wopy112-gao/skills/leafather-report-audit)
- [Specification](artifact/SPEC.md)
- [Data source and usage notes](artifact/references/usage-notes.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, CSV, JSON, Shell commands]

**Output Format:** [Audit reports and evidence files: audit.md, audit.html, evidence.csv, and manifest.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports disclose audit coverage. HTML and CSV outputs can contain internal metrics and SQL text.]

## Skill Version(s):

3.6.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
