## Description: <br>
Loomal capabilities - agent inbox at mailgent.dev, encrypted credential vault with 2FA, calendar, and USDC payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masteratwork](https://clawhub.ai/user/masteratwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with Loomal mail, credential vault, 2FA, calendar, identity signing, and USDC payment workflows under a scope-gated Loomal API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad Loomal API key could allow the agent to access more mail, vault, calendar, identity, or payment tools than the task needs. <br>
Mitigation: Use narrow per-task keys, review granted scopes, and rotate or revoke keys when work is complete. <br>
Risk: Sensitive actions such as sending mail, deleting data, using credentials, making a calendar public, or redeeming payments can have external effects. <br>
Mitigation: Require explicit user review for those actions and confirm the active Loomal identity before sensitive work. <br>


## Reference(s): <br>
- [Loomal](https://loomal.ai) <br>
- [Loomal Console](https://console.loomal.ai) <br>
- [Loomal Documentation](https://docs.loomal.ai) <br>
- [Loomal API Reference](https://docs.loomal.ai/api-reference) <br>
- [@loomal/mcp package](https://www.npmjs.com/package/@loomal/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/masteratwork/loomal-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/masteratwork) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and tool-use guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LOOMAL_API_KEY and an MCP client with npx or bunx available.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
