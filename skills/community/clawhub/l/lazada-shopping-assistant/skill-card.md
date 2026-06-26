## Description: <br>
Lazada Shopping Assistant guides users from buying intent to ranked Lazada product recommendations by detecting the regional site, clarifying usage needs, searching official listings, scraping public product data, and presenting comparison tables with rationale and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gezhi-io](https://clawhub.ai/user/gezhi-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare Lazada products across supported regional sites, using public search-result data to produce concise ranked recommendations before the user decides what to buy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses browser automation or page fetching to collect live public Lazada search results, so prices, availability, and dynamic page data may be incomplete or change quickly. <br>
Mitigation: Review the final Lazada listing before relying on a recommendation, and prefer built-in browser tools where available for more complete page data. <br>
Risk: Shopping workflows can expose account or payment information if the user continues into logged-in checkout flows. <br>
Mitigation: Use the skill for public product discovery only, keep checkout human-controlled, and do not provide Lazada login, payment, or account details to the agent. <br>
Risk: The skill may suggest installing additional browser automation tooling when built-in tools are unavailable. <br>
Mitigation: Install global browser tooling or extra OpenClaw browser skills only from trusted sources and only when that capability is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gezhi-io/lazada-shopping-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, tiered recommendations, clickable product links, and occasional setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Same-language response as the user; product data depends on browser automation or limited page-fetch fallback.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
