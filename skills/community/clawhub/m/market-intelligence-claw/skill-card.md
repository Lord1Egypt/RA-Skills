## Description: <br>
Real-time strategic intelligence layer for ecommerce and digital businesses that helps with competitor research, market trends, pricing, keyword research, customer sentiment, brand monitoring, and strategic business decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abhishekj9621](https://clawhub.ai/user/Abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, ecommerce operators, and digital business teams use this skill to plan live market research, compare competitors, assess trends and pricing, monitor brand or industry news, and turn public market signals into actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-research queries may send public keywords, competitor domains, geography, or marketplace choices to external providers. <br>
Mitigation: Review and approve the research plan before calls run, keep unreleased product names and confidential plans out of queries, and confirm the intended marketplace for Amazon research. <br>
Risk: Optional paid APIs can consume credits or incur charges. <br>
Mitigation: Use dedicated low-privilege credentials, configure spending or quota caps, and require explicit approval for paid calls with estimated cost shown in advance. <br>
Risk: Market, pricing, SEO, and sentiment outputs may be incomplete or misleading if provider data is unavailable or estimated from web search. <br>
Mitigation: Treat outputs as decision support, check the listed sources, and prefer configured data providers for higher-confidence metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abhishekj9621/market-intelligence-claw) <br>
- [Competitor Analysis Module](references/competitor.md) <br>
- [Keyword & SEO Intelligence Module](references/keywords-seo.md) <br>
- [Pricing, News, and Sentiment Modules](references/modules-2.md) <br>
- [API Setup Guide](references/setup.md) <br>
- [Trend Analysis Module](references/trends.md) <br>
- [SerpApi](https://serpapi.com) <br>
- [DataForSEO](https://dataforseo.com) <br>
- [Rainforest API](https://rainforestapi.com) <br>
- [NewsAPI](https://newsapi.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown research plans, intelligence reports, setup guidance, and sourced recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include planned external queries, cost estimates, provider names, source lists, and fallback notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
