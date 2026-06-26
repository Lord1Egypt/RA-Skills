## Description: <br>
This skill helps agents extract structured Google Maps review data through BrowserAct's Google Maps Reviews API workflow for local business, reputation, competitor, market, and venue research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect Google Maps reviews for local businesses, venues, brands, chains, and competitors. It supports reputation monitoring, sentiment analysis, market research, service quality audits, and review-based customer insight workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends Google Maps review lookup requests through BrowserAct and may return reviewer-identifying fields. <br>
Mitigation: Use the skill only for explicit review-collection tasks, minimize unnecessary profile or avatar fields in downstream use, and consider applicable Google Maps, BrowserAct, privacy, and data-use obligations. <br>
Risk: The skill depends on a BrowserAct API key and a third-party workflow service. <br>
Mitigation: Confirm BROWSERACT_API_KEY is configured before use, do not retry invalid credentials, and report service errors to the user after the documented single retry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/google-maps-reviews-api-skill) <br>
- [Publisher profile](https://clawhub.ai/user/phheng) <br>
- [BrowserAct Console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Terminal status logs followed by structured review data or JSON returned by the BrowserAct workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY. The review payload may include reviewer names, profile URLs, avatar URLs, ratings, text, dates, and likes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
