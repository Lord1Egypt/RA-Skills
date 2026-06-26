## Description: <br>
27 tools for DeFi, DEX swaps, cross-chain bridges, Twitter/X, on-chain token data, crypto utilities, and LLM access via x402 micro-payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foodaka](https://clawhub.ai/user/foodaka) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto operators use this skill to access paid MCP tools for DeFi research, unsigned transaction building, swaps, bridges, token analytics, X/Twitter interactions, crypto utilities, and LLM queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm MCP server is unpinned and can change over time. <br>
Mitigation: Review the npm package and repository before installation, and pin or audit the exact package version used in production environments. <br>
Risk: The skill uses a wallet private key for local payment signing and automatic paid calls. <br>
Mitigation: Use a fresh dedicated Base wallet with only funds you are willing to spend, and never use a main wallet private key. <br>
Risk: Paid tool calls can spend USDC without careful user awareness. <br>
Mitigation: Require confirmation before paid calls and remind users of per-call costs before initiating multi-step workflows. <br>
Risk: Twitter/X and LLM tools may expose secrets or sensitive business data through external services. <br>
Mitigation: Avoid sending secrets or sensitive business data through social or LLM tools, and review prompts and post content before submission. <br>


## Reference(s): <br>
- [ClawHub Paytoll listing](https://clawhub.ai/foodaka/paytoll) <br>
- [PayToll homepage](https://paytoll.io) <br>
- [PayToll MCP repository](https://github.com/foodaka/paytoll-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text, markdown] <br>
**Output Format:** [Markdown guidance with MCP tool call results and unsigned transaction data when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool availability may change dynamically through the MCP server; paid calls require a Base wallet funded with USDC and gas.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
