## Description:

Use this skill when users need KVcore CRM actions through MCP/CLI (contacts, tags, notes, calls, email, text, campaigns), including raw endpoint access and optional Twilio call fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Developers and CRM operators use this skill to perform KVcore contact, tag, note, call, email, text, campaign, and raw endpoint actions through MCP tools or CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad KVcore and Twilio access could send messages, place calls, change CRM records, refresh campaigns, or call raw endpoints unexpectedly.

Mitigation: Require explicit user confirmation before messaging, calling, changing contacts or tags, refreshing campaigns, or using raw API endpoints.

Risk: KVcore and Twilio credentials could grant sensitive CRM and communications access if over-scoped or exposed.

Mitigation: Use least-privilege credentials and store secrets only in secure environment storage.

## Reference(s):

- [KVcore API base URL](https://api.kvcore.com)
- [ClawHub skill page](https://clawhub.ai/danielfoch/skills/kvcore-mcp-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe MCP tool calls, KVcore CLI commands, raw API requests, and credential setup steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
