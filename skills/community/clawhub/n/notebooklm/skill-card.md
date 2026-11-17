## Description:

NotebookLM helps agents query Google NotebookLM notebooks for citation-backed answers and manage notebooks, sources, Studio content, and quota-aware research workflows through MCP tools or the NotebookLM MCP REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roomi-fields](https://clawhub.ai/user/roomi-fields)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to ask source-grounded questions over NotebookLM notebooks, preserve citations for downstream work, and generate notebook-based study or Studio content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication command installs and runs the NotebookLM MCP npm package without a pinned version.

Mitigation: Install only from a trusted publisher, pin or locally install the package before authentication, and review the package before use.

Risk: The skill uses an authenticated Google NotebookLM session and can send notebook questions through a configured server URL.

Mitigation: Verify the active Google account and NOTEBOOKLM_SERVER_URL before sending questions, and use notebooks and sources appropriate for that account.

Risk: The workflow mentions rotating Google accounts after quota limits.

Mitigation: Use account rotation only when allowed by applicable account, organizational, and service policies.

Risk: Batch exports write answers and citation sidecars to a local vault directory.

Mitigation: Choose a dedicated vault directory with appropriate access controls and avoid storing sensitive notebook excerpts in shared paths.

## Reference(s):

- [HTTP REST API reference](references/rest-api.md)
- [Effective research with NotebookLM](references/research-workflows.md)
- [NotebookLM MCP project](https://github.com/roomi-fields/notebooklm-mcp)
- [RTFM project](https://github.com/roomi-fields/rtfm)
- [ClawHub skill page](https://clawhub.ai/roomi-fields/skills/notebooklm)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses or citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include citation metadata, cited excerpts, notebook identifiers, generated content records, and batch export file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
