## Description:

Rust-native MCP server for fast, local processing of Excel, Word, PowerPoint, and PDF files with reading, writing, form filling, and skill execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdnaimino](https://clawhub.ai/user/xdnaimino)

### License/Terms of Use:

MIT OR Apache-2.0

## Use Case:

Developers and agents use this MCP server to read, transform, and generate Excel, Word, PowerPoint, and PDF documents locally, including document extraction, Office file creation, PDF form filling, and consistency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions fetch and run a local executable with access to document folders.

Mitigation: Install only from a trusted publisher and distribution channel, prefer a pinned and reviewed version, use locked installs where available, and verify release artifacts when checksums are provided.

Risk: Office and PDF workflows may expose or alter personal or business information in local documents.

Mitigation: Run the server only on document folders intended for agent access and review generated or modified Office/PDF files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdnaimino/skills/office-oxide-mcp)
- [Packaged README](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, JSON configuration snippets, shell commands, and Office/PDF files produced through MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or modify local document files when invoked against accessible paths.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
