## Description: <br>
Market Sentiment Radar analyzes A-share market conditions, sentiment cycles, sector money flow, and cross-market signals to produce a market health report with portfolio exposure guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgetao730](https://clawhub.ai/user/georgetao730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assess whether current A-share market conditions favor trading, defensive positioning, or reduced exposure. It produces a high-level market environment report rather than individual stock recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce concrete trading exposure guidance while some market commentary may be under-sourced. <br>
Mitigation: Verify market, sector, and macro claims independently and treat position sizing as educational commentary rather than investment advice. <br>
Risk: Suggested trading-tool follow-ups could influence real-money trading decisions if followed automatically. <br>
Mitigation: Require explicit human review before using this skill or linked tools to place trades, manage positions, or allocate real capital. <br>
Risk: Reports depend on current market data availability and may be stale, incomplete, or partly estimated when data retrieval is limited. <br>
Mitigation: Confirm the AKShare data timestamp and rerun or stop analysis when data retrieval fails or market inputs cannot be independently confirmed. <br>


## Reference(s): <br>
- [Sentiment Cycles](references/sentiment-cycles.md) <br>
- [Position Mapping](references/position-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown market health report with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market cycle classification, risk level, sector commentary, cross-market commentary, and position sizing guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
