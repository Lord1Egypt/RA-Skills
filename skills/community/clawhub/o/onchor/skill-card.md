## Description: <br>
API marketplace for AI agents. Browse, buy, sell APIs, and call them via CLI, MCP, or raw HTTP with USDC on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sosa782](https://clawhub.ai/user/sosa782) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to discover, subscribe to, call, publish, and manage marketplace APIs through Onchor. It can also guide agents through account setup, balance checks, USDC-funded purchases, seller listings, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use an Onchor account token that controls an account capable of holding, spending, and withdrawing USDC. <br>
Mitigation: Store the oat_ token only in a secure secret store, keep it out of chat history and logs, and rotate or revoke it if exposed. <br>
Risk: Marketplace calls, purchases, subscriptions, listing changes, wallet or webhook changes, and withdrawals can have financial or account-control impact. <br>
Mitigation: Require explicit human approval before every paid action, seller listing edit or delete, wallet or webhook update, and withdrawal. <br>
Risk: The skill recommends using an npm CLI or MCP server, which adds supply-chain and runtime trust concerns. <br>
Mitigation: Verify the package identity and version before execution and prefer pinned, reviewed installations in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sosa782/onchor) <br>
- [Publisher profile](https://clawhub.ai/user/sosa782) <br>
- [Onchor homepage](https://onchor.xyz) <br>
- [Onchor API base](https://api.onchor.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated CLI, MCP, or curl workflows that can spend or withdraw USDC when used with account credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: skill frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
