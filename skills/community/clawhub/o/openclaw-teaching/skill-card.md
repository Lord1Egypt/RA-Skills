## Description:

OpenClaw Teaching helps agents maintain an OpenClaw knowledge base and generate teaching materials as PowerPoint or Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roadherogb](https://clawhub.ai/user/roadherogb)

### License/Terms of Use:

MIT

## Use Case:

Developers, educators, and OpenClaw users use this skill to retrieve OpenClaw platform knowledge, update the bundled knowledge base, and produce tutorial documents or slide decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local import precedence in generate_docs.py could load unintended Python code in some deployments.

Mitigation: Install and run the skill in an isolated environment, or remove the path manipulation before shared deployment.

Risk: Knowledge update, delete, and restore commands can change KNOWLEDGE_BASE.md.

Mitigation: Keep backups, review diffs before publishing updated knowledge, and limit these commands to trusted operators.

Risk: Document generation writes files to caller-supplied output paths.

Mitigation: Use dedicated output directories and review paths before execution to avoid accidental overwrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roadherogb/skills/openclaw-teaching)
- [README](artifact/README.md)
- [OpenClaw knowledge base](artifact/KNOWLEDGE_BASE.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated outputs may include PPTX, DOCX, and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents are written to caller-supplied output paths; knowledge update commands modify the bundled knowledge base and create backups.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
