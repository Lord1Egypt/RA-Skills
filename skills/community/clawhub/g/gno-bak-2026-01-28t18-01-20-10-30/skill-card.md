## Description:

Search local documents, files, notes, and knowledge bases with keyword, semantic, and hybrid search, and generate answers with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoataiza](https://clawhub.ai/user/nicoataiza)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and agent users use this skill to index local document collections, search them with keyword or semantic retrieval, and retrieve or summarize relevant content with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed folders and assistant integrations can expose local document contents to users or tools with access to GNO.

Mitigation: Index only intended folders, review collections before connecting assistants, and confirm MCP status before use.

Risk: The web UI can expose indexed documents if it is bound to a network interface.

Mitigation: Run the web UI on 127.0.0.1 unless deliberate network access is required.

Risk: Write-enabled or forced MCP and skill installation options can broaden access or persist configuration changes.

Mitigation: Use status or dry-run style checks first, and avoid --force and --enable-write unless they are explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoataiza/skills/gno-bak-2026-01-28t18-01-20-10-30)
- [GNO CLI Reference](artifact/cli-reference.md)
- [GNO Usage Examples](artifact/examples.md)
- [GNO MCP Installation](artifact/mcp-reference.md)
- [GNO MCP documentation](https://www.gno.sh/docs/MCP)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from GNO commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local file paths, document URIs, citations, tags, search scores, and MCP configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
