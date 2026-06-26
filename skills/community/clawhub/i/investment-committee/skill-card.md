## Description: <br>
Investment Committee coordinates five investor-style analysis personas to fetch market data and produce Chinese committee verdict reports for stocks, ETFs, crypto assets, gold, and commodities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitwater](https://clawhub.ai/user/bitwater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze buy decisions, position management, and comparisons across equities, ETFs, crypto assets, gold, and commodities. It produces a Chinese committee-style report with individual viewpoints, scoring, risk notes, and a final verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-generated investment reports and recommendations may be incomplete, incorrect, or based on stale market data. <br>
Mitigation: Independently verify prices, fundamentals, recent news, and recommendations before making financial decisions. <br>
Risk: Reports may be posted to the current Discord channel and saved in workspace history, which can expose personal holdings or investment intent. <br>
Mitigation: Use private channels for sensitive holdings, avoid unnecessary personal details, and review or delete archived reports when needed. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/bitwater/investment-committee) <br>
- [Stooq market data endpoint](https://stooq.com/q/d/l/?s={sym}&d1={d1}&d2={d2}&i=d) <br>
- [Charlie Munger analysis framework](references/munger.md) <br>
- [Howard Marks analysis framework](references/marks.md) <br>
- [Duan Yongping analysis framework](references/duan.md) <br>
- [Stanley Druckenmiller analysis framework](references/druckenmiller.md) <br>
- [James Simons analysis framework](references/simons.md) <br>
- [Committee verdict rules](references/verdict.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown report with supporting shell command usage for market data retrieval] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch market quotes from Stooq and archive generated reports in the workspace history path described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
