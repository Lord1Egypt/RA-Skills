## Description: <br>
Apply a research-grade decision pipeline to every investment idea - news-aware bull/bear synthesis, calibrated probability estimation, decision-process audit, Kelly-based position sizing, market-microstructure-aware execution, and concentration discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dpneko](https://clawhub.ai/user/dpneko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate investment research into a structured trade decision workflow covering news synthesis, calibrated probabilities, process review, sizing, execution, and concentration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides high-impact financial decision support, including actionable trading, sizing, and order guidance. <br>
Mitigation: Require independent user review, risk limits, jurisdictional checks, and explicit confirmation before any trade or order preparation. <br>
Risk: The artifact bundles full-text book references, creating possible licensing and redistribution risk. <br>
Mitigation: Confirm rights to redistribute and use the bundled reference material before publishing, installing in shared environments, or commercializing derived releases. <br>
Risk: Investment conclusions can be wrong or stale if market data, filings, news, bid-ask spreads, or scheduled events are missing. <br>
Mitigation: Run fresh data and news checks from the required sources, surface unavailable inputs, and stop before sizing or execution when evidence gaps remain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dpneko/investing-decision-quality) <br>
- [Beat the Market](references/01-thorp-beat-the-market.md) <br>
- [Fortune's Formula](references/02-poundstone-fortunes-formula.md) <br>
- [Superforecasting](references/03-tetlock-superforecasting.md) <br>
- [The Signal and the Noise](references/04-silver-signal-and-the-noise.md) <br>
- [Thinking in Bets](references/05-duke-thinking-in-bets.md) <br>
- [Trading and Exchanges](references/06-harris-trading-and-exchanges.md) <br>
- [Poor Charlie's Almanack](references/07-munger-poor-charlies-almanack.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown decision analysis with checklists, tables, calculations, and cited reference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include position-sizing calculations, execution constraints, risk-limit prompts, and refusal guidance when checklist gates are incomplete.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
