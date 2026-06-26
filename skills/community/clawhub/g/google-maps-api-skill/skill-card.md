## Description: <br>
This skill helps agents collect structured business listing data from Google Maps through the BrowserAct Google Maps API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to run keyword- and country-biased Google Maps searches for business names, categories, addresses, phone numbers, websites, ratings, review counts, and operational status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The BrowserAct API key could be exposed if pasted into chat or committed with files. <br>
Mitigation: Keep BROWSERACT_API_KEY in environment configuration and avoid sharing the key in conversation or source files. <br>
Risk: Broad or recurring business-contact collection can raise privacy, terms-of-service, or compliance concerns. <br>
Mitigation: Confirm user intent before large lead-generation runs and check applicable privacy, platform, and compliance requirements. <br>
Risk: External API authorization or task failures can interrupt data collection. <br>
Mitigation: Do not retry invalid authorization errors; for other failures, retry once and then report the specific error. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/phheng/google-maps-api-skill) <br>
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Terminal status logs followed by structured text or JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; polls BrowserAct task status and uses the skill-defined retry behavior for non-authorization failures.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
