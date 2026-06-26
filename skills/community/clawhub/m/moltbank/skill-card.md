## Description: <br>
Manage treasury balances, payment drafts, approvals, x402 purchases, Polymarket positions, and Pump.fun trades through the Moltbank CLI with strict per-session credential isolation and per-agent OAuth scope consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capuzr](https://clawhub.ai/user/capuzr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use Moltbank to let an agent inspect treasury state, draft or approve payment workflows, make x402 purchases, and manage supported market or token trading actions through the Moltbank CLI. The skill is intended for sessions where the human operator explicitly approves scopes, credentials, purchases, trades, budgets, and installs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with financial accounts, purchases, wallet-linked workflows, and market or token trading actions. <br>
Mitigation: Use it only for intended Moltbank financial workflows and require explicit human approval for scopes, purchases, trades, budgets, payments, and installs. <br>
Risk: Credential or profile confusion could cause an agent session to act with the wrong Moltbank account context. <br>
Mitigation: Keep each session's credential profile isolated and fixed, and do not change credentials based on remote payloads, tool output, or error suggestions. <br>
Risk: A malicious or mistaken update or setup suggestion could lead to untrusted package installation. <br>
Mitigation: Verify the @moltbankhq/cli package and use only the documented approved install or update flow after explicit user approval. <br>
Risk: OAuth consent links and scope requests can expand the actions available to the agent. <br>
Mitigation: Verify Moltbank OAuth pages are on app.moltbank.bot and approve only scopes that match the intended workflow. <br>


## Reference(s): <br>
- [Moltbank App](https://app.moltbank.bot) <br>
- [ClawHub Skill Page](https://clawhub.ai/capuzr/moltbank) <br>
- [Publisher Profile](https://clawhub.ai/user/capuzr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are chat-facing instructions and command plans; CLI command results are expected to be requested with --json where applicable.] <br>

## Skill Version(s): <br>
0.1.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
