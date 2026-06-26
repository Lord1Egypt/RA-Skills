## Description: <br>
Monitor the Uniswap TokenJar with a real-time dashboard showing balances, accumulation rates, burn economics, and projected time to next profitable burn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and Uniswap protocol operators use this skill to inspect TokenJar balances, fee accumulation, burn economics, and short live monitoring sessions. It is intended for read-only monitoring and analysis, not transaction execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic protocol-fee requests may activate this monitoring skill when the user intended another Uniswap fee workflow. <br>
Mitigation: Confirm the request concerns Uniswap TokenJar monitoring before relying on the dashboard or live updates. <br>
Risk: Profitability projections depend on token prices, gas estimates, and historical accumulation rates that may change quickly. <br>
Mitigation: Treat projections as estimates and refresh the dashboard before making operational decisions. <br>
Risk: The skill is read-only and does not execute burns. <br>
Mitigation: Use an execution-oriented workflow only after independently reviewing the monitoring output and intended transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/monitor-tokenjar) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown dashboard report with optional live update summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only TokenJar balance, accumulation, profitability, history, projection, and alert summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
