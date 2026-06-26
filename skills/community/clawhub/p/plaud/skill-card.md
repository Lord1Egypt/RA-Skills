## Description: <br>
Use when working with Plaud recordings, including /plaud Telegram workflows, listing recent recordings, finding recordings by date or keyword, reading transcripts, summarizing notes, extracting action items, drafting follow-ups, exporting Plaud content, or diagnosing Plaud MCP/CLI authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoniosilveira](https://clawhub.ai/user/antoniosilveira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to work with Plaud recordings through MCP, CLI, and Telegram workflows. It helps list and find recordings, summarize notes and transcripts, extract action items, draft follow-ups, export content, and diagnose authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private Plaud recordings, transcripts, summaries, and notes through authenticated Plaud integrations. <br>
Mitigation: Install only for the intended Plaud account and access only the specific recording, query, or date range needed for the user's task. <br>
Risk: OAuth tokens and Plaud CLI or MCP credentials may grant access to sensitive recording data. <br>
Mitigation: Keep Plaud authentication scoped to trusted environments, limit Telegram bot access to trusted chats, and disconnect or rotate credentials when access is no longer needed. <br>
Risk: Using external Plaud MCP or CLI packages at @latest can change behavior without review. <br>
Mitigation: Pin or review the external Plaud MCP and CLI package versions before deployment in sensitive or repeatable workflows. <br>


## Reference(s): <br>
- [Plaud CLI Reference](references/cli.md) <br>
- [Plaud MCP Reference](references/mcp.md) <br>
- [Plaud Workflow Patterns](references/workflows.md) <br>
- [Plaud MCP documentation](https://docs.plaud.ai/documentation/plaud_app/mcp) <br>
- [Plaud CLI documentation](https://docs.plaud.ai/documentation/plaud_app/cli) <br>
- [Plaud documentation index](https://docs.plaud.ai/llms.txt) <br>
- [Plaud website](https://www.plaud.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and plain text with optional shell commands and exported files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce recording summaries, transcripts, metadata exports, action items, follow-up drafts, and authentication troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
