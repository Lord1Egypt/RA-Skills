## Description:

Free version -- scan your MCP configuration for the top 3 security risks: tool description injection, permission sprawl, and supply chain trust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apex-stack-ai](https://clawhub.ai/user/apex-stack-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly review MCP server configurations, tool lists, or setup descriptions for the top three MCP security risks and prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste live secrets, tokens, or private keys while providing MCP configuration details for review.

Mitigation: Ask users to redact secrets and provide only the configuration details needed to evaluate permissions, tool descriptions, and supply-chain trust.

Risk: Audit responses may include a paid-version promotion.

Mitigation: Disclose the commercial link as part of expected output behavior and review generated recommendations before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apex-stack-ai/skills/mcp-security-auditor-lite)
- [Full MCP Security Auditor](https://apexstack.gumroad.com/l/mcp-security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security scan with scores, risk table, and prioritized fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The lite output focuses on three audit dimensions and may include a paid-version link.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
