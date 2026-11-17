## Description:

Creates Lark/Feishu wiki documents from Markdown content, including headings, rich text, lists, code blocks, and divider blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to create new Lark/Feishu wiki documents from Markdown through a command line workflow or Python API. It is intended for teams that can provision and restrict a Lark tenant app credential for document creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Lark tenant app credential that can create and write wiki documents.

Mitigation: Use a dedicated Lark app scoped to a test or limited wiki space, grant the minimum available document and wiki permissions, and rotate credentials after exposure.

Risk: Supplying secrets through command-line flags or config files can expose them through shell history, logs, or repository contents.

Mitigation: Prefer protected environment variables or a secret manager, keep config files out of source control, and avoid passing app secrets directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/griffithkk3-del/skills/lark-wiki-writer)
- [Lark Open Platform](https://open.larksuite.com/app)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, Python API examples, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and commands for creating Lark wiki documents; runtime execution sends Markdown-derived document blocks to Lark APIs.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
