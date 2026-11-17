## Description:

Search and retrieve markdown documents from local knowledge bases using qmd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsteelerose](https://clawhub.ai/user/davidsteelerose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and knowledge-base users use this skill to search indexed markdown notes, documentation, and transcripts, then retrieve matching documents or passages through qmd CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the global qmd CLI from the upstream repository can expose the user to upstream package trust risk.

Mitigation: Install only after reviewing and trusting the qmd upstream repository.

Risk: Indexing broad private folders may expose sensitive notes or documents through search, embedding, or retrieval workflows.

Mitigation: Use narrow collections, review indexed content before embedding, and avoid LLM-backed query mode for sensitive material unless the provider path is understood.

Risk: Running the qmd MCP server may expose local markdown search and retrieval tools to connected clients.

Mitigation: Run the MCP server only for trusted local clients.

## Reference(s):

- [QMD upstream repository](https://github.com/tobi/qmd)
- [ClawHub skill page](https://clawhub.ai/davidsteelerose/skills/k2ljl-qmd)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline bash code blocks and qmd JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to use qmd with --json for structured search and retrieval output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
