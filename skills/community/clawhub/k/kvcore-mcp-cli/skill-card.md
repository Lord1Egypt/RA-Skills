## Description: <br>
Use this skill when users need KVcore CRM actions through MCP/CLI (contacts, tags, notes, calls, email, text, campaigns), including raw endpoint access and optional Twilio call fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CRM operators use this skill to perform KVcore contact, tag, note, call, email, text, campaign, and raw API actions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change CRM records and trigger outbound email, text, call, campaign, tag, note, and raw API actions. <br>
Mitigation: Use least-privilege KVcore and Twilio credentials, review account scope before installation, and require explicit human confirmation before sending messages, placing calls, changing contacts or tags, refreshing campaigns, or using raw API access. <br>
Risk: The security summary flags broad CRM-changing, outbound messaging, raw API, and Twilio call powers without enough scoping or user-control guidance. <br>
Mitigation: Review the referenced MCP and CLI implementation source before giving it production credentials, and restrict use to trusted KVcore and Twilio accounts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/danielfoch/kvcore-mcp-cli) <br>
- [KVcore API base URL](https://api.kvcore.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe or execute CRM-changing and outbound communication actions when connected to configured KVcore or Twilio credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
