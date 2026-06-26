## Description: <br>
This skill guides an agent through Pionex spot order placement, cancellation, and order/fill checks using the `pionex-trade-cli` CLI with API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pibrandon](https://clawhub.ai/user/pibrandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading automation operators use this skill to prepare, dry-run, confirm, place, cancel, and review Pionex spot orders through the Pionex CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel real Pionex spot orders. <br>
Mitigation: Use dry-run where supported, confirm the exact symbol, side, order type, size or amount, and cancellation scope with the user before any live write action. <br>
Risk: The skill requires trading-capable API credentials. <br>
Mitigation: Use least-privilege keys, enable IP whitelisting where possible, never share API secrets, and revoke keys when they are no longer needed. <br>
Risk: The skill depends on the Pionex CLI package for trading operations. <br>
Mitigation: Install and use the CLI only when the user trusts the package and its configured account context. <br>


## Reference(s): <br>
- [Pionex API Docs](https://pionex-doc.gitbook.io/apidocs/) <br>
- [Pionex](https://www.pionex.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run command proposals, account-balance checks, and confirmation prompts before live trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
