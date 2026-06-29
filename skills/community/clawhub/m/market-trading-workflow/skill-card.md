## Description: <br>
Conservative World Cup fixture-trading workflow for ClawHub: discover a market, validate the matchup, price the edge, and trade only when safe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[natekohisbetterthanryan](https://clawhub.ai/user/natekohisbetterthanryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to scan World Cup fixture markets, normalize team names, compare model probabilities to market prices, and return a paper-trade, live-trade, or pass decision with a concrete reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that live orders can submit a larger amount than the stake-sized amount shown in the decision output. <br>
Mitigation: Review and fix the live-order amount path before using --live; keep the default paper mode for validation until the submitted amount matches the reported stake-sized amount. <br>
Risk: Live trading and optional wallet or private-key configuration can expose users to financial loss or credential misuse. <br>
Mitigation: Use dry-run or paper trading by default, keep credentials in environment variables only, verify market mapping and fair-probability inputs, and require explicit operator approval before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/natekohisbetterthanryan/market-trading-workflow) <br>
- [Automated slate scan notes](references/automated-slate-scan.md) <br>
- [Simmer SDK compatibility notes](references/simmer-sdk-compat.md) <br>
- [Stake sizing guidance](references/stake-sizing-guidance.md) <br>
- [Team-name normalization notes](references/team-name-normalization.md) <br>
- [World Cup market discovery](references/world-cup-market-discovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON decision reports and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and configured Simmer credentials.] <br>

## Skill Version(s): <br>
1.0.20 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
