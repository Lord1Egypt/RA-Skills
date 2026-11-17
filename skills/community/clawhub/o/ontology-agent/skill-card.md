## Description:

Ontology Agent turns a company description into a portable business ontology with knowledge, logic, and decision layers plus an AI expert team and optional DingTalk, WeCom, and Feishu connectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontoai](https://clawhub.ai/user/ontoai)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, founders, and developers use this skill to model a company as a runnable agent system, generate a persistent company instance and department expert team, and export or integrate the resulting ontology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores company instance data, memory logs, and operational database files.

Mitigation: Start with a test company, avoid entering credentials or sensitive PII, and inspect ~/.workbuddy/company-data for stored instance, memory, and database files before real use.

Risk: Proactive monitoring is enabled by default and has incomplete scoping and retention controls in the security evidence.

Mitigation: Disable monitoring or scope it to approved domains before using the skill in a real workspace.

Risk: Sync and export scripts can operate on local directories and produce portable bundles.

Mitigation: Run sync and export scripts only against intended directories and review generated bundles before sharing or importing them elsewhere.

Risk: Real IM or knowledge-base integrations may become active after credentials are configured.

Mitigation: Do not add production credentials until the connectors, permissions, and target workspace have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ontoai/skills/ontology-agent)
- [Official site](https://ontoagent.net)
- [README](README.md)
- [Onboarding guide](GUIDE.md)
- [Product introduction](references/product_intro.md)
- [Deployment reference](references/deployment.yaml)
- [Portability reference](references/portability.md)
- [Connector reference](connectors/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML configuration, Python command examples, and generated local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local instance, memory log, SQLite database, expert package, and export bundle files when the user runs included scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
