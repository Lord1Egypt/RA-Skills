## Description:

Provides agents with full-function guidance for operating private Tencent Lexiang knowledge-base instances, including search, reading, document creation, block editing, file upload, external imports, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexiang](https://clawhub.ai/user/lexiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise knowledge workers use this skill to let an agent operate private Lexiang knowledge-base deployments: search and read content, create or edit pages, manage files, import meeting recordings, and guide MCP configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Lexiang token may allow the agent to read and modify private enterprise knowledge-base content.

Mitigation: Install only for trusted Lexiang MCP endpoints, prefer least-privilege tokens, and test in a non-production space before broad use.

Risk: File upload and folder sync workflows can transmit local files, including unintended secrets or regulated data.

Mitigation: Verify exact local paths before upload or sync, use dry-run planning where available, and exclude folders containing secrets or regulated data.

Risk: Presigned upload URLs may send file data to an unexpected destination if not checked.

Mitigation: Confirm the destination host for each presigned upload URL before transmitting file contents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lexiang/skills/lexiang-private-skills)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Lexiang MCP Base Reference](artifact/references/base.md)
- [Setup Guide](artifact/references/setup.md)
- [Search and Browse Reference](artifact/references/search.md)
- [Document Writing Reference](artifact/references/writer.md)
- [Block Operations Reference](artifact/references/blocks.md)
- [File Upload Reference](artifact/references/files.md)
- [External Import Reference](artifact/references/connectors.md)
- [Script Usage Reference](artifact/scripts/README.md)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with MCP tool-call parameters, JSON configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP call arguments, generated access links, and file upload plans.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
