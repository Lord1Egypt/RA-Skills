## Description: <br>
Payclaw is a CLI skill for OpenClaw agents to configure Circle wallet workflows, send or request testnet USDC, and manage local payment, escrow, and agent directory records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rojasjuniore](https://clawhub.ai/user/rojasjuniore) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use Payclaw to add testnet USDC wallet, payment request, payment history, and agent-directory workflows to OpenClaw agent experiments. It is most appropriate for trusted test environments where recipients, amounts, and release decisions can be manually verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says Payclaw has escrow claims and should not be treated as real escrow. <br>
Mitigation: Use it only in a trusted test environment and manually verify every escrow recipient, amount, and release or refund decision. <br>
Risk: The security review flags shell-based command execution and insufficient input validation around wallet names, addresses, amounts, memos, and API-key strings. <br>
Mitigation: Avoid untrusted inputs and use a low-risk Circle testnet API key until command construction and validation are fixed. <br>


## Reference(s): <br>
- [Payclaw ClawHub listing](https://clawhub.ai/rojasjuniore/payclaw) <br>
- [Payclaw homepage](https://github.com/rojasjuniore/payclaw) <br>
- [Moltbook profile](https://moltbook.com/u/JuniorClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output and Markdown documentation with bash and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files under the user's OpenClaw configuration directory and delegates wallet operations to the circle-wallet command.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
