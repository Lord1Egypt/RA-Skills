## Description: <br>
Guides agents in using the NotebookLM `nlm` CLI and MCP server to manage notebooks, add sources, generate NotebookLM artifacts, conduct research, and query source-backed content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hewenqiang](https://clawhub.ai/user/hewenqiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate NotebookLM programmatically through the `nlm` CLI or NotebookLM MCP tools, including notebook management, source ingestion, research, studio artifact generation, and source-grounded Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notebook and source content may be exposed through NotebookLM operations, public sharing, or collaborator invites. <br>
Mitigation: Use a dedicated Google profile where possible and require explicit user confirmation before enabling public links or inviting collaborators. <br>
Risk: Authentication flows may handle Google session access, including cookie-based fallback paths. <br>
Mitigation: Prefer the normal `nlm login` flow and avoid manually pasting raw cookies unless the user understands and accepts the credential exposure risk. <br>
Risk: Troubleshooting guidance includes broad local execution workarounds such as full-access sandbox mode and browser process termination. <br>
Mitigation: Use the least-permissive sandbox and targeted process management that will work; reserve broad access or broad kill commands for explicit, informed user approval. <br>
Risk: Delete operations for notebooks, sources, artifacts, and authentication profiles can be irreversible. <br>
Mitigation: Show exactly what will be deleted and obtain explicit user confirmation before running delete commands with confirmation flags. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hewenqiang/nlm-notebooklm) <br>
- [NotebookLM CLI - Complete Command Reference](artifact/references/command_reference.md) <br>
- [NotebookLM CLI - Troubleshooting Guide](artifact/references/troubleshooting.md) <br>
- [NotebookLM CLI - Complete Workflow Sequences](artifact/references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include explicit confirmation prompts for destructive or public-sharing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 0.3.19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
