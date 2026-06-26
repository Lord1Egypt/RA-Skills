## Description: <br>
Breaking news and Polymarket market correlation analysis for scanning major news, tracking prediction-market probability changes, and finding related markets and smart-money movements for user-provided events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to connect current news with active Polymarket markets, probability movement, volume changes, and public large-order signals. It supports proactive news radar requests and event-specific related-market discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on current web search and market data, so news, probability, volume, or large-order results may be incomplete or unavailable. <br>
Mitigation: Require source URLs for news items, use only data returned by the shared data layer or Gamma API, and state clearly when data cannot be found. <br>
Risk: The skill may display public wallet-address trade summaries when analyzing large orders. <br>
Mitigation: Limit wallet discussion to public market-trade context, mark unverified profiles as unclassified, and avoid inferring real-world identity. <br>
Risk: The skill relies on a separate polymarket-data-layer dependency for market and trade queries. <br>
Mitigation: Review the dependency and its connection methods before use, as recommended by the security guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cnica/polymarket-predictradar-news-impact-skills) <br>
- [Polymarket event URL format](https://polymarket.com/event/{slug}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis with news summaries, source links, market links, probability changes, volume summaries, and large-order notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public wallet-address trade summaries when relevant; all probability and volume values should come from the shared data layer or Gamma API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
