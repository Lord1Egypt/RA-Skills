## Description:

This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API for local business research, lead generation, competitor analysis, ratings checks, contact retrieval, and directory building.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, sales teams, and analysts use this skill to query Google Maps through BrowserAct and collect structured local business data such as names, categories, addresses, phone numbers, websites, ratings, review counts, and business status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BrowserAct API key and may prompt the user to provide one.

Mitigation: Configure BROWSERACT_API_KEY as an environment secret and avoid pasting credentials into chat.

Risk: The skill automates Google Maps business-contact extraction for uses such as outreach or CRM import.

Mitigation: Confirm that scraping, storing, and using business contact data is allowed by applicable laws, platform terms, and organizational policy before use.

Risk: The security verdict is suspicious because the skill broadly encourages automated business-contact scraping.

Mitigation: Review the skill before installation and limit use to approved data collection workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/google-maps-api-skill)
- [BrowserAct Console Integrations](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API Endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Terminal text with structured business records returned from the BrowserAct API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and the BROWSERACT_API_KEY environment variable; task status is streamed while the BrowserAct workflow runs.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
