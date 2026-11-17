## Description:

Linkly AI lets agents search, browse, read, and take notes across Linkly-indexed local documents, linked cloud libraries, OCR text, transcripts, and local Markdown notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkly-ai](https://clawhub.ai/user/linkly-ai)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external users use this skill to let an agent locate, enumerate, summarize, and read content in Linkly-indexed local or cloud document libraries, then save short local notes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to search and read Linkly-indexed local documents, linked cloud libraries, OCR text, transcripts, and local notes.

Mitigation: Install it only when that document access is intended, and review indexed folders plus cloud-library connections before use.

Risk: LAN tokens or a Linkly API key enable additional connection modes.

Mitigation: Provide those credentials only when the LAN or remote gateway mode is intentionally needed.

Risk: The skill can create or edit local Markdown notes at the user's request.

Mitigation: Use note-writing operations only for user-requested note capture, and rely on the documented base-version flow before editing existing notes.

## Reference(s):

- [Linkly AI Skill Page](https://clawhub.ai/linkly-ai/skills/linkly-ai)
- [Install Linkly AI CLI](https://linkly.ai/docs/en/use-cli)
- [Linkly AI MCP Gateway](https://mcp.linkly.ai)
- [Linkly AI CLI Reference](references/cli-reference.md)
- [Linkly AI MCP Tools Reference](references/mcp-tools-reference.md)
- [Advanced Search Strategies](references/search-strategies.md)
- [Troubleshooting Linkly AI](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document IDs, search result summaries, line-numbered excerpts, troubleshooting steps, and note content.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
