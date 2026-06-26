## Description: <br>
Interprets A-share single-stock research reports by summarizing institutional views, rating changes, core rationale, opportunities, risks, and consensus signals using Investoday finance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-analysis agents use this skill to answer questions about a single A-share stock's recent institutional research coverage, ratings, target-price movement, consensus, disagreements, opportunities, and risks. It is intended to produce informational research summaries, not trading instructions or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be mistaken for investment advice or trading recommendations. <br>
Mitigation: Treat generated reports as informational research summaries only; require human review before using them in financial decisions. <br>
Risk: The skill depends on investoday-finance-data for market data access and freshness. <br>
Mitigation: Install and trust the required dependency, and verify source data availability when conclusions are material. <br>
Risk: Broad finance questions may be routed to a skill optimized for single-stock research-report interpretation. <br>
Mitigation: Use a more specific industry, sector, news, or announcement skill when the user request is outside single-stock research coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-research-interpretation) <br>
- [Publisher profile: kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown research interpretation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured sections cover the conclusion, rating overview, core rationale, consensus and disagreement, opportunities, risks, and follow-up signals.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
