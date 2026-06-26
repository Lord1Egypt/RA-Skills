## Description: <br>
Run GA4 reports, inspect properties, list audiences and data streams, and analyze traffic and conversion data via the Google Analytics Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analysts use this skill to connect an agent to Google Analytics through ClawLink, discover accessible GA4 properties, run standard or realtime reports, inspect metadata, and review audiences, data streams, key events, and related property settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth credentials and can access GA4 properties available to the connected Google account. <br>
Mitigation: Connect only the intended account, verify the active Google Analytics integration before running tools, and limit use to properties the user is authorized to inspect. <br>
Risk: Configuration or write-capable tools could affect Google Analytics settings if the wrong property, event, or change is approved. <br>
Mitigation: Before any write action, confirm the exact property, event, and intended change with the user; verify GA4 key-event changes in the Google Analytics UI when the API path is unsupported. <br>
Risk: Complex GA4 reports can fail or mislead if dimensions and metrics are incompatible. <br>
Mitigation: Use the compatibility-check workflow before running complex reports and report API errors directly instead of inferring unsupported capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/google-analytics-reporting) <br>
- [GA4 Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [GA4 Dimensions & Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) <br>
- [GA4 Realtime API](https://developers.google.com/analytics/devguides/reporting/realtime/v1) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include GA4 report summaries, setup steps, tool-call parameters, compatibility guidance, and confirmation prompts for write actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
