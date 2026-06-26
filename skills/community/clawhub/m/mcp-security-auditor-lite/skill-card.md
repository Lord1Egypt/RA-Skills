## Description: <br>
Free version - scan your MCP configuration for the top 3 security risks: tool description injection, permission sprawl, and supply chain trust. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apex-stack-ai](https://clawhub.ai/user/apex-stack-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using MCP-connected agents use this skill to review MCP configs, tool lists, or server setups for tool description integrity, permission scope, and supply chain trust. It produces a concise scorecard and top fixes for the three covered audit dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP configs may contain API keys, tokens, private endpoints, or other secrets. <br>
Mitigation: Redact secrets and private infrastructure details before pasting configuration data into an agent session. <br>
Risk: The artifact includes a paid-version Gumroad link that is outside the skill's runtime behavior. <br>
Mitigation: Treat the paid-version link as external marketing and evaluate it separately before purchase or use. <br>
Risk: Checklist-style security scoring may miss issues outside the three covered lite audit dimensions. <br>
Mitigation: Use the output as triage guidance and perform deeper review for additional MCP risks before production deployment. <br>


## Reference(s): <br>
- [ClawHub listing: MCP Security Auditor Lite](https://clawhub.ai/apex-stack-ai/mcp-security-auditor-lite) <br>
- [Full MCP Security Auditor paid version](https://apexstack.gumroad.com/l/mcp-security-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown security scan with a score, risk table, and top fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers three audit dimensions and expects the user to provide an MCP config, tool list, or server setup description.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
