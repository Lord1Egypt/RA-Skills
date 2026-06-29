## Description: <br>
Ora地图拓客专家 helps agents search map-based business leads by city and keyword, retrieve contact-rich business listings, and present analysis from the returned JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oraagent](https://clawhub.ai/user/oraagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, export, and business development users use this skill to run one city-and-keyword map lead search and review returned businesses, contacts, websites, emails, phone numbers, and social links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords, approximate city coordinates, and any OraAgent API key are sent to the provider API. <br>
Mitigation: Install only when this provider data sharing is acceptable, and keep API keys scoped and protected. <br>
Risk: Returned business contact data may be used for outreach that is subject to privacy, anti-spam, and local compliance rules. <br>
Mitigation: Review and handle returned contact data responsibly before using it for sales or marketing activity. <br>
Risk: The skill saves returned business results to local JSON files. <br>
Mitigation: Store, share, and delete result files according to the sensitivity of the contact data they contain. <br>


## Reference(s): <br>
- [Ora地图拓客专家 on ClawHub](https://clawhub.ai/oraagent/ora-map-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown narrative with shell command execution details and references to local JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs one provider API search per request, using a single city and keyword.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
