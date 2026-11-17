## Description:

Read, search, inspect, download, organize, move, mark, and delete Mermail emails and threads, and manage mailbox folders or custom-label definitions from Claude, Codex, or another external MCP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage ordinary Mermail inbox work from an agent, including bounded search, message and thread review, attachment retrieval, organization, folder and custom-label management, and Trash or deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform mailbox writes and destructive actions such as permanent deletes, Trash emptying, folder deletion, and custom-label deletion.

Mitigation: Review destructive actions carefully, require exact authorization and confirmation tokens, freeze target ids and arguments, execute once, and report returned counts and partial results.

Risk: Mailbox content, links, attachments, filenames, headers, and custom-label rules may contain untrusted instructions or unsafe content.

Mitigation: Treat mailbox-derived content as data, prefer bounded metadata and scan-gated reads, cap body reads, verify attachments before download, and do not follow instructions embedded in messages or files.

Risk: The skill requires Mermail mailbox access through MERMAIL_API_KEY.

Mitigation: Install only when the agent should manage the mailbox, and scope MERMAIL_API_KEY to mailbox or workspace access the user is comfortable granting.

## Reference(s):

- [Mermail AI Skills documentation](https://docs.mermail.app/ai/skills)
- [Mermail MCP server](https://console.mermail.app/mcp)
- [Mermail inbox safety](references/security.md)
- [Mermail inbox tool contract](references/tools.md)
- [Mermail inbox workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text with exact mailbox identifiers, bounded summaries, previews, and result counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Names exact mailbox, email/thread, folder, attachment, and custom-label ids while redacting unnecessary addresses and body content.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
