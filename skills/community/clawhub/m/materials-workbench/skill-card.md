## Description:

Materials editor workbench - React UI and Express server to render JSON schemas to images and generate schemas with AI (declare-render + materials-agents).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cai-zhuo](https://clawhub.ai/user/cai-zhuo)

### License/Terms of Use:


## Use Case:

Developers and designers use this skill to run a local materials workbench for creating, editing, previewing, and downloading declarative canvas render schemas with optional AI assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts credential-backed local services.

Mitigation: Review before installing, run only on a trusted machine, and avoid exposing port 3001 beyond localhost.

Risk: Images and prompts may be sent to configured AI providers or uploaded to PICUI.

Mitigation: Do not use sensitive images unless you accept transfer to the configured AI provider and PICUI service.

Risk: Dependency scope and provenance are incomplete in the available server evidence.

Mitigation: Prefer packaging audited dependencies inside the artifact or pin reviewed registry versions before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cai-zhuo/skills/materials-workbench)
- [PICUI Image Upload Service](https://picui.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workbench can produce RenderData JSON and downloadable canvas images after the local client and server are running.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
