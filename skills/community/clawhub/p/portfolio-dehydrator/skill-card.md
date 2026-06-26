## Description: <br>
Portfolio Dehydrator diagnoses Web3 portfolio overlap and generates constrained allocation recommendations using public exchange OHLCV data, Sortino, Calmar, maximum drawdown, and Chinese Markdown reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaozrrr](https://clawhub.ai/user/shaozrrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Web3 analysts use this skill to generate or adapt a Python portfolio optimizer that evaluates token lists or holdings weights, fetches public market data, and produces client-facing allocation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat portfolio analysis as financial advice. <br>
Mitigation: Present outputs as analytical support, include risk disclosure, and require human review before making allocation decisions. <br>
Risk: Wallet secrets or sensitive holdings data could be exposed if entered directly. <br>
Mitigation: Do not enter private keys or wallet secrets; preprocess wallet-derived holdings separately and pass only token symbols and weights. <br>
Risk: Public exchange market-data APIs may be unavailable, rate limited, or incomplete. <br>
Mitigation: Use the documented fallback chain, skip unavailable assets, and avoid synthetic price paths. <br>


## Reference(s): <br>
- [Implementation Spec](references/implementation-spec.md) <br>
- [Bundled Web3 Portfolio Optimizer](assets/web3_portfolio_optimizer.py) <br>
- [Skill Repository](https://github.com/Shaozrrr/portfolio-dehydrator-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/shaozrrr/portfolio-dehydrator) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and requirements code blocks, or a Chinese Markdown portfolio report from the bundled backend] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public exchange market data only; reports include source transparency and data-confidence grading.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
