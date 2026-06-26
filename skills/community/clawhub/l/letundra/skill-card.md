## Description: <br>
Universal AI travel assistant for visa information, travel and aviation news, RSS feeds, holidays, and currency information from letundra.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leninws](https://clawhub.ai/user/leninws) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-support agents use this skill to answer travel questions about visas, country holidays, exchange rates, aviation news, and Letundra news RSS feeds. It is not intended for booking travel, hotels, or other reservations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel-related country, tag, or currency lookups are sent to letundra.com. <br>
Mitigation: Use the skill only when sharing those lookup terms with Letundra is acceptable. <br>
Risk: Visa and travel requirements can change and may be incomplete or outdated on third-party pages. <br>
Mitigation: Verify critical visa and entry requirements with official government or carrier sources before travel. <br>
Risk: Bundled publishing scripts can publish skills through an authenticated ClawHub account. <br>
Mitigation: Do not run publishing scripts unless you intentionally maintain these skills and understand the authenticated publishing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leninws/letundra) <br>
- [Publisher profile](https://clawhub.ai/user/leninws) <br>
- [Letundra homepage](https://letundra.com) <br>
- [Letundra news page](https://letundra.com/ru/news/) <br>
- [Letundra country page pattern](https://letundra.com/ru/countries/{slug}/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, RSS XML, and concise travel guidance based on fetched Letundra pages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links, dates, tags, visa fields, currency conversion values, holiday lists, and RSS items.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
