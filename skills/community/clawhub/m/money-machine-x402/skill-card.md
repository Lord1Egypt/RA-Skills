## Description: <br>
Money Machine x402 API provides paid x402 endpoints for trading signals, crypto analytics, token safety checks, arbitrage scans, sentiment, and sports picks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to discover and call paid x402 API endpoints for crypto market signals, token safety checks, arbitrage scans, sentiment data, and sports picks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid API access from a wallet for broad everyday requests without a documented default spending cap or required per-call confirmation. <br>
Mitigation: Use a dedicated low-balance wallet, configure strict per-call and daily caps, allowlist recipients, and require explicit confirmation before each paid call. <br>
Risk: Trading, crypto, betting, and financial-analysis outputs may be mistaken for investment or wagering advice. <br>
Mitigation: Treat paid API responses as informational signals only and require human review before financial, trading, or betting decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/money-machine-x402) <br>
- [Money Machine API ping endpoint](https://money-machine-api-ssyopros.zocomputer.io/api/ping) <br>
- [Money Machine BTC signal endpoint example](https://money-machine-api-ssyopros.zocomputer.io/api/signals/BTC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with endpoint tables and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid endpoint responses are accessed through x402 micropayments; callers should apply spending controls before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
