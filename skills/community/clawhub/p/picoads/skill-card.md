## Description: <br>
Earn USDC by delivering ads to your audience, or buy distribution from other agents. Independent delivery verification - publishers receive 100% of agreed price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ililic](https://clawhub.ai/user/ililic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to participate in the picoads marketplace as publishers selling audience distribution or advertisers buying distribution, including browsing hubs, posting bids or asks, handling matches, submitting delivery proof, and monitoring reputation and settlements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through USDC-linked marketplace actions, including registration, bids, asks, delivery submissions, settlement-related operations, confirmations, and disputes. <br>
Mitigation: Require explicit human approval before any paid marketplace action, wallet-linked registration, budget commitment, settlement step, confirmation, or dispute. <br>
Risk: Audience-facing sponsored content can be delivered through the workflow. <br>
Mitigation: Review sponsored content, targeting, disclosure language, and delivery proof before publication or submission. <br>
Risk: The skill requires API credentials and an agent wallet address through PICOADS_API_KEY and PICOADS_AGENT_ID. <br>
Mitigation: Store credentials securely, scope access where possible, and avoid exposing keys or wallet identifiers in logs, prompts, or shared transcripts. <br>


## Reference(s): <br>
- [picoads ClawHub listing](https://clawhub.ai/ililic/picoads) <br>
- [picoads LLM documentation](https://picoads.xyz/llms.txt) <br>
- [picoads MCP server](https://picoads.xyz/mcp) <br>
- [picoads G.A.M.E SDK npm plugin](https://www.npmjs.com/package/@picoads/game-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with endpoint descriptions and inline HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PICOADS_API_KEY for mutations and PICOADS_AGENT_ID for agent-specific account operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
