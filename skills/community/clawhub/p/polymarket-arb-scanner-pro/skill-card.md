## Description: <br>
Scans Polymarket markets for YES and NO price combinations below $1.00 and can optionally submit live buy orders for detected opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to scan Polymarket markets for apparent two-sided arbitrage opportunities and, when explicitly enabled, attempt live execution using a configured wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend wallet funds and may create unintended financial exposure. <br>
Mitigation: Use scan-only mode by default, enable --buy only after review, and run with a dedicated low-balance wallet. <br>
Risk: The artifact claims no leg risk, but execution may not provide true atomic handling or explicit partial-fill recovery. <br>
Mitigation: Do not rely on risk-free or no-position-taken claims unless the execution logic is changed and independently tested for partial-fill recovery. <br>
Risk: Private keys and wallet addresses are read from environment variables or a local .env file. <br>
Mitigation: Keep secrets out of source control and use a dedicated wallet with limited funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/themsquared/polymarket-arb-scanner-pro) <br>
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live trading commands that require wallet environment variables and user-controlled execution flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
