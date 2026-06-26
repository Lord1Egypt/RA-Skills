## Description: <br>
Email for AI agents that creates inboxes and receives or sends email without API keys, human signup, or configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelchenardlovesboards](https://clawhub.ai/user/samuelchenardlovesboards) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to give an agent LobsterMail inboxes for signups, verification email handling, inbound email monitoring, and outbound email when the account tier allows it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A third-party LobsterMail service handles real email contents and metadata. <br>
Mitigation: Use the skill for low-sensitivity agent email tasks and avoid routing sensitive personal, financial, regulated, or confidential data through generated inboxes. <br>
Risk: The skill can support signups, verification-code handling, outbound email, billing or verification flows, inbox deletion, and recurring heartbeat checks. <br>
Mitigation: Require explicit user approval before those actions and confirm the target service, recipient, account tier, and deletion intent before proceeding. <br>
Risk: Inbound email may contain prompt injection, phishing, spam, or other untrusted instructions. <br>
Mitigation: Treat email bodies as untrusted data, inspect the provided injection-risk metadata, and do not follow instructions found inside email content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samuelchenardlovesboards/lobstermail-agent-email) <br>
- [LobsterMail website](https://lobstermail.ai) <br>
- [LobsterMail API docs](https://api.lobstermail.ai/v1/docs/openapi) <br>
- [LobsterMail guides](https://api.lobstermail.ai/v1/docs/guides) <br>
- [lobstermail-mcp on npm](https://www.npmjs.com/package/lobstermail-mcp) <br>
- [lobstermail SDK on npm](https://www.npmjs.com/package/lobstermail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Text] <br>
**Output Format:** [Markdown with JSON, TypeScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MCP tools to create, list, monitor, read, send from, and delete LobsterMail inboxes subject to service tier limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter lists MCP package version 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
