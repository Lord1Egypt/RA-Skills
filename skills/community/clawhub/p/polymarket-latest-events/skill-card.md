## Description: <br>
Fetch the latest events from Polymarket prediction market. Use when user asks about Polymarket events, prediction markets, trending bets, or wants to see what's new on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaplora](https://clawhub.ai/user/yaplora) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent active Polymarket events, inspect market odds, and build direct event links from public Polymarket Gamma API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad prediction-market or betting-odds questions when the user may mean another platform. <br>
Mitigation: Clarify that the user wants Polymarket results before fetching or presenting market data. <br>
Risk: Market odds and event data can be mistaken for financial advice. <br>
Mitigation: Present results as informational public market data and avoid recommending trades or outcomes. <br>
Risk: Results depend on Polymarket's public API availability and current response format. <br>
Mitigation: Handle failed or changed API responses explicitly and avoid treating missing fields as confirmed facts. <br>


## Reference(s): <br>
- [Polymarket Gamma API events endpoint](https://gamma-api.polymarket.com/events?active=true&closed=false&limit=10&order=createdAt&ascending=false) <br>
- [Polymarket event links](https://polymarket.com/event/{slug}) <br>
- [Polymarket Gamma API tags endpoint](https://gamma-api.polymarket.com/tags?limit=100) <br>
- [Polymarket Gamma API sports endpoint](https://gamma-api.polymarket.com/sports) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown list with event titles, odds, descriptions, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Polymarket Gamma API responses and requires no API key.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
