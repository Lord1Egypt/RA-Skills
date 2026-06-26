## Description: <br>
Query and analyze website analytics from Plausible Analytics. Use when you need to check real-time visitors, get page views and visitor statistics for a time period, analyze traffic sources or top pages, examine geographic distribution, or generate analytics reports and insights for websites tracked with Plausible Analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site operators, and analytics users use this skill to retrieve Plausible Analytics data for real-time visitors, aggregate traffic metrics, and breakdowns by page, source, device, browser, operating system, or country. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires PLAUSIBLE_API_KEY and sends it as a bearer token when calling Plausible Analytics. <br>
Mitigation: Install only where that key may be exposed to the skill, prefer a limited or read-only key if available, and avoid sharing command output that could reveal credentials or account details. <br>
Risk: Analytics results can include sensitive operational information such as referrers, pages, countries, and traffic counts. <br>
Mitigation: Confirm the intended site ID before running commands and treat returned analytics as sensitive data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ChloePark85/plausible-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and PLAUSIBLE_API_KEY; accepts a Plausible site ID from PLAUSIBLE_SITE_ID or command arguments.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
