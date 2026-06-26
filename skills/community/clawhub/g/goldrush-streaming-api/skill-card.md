## Description: <br>
GoldRush Streaming API helps agents guide developers who need real-time blockchain data through GraphQL subscriptions over WebSocket for live price feeds, DEX pair monitoring, wallet activity streaming, token search, trader PnL analysis, and real-time analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gane5h](https://clawhub.ai/user/gane5h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building trading bots, live dashboards, alerts, copy-trading tools, DEX monitoring, and real-time blockchain analytics with the GoldRush Streaming API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GoldRush API keys can be exposed if placed in browser-side code, repositories, logs, screenshots, or shell history. <br>
Mitigation: Store API keys in environment variables or a secret manager and avoid exposing them in client-side code or shared artifacts. <br>
Risk: Wallet activity streaming can create privacy concerns when monitoring addresses without a legitimate purpose. <br>
Mitigation: Monitor only wallet addresses that the user has a legitimate reason to track and limit disclosure of streamed wallet activity. <br>


## Reference(s): <br>
- [GoldRush Streaming API Reference](references/overview.md) <br>
- [Streaming API Endpoints](references/endpoints.md) <br>
- [Streaming API SDK Guide](references/sdk-guide.md) <br>
- [GraphQL over WebSocket Protocol](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md) <br>
- [Covalent TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) <br>
- [Redstone](https://redstone.finance/) <br>
- [ClawHub Release Page](https://clawhub.ai/gane5h/goldrush-streaming-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with TypeScript, GraphQL, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; outputs guidance and implementation examples rather than executing API calls.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
