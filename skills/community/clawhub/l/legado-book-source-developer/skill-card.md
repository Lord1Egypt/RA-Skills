## Description:

Legado (阅读) Android app book source development skill for creating book sources for novel and manga websites, debugging source rules, querying Legado rule knowledge, and analyzing website HTML structure for authorized targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuluoxci](https://clawhub.ai/user/yuluoxci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced Legado users use this skill to create, validate, debug, and share Legado book-source JSON for websites they own or are authorized to test. It supports HTML structure analysis, encoding handling, CSS selector rules, ruleSearch/ruleToc/ruleContent/ruleBookInfo configuration, and book-source validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete source configurations can be uploaded to a public third-party host, which may expose sensitive headers, cookies, session IDs, private endpoints, passwords, or proprietary rules.

Mitigation: Review every source configuration before upload and remove credentials, Authorization headers, cookies, session data, private endpoints, and proprietary rules.

Risk: Website analysis and anti-bot bypass materials can be misused against sites without permission.

Mitigation: Use the skill only on websites the user owns or is explicitly authorized to test, and avoid anti-bot bypass workflows unless permission is clear.

## Reference(s):

- [Legado Development Guide](references/legado_development_guide.md)
- [Legado Data Structures](references/legado_data_structures.md)
- [Legado Book Source Complete Guide](references/Legado书源开发完整指南.md)
- [User Interaction Guide](references/用户交互指南.md)
- [Tool Usage Guide](references/工具使用说明.md)
- [No-Python Workflow](references/no_python_workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON book-source configurations and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Legado book-source JSON arrays and validation or analysis notes for authorized targets.]

## Skill Version(s):

2.3.7 (source: target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
