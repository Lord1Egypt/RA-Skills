## Description:

Guides agents through a three-stage interactive PPT design workflow for requirement confirmation, style previews, full slide generation, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation-building agents, and business users use this skill to manage Chinese-first PPT creation through structured requirements intake, 1-2 page style previews, full generation, and QA before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory QA shell templates can be command-injected through a crafted presentation title.

Mitigation: Use sanitized generated filenames, quote file paths, avoid Python -c string interpolation, and run generation and validation in a least-privilege workspace.

Risk: Chinese-first and optional Japanese vaporwave styling may produce locale or readability mismatches for some audiences.

Mitigation: Review generated slide text, filenames, and style selections against the intended audience and delivery language before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-ppt-design-workflow)
- [Publisher profile](https://clawhub.ai/user/golngod)
- [OPC platform](https://opc.cn)
- [Coze platform](https://coze.cn)
- [Quality checklist](artifact/references/qa_checklist.md)
- [8-style prompt templates](artifact/references/style_templates.md)
- [8-style prompt templates V2.0](artifact/references/style_templates_v2.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, QA checklists, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow that depends on create-ppt generation behavior and user approval gates.]

## Skill Version(s):

1.0.0 (source: server release, target metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
