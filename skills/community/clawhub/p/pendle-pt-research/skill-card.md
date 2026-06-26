## Description: <br>
Research Pendle PT (principal token) markets, including unlevered hold-to-par ideas, near-expiry rotations, and looped PT strategies across money markets like Morpho and Euler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moshu](https://clawhub.ai/user/moshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi researchers and agent users use this skill to evaluate Pendle principal token markets, compare natural PT yields against practical loopability, and produce decision-oriented rankings for hold-to-par, near-expiry rotation, and looped PT strategies. Outputs should be treated as research inputs rather than financial advice or trade execution confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rankings or loop routes may be mistaken for financial advice or executable trade instructions. <br>
Mitigation: Treat outputs as research only and independently verify market support, liquidity, utilization, borrow rates, liquidation risk, and wallet transaction details before using capital. <br>
Risk: Leveraged PT loops can be sensitive to borrow costs, liquidity changes, and liquidation thresholds. <br>
Mitigation: Use conservative sizing and buffers, and re-check current market conditions before taking action. <br>


## Reference(s): <br>
- [Pendle PT markets](https://app.pendle.finance/trade/markets) <br>
- [Pendle PT ranking framework](artifact/references/ranking-framework.md) <br>
- [Manual Contango PT comparison framework](artifact/references/manual-contango-comparison.md) <br>
- [ClawHub skill page](https://clawhub.ai/moshu/pendle-pt-research) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/moshu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown or bullet-list research reports, with optional shell commands and local JSON data snapshots from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked market buckets, risk tiers, liquidity notes, loop support status, borrow-market details, and practical execution guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
