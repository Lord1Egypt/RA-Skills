## Description: <br>
Gmail Lead Desk supports sales and customer-support Gmail workflows through the AISA gateway: OAuth connection, unread lead scans, thread summaries, draft-first replies, confirmed sends, and label-based archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer-support teams use this skill to connect an authorized Gmail account, find unread leads, summarize customer threads, prepare draft replies, and archive closed deals with labels. Agents should use it when the user asks for Gmail lead follow-up, inquiry triage, draft replies, confirmed sends, or deal archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gmail OAuth connection and an AISA API key, which can expose mailbox data if used with the wrong account or mishandled credentials. <br>
Mitigation: Use only Gmail accounts the user is authorized to manage, protect AISA_API_KEY, and confirm the connected account before mailbox actions. <br>
Risk: Sending email, applying labels, archiving messages, or batch mailbox changes can affect real customer communications. <br>
Mitigation: Keep draft-only behavior by default, show the full message or sample affected IDs, and require explicit confirmation before sends, labels, archives, attachments, or cleanup actions. <br>
Risk: Customer messages, attachments, and secrets may be included in prompts or tool calls unnecessarily. <br>
Mitigation: Minimize sensitive content in natural-language prompts, avoid unrelated customer data, and request user consent before downloading or sending attachments. <br>


## Reference(s): <br>
- [Gmail Lead Desk on ClawHub](https://clawhub.ai/aisadocs/gmail-lead-desk) <br>
- [AISA](https://aisa.one) <br>
- [Connect Gmail and execute tools](references/connect_and_execute.md) <br>
- [Gmail Lead Desk Workflows](references/workflows.md) <br>
- [Gmail Tool Whitelist](references/tool_whitelist.md) <br>
- [Gmail API Gotchas](references/gmail_gotchas.md) <br>
- [Composio Gmail documentation](https://docs.composio.dev/toolkits/gmail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, curl examples, structured summaries, draft previews, and API response identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and an authorized Gmail connected account; default workflows stop at drafts unless the user explicitly confirms send or mailbox changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
