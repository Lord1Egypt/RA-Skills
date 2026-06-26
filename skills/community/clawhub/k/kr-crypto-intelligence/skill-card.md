## Description: <br>
Korean crypto, Korean news, and AI analysis data service for trading and content agents, with paid MCP and REST endpoints covering Kimchi Premium, exchange intelligence, market sentiment, K-pop news, semiconductor news, and signed payment receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bakyang2](https://clawhub.ai/user/bakyang2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request Korean crypto market data, Korean market sentiment, and translated Korean news analysis through a remote paid MCP or REST service. It is suited to agents that need exchange intelligence, paid API responses, and receipt records for accountability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid remote tool calls can incur per-call USDC charges through x402-enabled clients. <br>
Mitigation: Keep payment confirmation enabled, configure a spending limit, and start with user-invoked operation until billing behavior is understood. <br>
Risk: Tool calls are sent to an external remote service and may include tool parameters plus normal HTTP metadata. <br>
Mitigation: Avoid sending unnecessary private context and review the MCP client's privacy and transport settings before use. <br>
Risk: Paid response records may need auditability for reconciliation or accountability. <br>
Mitigation: Verify signed receipts against the published receipt signer metadata when audit logs or payment reconciliation are required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bakyang2/kr-crypto-intelligence) <br>
- [MCP endpoint](https://mcp.printmoneylab.com/mcp) <br>
- [API documentation](https://api.printmoneylab.com/docs) <br>
- [x402 receipt metadata](https://api.printmoneylab.com/.well-known/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MCP configuration snippets and remote MCP or REST JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid responses may include ECDSA secp256k1 receipts; calls may require x402 payment authorization through the client.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
