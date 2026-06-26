## Description: <br>
Interprets sell-side research for industries, sectors, concepts, and themes by using the investoday finance data interface to identify the requested entity and produce a structured sector research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance research users and agents use this skill to summarize sell-side views for industries, sectors, concepts, and themes. It identifies the requested sector or concept through the investoday-finance-data dependency, retrieves recent research sentiment, and returns structured consensus, disagreement, opportunity, risk, and follow-up observation points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated sector research summary may be mistaken for personalized investment advice. <br>
Mitigation: Present findings as market research only, avoid buy or sell instructions, target prices, position sizing, and trade timing, and preserve the skill's evidence and disclaimer constraints. <br>
Risk: Sector consensus can be overstated when the retrieved research sample is sparse or one-sided. <br>
Mitigation: Require repeated evidence before labeling a view as consensus, use a clear time window such as recent 90-day research, and state when data is insufficient. <br>
Risk: The skill depends on the separate investoday-finance-data skill for market data and entity recognition. <br>
Mitigation: Confirm the dependency is available before use and ask for a clearer sector, industry, concept, or theme when entity recognition is unstable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-sector-research-interpretation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kenneth-bro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sector research interpretation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses recent sector or concept research sentiment through the investoday-finance-data dependency and should state when available evidence is insufficient.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
