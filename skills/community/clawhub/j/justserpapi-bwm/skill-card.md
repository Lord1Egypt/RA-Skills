## Description: <br>
Search Google web, news, maps, trends, shopping, scholar, finance, hotel, and media surfaces through Just Serp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external agents use this skill to collect structured Google result data for search research, competitive intelligence, trend monitoring, local business lookups, shopping analysis, and scholar analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, location filters, place IDs, and similar lookup parameters are sent to Just Serp API. <br>
Mitigation: Avoid highly sensitive internal queries or private URLs, and use the skill only when sharing those lookup parameters with Just Serp API is acceptable. <br>
Risk: The skill requires the sensitive JUST_SERP_API_KEY credential. <br>
Mitigation: Keep the API key private and avoid exposing it in chat messages, screenshots, logs, or process listings on shared machines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blueworldmarketing/justserpapi-bwm) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured API response summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill calls read-only GET operations and typically summarizes Google result patterns before exposing raw JSON when useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
