## Description: <br>
Calculates estimated Monero mining profitability from hardware, electricity, network, and market inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumaimiao](https://clawhub.ai/user/liumaimiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, miners, and analysts use this skill to estimate XMR earnings, electricity costs, net profit or loss, break-even price, and ROI for candidate mining setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profitability numbers can be misleading if market price, network difficulty, block reward, or electricity inputs are stale or simplified. <br>
Mitigation: Treat outputs as estimates and verify current Monero market, network, and local electricity data before making mining or hardware decisions. <br>
Risk: The artifact includes example Python code that calls CoinGecko for market data. <br>
Mitigation: Review outbound API use and data handling before running adapted code in controlled environments. <br>
Risk: The artifact shows a `monero-profitability` command, but the release evidence reports no included executable code. <br>
Mitigation: Do not install or run a separate command with that name unless its source and behavior are independently trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liumaimiao/monero-profitability-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with command examples, calculation tables, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profitability estimates depend on current market, network, hardware, and electricity inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
