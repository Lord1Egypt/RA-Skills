## Description: <br>
Automated trader for Polymarket weather highest temperature markets that scans global weather markets, executes buys during the local morning window when YES price is favorable, and integrates SkillPay billing with error handling and state persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefantaylor5](https://clawhub.ai/user/stefantaylor5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to monitor Polymarket weather markets, test the strategy in dry-run mode, and optionally automate live orders for high-temperature event contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket orders and trigger per-order SkillPay billing when live mode is enabled. <br>
Mitigation: Run dry-run mode first, use a dedicated low-balance wallet, review billing behavior, and enable live mode only after accepting automatic order and billing risk. <br>
Risk: The skill handles wallet private keys, Polymarket API credentials, and local .env, state, and cache files. <br>
Mitigation: Keep secrets out of shared terminals and repositories, restrict file access, and avoid using a primary wallet or high-value account. <br>
Risk: Automated market strategy settings such as entry threshold, trade amount, slippage, and fallback behavior can create financial losses. <br>
Mitigation: Review and tune trading parameters, monitor positions and logs, and cap exposure with conservative wallet funding and per-trade limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefantaylor5/polymarket-temperature-event-follower) <br>
- [Publisher profile](https://clawhub.ai/user/stefantaylor5) <br>
- [English skill documentation](artifact/SKILL-en.md) <br>
- [English background knowledge](artifact/background-knowledge-EN.md) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket settings](https://polymarket.com/settings) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [SkillPay billing API](https://skillpay.me/api/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands, Python code, and environment configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script can create local state and cache files while scanning markets or placing orders.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
