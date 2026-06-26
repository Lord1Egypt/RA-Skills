## Description: <br>
Detects significant Polymarket probability movements over configurable time windows, explains possible causes with current news, and helps users manage local movement alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to identify active Polymarket prediction markets with large recent probability changes, investigate possible news-driven causes, and configure movement alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movement analysis depends on the separate polymarket-data-layer skill and current market data availability. <br>
Mitigation: Review the polymarket-data-layer skill before installation and report unavailable data explicitly instead of fabricating market results. <br>
Risk: Alert settings persist locally in scripts/state/alerts.json and may expose monitoring preferences in shared environments. <br>
Mitigation: Review, edit, disable, or delete alert records as needed, and avoid sensitive notes in shared workspaces. <br>
Risk: Possible-cause explanations can be speculative when no relevant current news source is found. <br>
Mitigation: Cite source links when available and label unsourced explanations as AI speculation and unverified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnica/polymarket-predictradar-market-movers-skills) <br>
- [Publisher profile](https://clawhub.ai/user/cnica) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown movement leaderboards, alert confirmations, and concise explanatory guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local alert configuration in scripts/state/alerts.json; market results depend on the separate polymarket-data-layer skill and current data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
