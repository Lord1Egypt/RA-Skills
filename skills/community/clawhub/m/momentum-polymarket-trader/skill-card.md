## Description: <br>
Automated Polymarket trading skill based on price momentum signals that executes trades when market trends are detected. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this AION skill template to monitor Polymarket opportunity markets, test or customize momentum-based trading signals, and optionally execute live orders through AION with configured credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can submit real Polymarket trades and may lose funds. <br>
Mitigation: Test in dry-run mode first, require explicit confirmation for live orders, and keep position limits conservative. <br>
Risk: The skill asks for sensitive AION API or wallet credentials. <br>
Mitigation: Prefer simulation or pre-signed EIP712 orders, avoid providing a wallet private key unless it is isolated to funds you are willing to risk, and keep credentials scoped and rotated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skybinjf/momentum-polymarket-trader) <br>
- [AION Documentation](https://docs-t.aionmarket.com/) <br>
- [Building Skills Guide](https://docs-t.aionmarket.com/essentials/building-skills) <br>
- [Polymarket API](https://docs.polymarket.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Plain-text command-line logs with trade decisions, order updates, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode simulates trades by default; live mode can submit real Polymarket orders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
