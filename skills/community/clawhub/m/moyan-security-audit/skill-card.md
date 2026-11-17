## Description:

墨言安全审计 — Agent 生态首个可验证信任验证服务。PMI 四维向量评分 + DecayProof 可验证衰减 + κ_Axiom 自治审计。43 防线 / 7 层纵深防御。支持支付宝/微信/ClawTip AI 支付闭环。64/64 TSC 合规，W3C agent-identity 三方收敛。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to understand and route security-audit work to Moyan's trust-scoring audit service, including its risk categories, paid service tiers, and API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill points to an external paid audit service and API endpoints, which may receive code or other sensitive inputs.

Mitigation: Review the service provider and its data handling terms before sending private code, credentials, customer data, or other sensitive material.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liuyanfeng1234/skills/moyan-security-audit)
- [Moyan service website](https://sixu-ai.net.cn)
- [Moyan security audit documentation](https://github.com/Liuyanfeng1234/agent-os/discussions/38)
- [MCP server reference](https://github.com/modelcontextprotocol/servers/pull/4395)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Analysis]

**Output Format:** [Markdown text with API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May point the agent to an external paid audit service; no bundled executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
