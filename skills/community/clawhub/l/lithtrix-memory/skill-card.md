## Description: <br>
Persistent cross-session memory and verifiable agent identity via the Lithtrix MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[learningloons-hash](https://clawhub.ai/user/learningloons-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an OpenClaw agent to Lithtrix for persistent memory, semantic recall across sessions, and agent passport checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected conversation context and user preferences may be sent to Lithtrix for persistent storage. <br>
Mitigation: Set clear agent rules to store only non-sensitive summaries, avoid secrets and regulated data, and request user consent before saving persistent memory. <br>
Risk: The evidence does not define memory review, deletion, retention, or sensitivity controls. <br>
Mitigation: Confirm review, deletion, and retention processes with Lithtrix or the publisher before production use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/learningloons-hash/lithtrix-memory) <br>
- [Lithtrix documentation](https://docs.lithtrix.ai) <br>
- [Lithtrix MCP on npm](https://www.npmjs.com/package/lithtrix-mcp) <br>
- [Lithtrix trust overview](https://lithtrix.ai/trust.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with shell, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LITHTRIX_API_KEY and may call Lithtrix API or MCP tools for persistent memory and passport lookup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
