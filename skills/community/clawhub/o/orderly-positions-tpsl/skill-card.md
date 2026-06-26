## Description: <br>
Monitor positions in real-time, configure Take-Profit/Stop-Loss orders, and manage risk with leverage settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill when building Orderly Network position management interfaces that monitor PnL, configure TP/SL orders, adjust leverage, and surface margin or liquidation risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes live trading actions that can affect real funds, including closing positions, changing leverage, placing TP/SL orders, creating stop orders, and canceling orders. <br>
Mitigation: Prefer read-only credentials for monitoring and require an explicit confirmation step before trading actions, showing the symbol, side, size, leverage, trigger prices, reduce-only setting, and liquidation or loss impact. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with TypeScript and REST API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for position monitoring, TP/SL order setup, leverage changes, risk metrics, PnL calculations, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
