## Description: <br>
Scan Simmer markets for a configurable fair-value edge and buy YES or NO when the market price diverges enough from your thesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill as a configurable template for scanning Simmer-indexed prediction markets and preparing or placing trades when market prices diverge from a user-supplied fair probability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run on a schedule and may perform account-changing auto-redemption even when live trading is not enabled. <br>
Mitigation: Install only with a dedicated low-balance account or wallet and review the auto-redemption behavior before deployment. <br>
Risk: Live trading requires sensitive credentials and can place prediction-market orders when explicitly enabled. <br>
Mitigation: Keep dry-run mode as the default, avoid providing WALLET_PRIVATE_KEY unless necessary, and require explicit operator approval before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skybinjf/prediction-fair-value-template) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/skybinjf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; optional settings control market query, fair probability, edge threshold, venue, slippage, and live trading.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
