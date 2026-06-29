## Description: <br>
PipRail gives an OpenClaw agent a self-custodial crypto payment wallet with hard spend caps for discovering, quoting, planning, and paying x402 paywalls across supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piprail](https://clawhub.ai/user/piprail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use PipRail to let an agent discover, quote, plan, and optionally pay x402 resources with a self-custodial wallet under configured spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move crypto funds when a user supplies a wallet key and enables payment tools. <br>
Mitigation: Start in read-only mode without PIPRAIL_PRIVATE_KEY; if enabling payments, use a dedicated low-balance wallet and low PIPRAIL_MAX_AMOUNT and PIPRAIL_MAX_TOTAL values. <br>
Risk: The agent may invoke payment actions through the @piprail/mcp package after configuration. <br>
Mitigation: Review the @piprail/mcp npm package or source before trusting it with real funds, and review quoted payment details before allowing payment. <br>


## Reference(s): <br>
- [PipRail homepage](https://piprail.com) <br>
- [PipRail OpenClaw integration docs](https://docs.piprail.com/integrations/openclaw/) <br>
- [@piprail/mcp npm package](https://www.npmjs.com/package/@piprail/mcp) <br>
- [PipRail MCP tools](https://docs.piprail.com/mcp/tools/) <br>
- [PipRail spend controls](https://docs.piprail.com/spend-controls/payment-policy/) <br>
- [PipRail MCP configuration](https://docs.piprail.com/mcp/configuration/) <br>
- [PipRail MCP chains](https://docs.piprail.com/mcp/chains/) <br>
- [ClawHub skill page](https://clawhub.ai/piprail/piprail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MCP tool results and Markdown instructions with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only discovery, quote, budget, guide, register, and receipt verification are available without a wallet key; payment requires explicit wallet and budget configuration.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
