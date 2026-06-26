## Description: <br>
Create and manage self-rewarding meme coins on Solana via the OP0 Altar protocol, deploying pump.fun tokens where holders automatically receive rewards in 129 payout token options every few BTC blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[op0prot](https://clawhub.ai/user/op0prot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to create, monitor, list, and inspect OP0 Altar token launches on Solana, including reward-token selection and funding-status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use of this skill can initiate real SOL transfers and public token deployment. <br>
Mitigation: Before funding, confirm the returned dev_wallet address, exact SOL amount, token settings, marketing wallet, and 30-minute funding window with the user. <br>
Risk: The OP0 API key authorizes access to OP0 actions. <br>
Mitigation: Keep OP0_API_KEY private and install the skill only when the user trusts OP0 and the op0.live API. <br>
Risk: SOL transfers and token launches may be irreversible after execution. <br>
Mitigation: Present funding and deployment steps as explicit user-confirmed actions and avoid implying that completed transactions can be undone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/op0prot/op0-altar) <br>
- [OP0 public Altar API endpoint](https://api.op0.live/functions/v1/altar-api-public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OP0 API responses, Solana funding instructions, status summaries, and OpenClaw MCP configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
