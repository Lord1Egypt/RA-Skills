## Description: <br>
Calculates Monero mining profitability with inputs for hashrate, power, electricity cost, and current market parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumaimiao](https://clawhub.ai/user/liumaimiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to estimate Monero mining earnings, electricity costs, break-even points, and ROI from hardware and market inputs. It is calculation guidance only and does not package mining software. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may assume the referenced monero-profitability command is supplied by this release. <br>
Mitigation: Only run a command with that name after verifying where it came from and trusting its source. <br>
Risk: Profitability estimates depend on volatile market and network parameters. <br>
Mitigation: Refresh XMR price, network difficulty, block reward, electricity rate, and pool fee inputs before making mining or hardware decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liumaimiao/monero-profit-calculator-2026) <br>
- [CoinGecko Monero API endpoint](https://api.coingecko.com/api/v3/coins/monero) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tables, example shell commands, and an illustrative Python snippet.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable mining code is packaged.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
