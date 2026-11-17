## Description:

Headteacher helps agents set up and operate a class-management workspace for student records, Feishu Base schema setup, data operations, and Office artifact generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzdame](https://clawhub.ai/user/yzdame)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, headteachers, and their agent operators use this skill to initialize and manage class data, import or update student records, inspect Feishu Base workspaces, and generate working documents such as seat plans, duty schedules, parent communication records, and parent meeting slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify remote Feishu Base workspaces and schemas.

Mitigation: Review Feishu permissions, confirm the tenant and target Base, and preview schema-changing operations before using real student data.

Risk: Local state, logs, or JSON output may expose Feishu Base identifiers or class workspace details.

Mitigation: Keep .headteacher-skill files out of version control, redact shared outputs, and avoid publishing logs that include workspace identifiers.

Risk: Student records may include sensitive contact, address, or identification fields.

Mitigation: Start with test data, minimize displayed sensitive fields, and confirm before importing or syncing personally identifiable student information.

## Reference(s):

- [Schema Manifest](references/schema-manifest.md)
- [Backend Contract](references/backend-contract.md)
- [Feishu Model](references/feishu-model.md)
- [Notion Model](references/notion-model.md)
- [Obsidian Model](references/obsidian-model.md)
- [Artifact Spec](references/artifact-spec.md)
- [ClawHub Skill Page](https://clawhub.ai/yzdame/skills/headteacher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, structured schema plans, JSON/state-file descriptions, and Office artifact generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or register downstream .docx, .xlsx, and .pptx artifacts after structured class data is available.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
