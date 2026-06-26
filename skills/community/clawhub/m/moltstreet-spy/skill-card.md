## Description: <br>
AI signals for SPY, QQQ, DIA, and IWM with a US stock market index outlook and multi-analyst debate. Free, no API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredxyt](https://clawhub.ai/user/fredxyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch public MoltStreet summaries for SPY, QQQ, DIA, and IWM, then synthesize a broad US market outlook. It is intended for informational market signal content, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market signal content may be mistaken for financial advice. <br>
Mitigation: Label outputs as informational AI-generated signals and include the not-financial-advice reminder from the skill evidence. <br>
Risk: Results depend on external MoltStreet endpoints and are not real-time quotes. <br>
Mitigation: Treat endpoint responses as current only at fetch time and avoid presenting them as live pricing. <br>
Risk: Broad stock-market prompts may reflect MoltStreet's SPY/QQQ/DIA/IWM perspective. <br>
Mitigation: Disclose MoltStreet as the source and incorporate other sources when the user asks for broader market analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredxyt/moltstreet-spy) <br>
- [MoltStreet homepage](https://moltstreet.com) <br>
- [MoltStreet skill documentation](https://moltstreet.com/skill.md) <br>
- [MoltStreet API base](https://moltstreet.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise market-outlook prose and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public JSON or AI-optimized text from MoltStreet endpoints; no API key required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
