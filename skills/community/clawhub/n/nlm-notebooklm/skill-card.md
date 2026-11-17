## Description:

Expert guide for the NotebookLM CLI (`nlm`) and MCP server, helping agents interact with Google NotebookLM programmatically to manage notebooks, add sources, generate content, research, chat with sources, and automate NotebookLM workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hewenqiang](https://clawhub.ai/user/hewenqiang)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to choose between NotebookLM MCP tools and the `nlm` CLI, authenticate, manage notebooks and sources, generate NotebookLM artifacts, run research workflows, and troubleshoot automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NotebookLM automation may access a user's Google or NotebookLM session.

Mitigation: Install only when that account access is acceptable for the intended environment and account.

Risk: Raw browser cookie headers can expose account session material if pasted into chats, logs, or shared transcripts.

Mitigation: Do not paste raw cookie headers into chats or logs; use safer authentication flows where available.

Risk: Weakening sandbox protections can broaden command and file-system access during automation.

Mitigation: Avoid danger-full-access unless the command, environment, and skill publisher are trusted.

Risk: Public notebook sharing can expose notebook contents through enabled links.

Mitigation: Review public-sharing effects before enabling links and disable public access when it is no longer needed.

Risk: Skill install, update, and uninstall commands change the local agent environment.

Mitigation: Treat skill management commands as administrative changes and review them separately before execution.

## Reference(s):

- [NotebookLM Skill on ClawHub](https://clawhub.ai/hewenqiang/skills/nlm-notebooklm)
- [NotebookLM CLI Command Reference](references/command_reference.md)
- [NotebookLM CLI Troubleshooting Guide](references/troubleshooting.md)
- [NotebookLM CLI Workflow Sequences](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences for authentication, notebook management, source ingestion, generation, export, sharing, and troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 0.3.19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
