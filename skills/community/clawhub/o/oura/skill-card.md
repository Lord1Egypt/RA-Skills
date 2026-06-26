## Description: <br>
This skill helps an agent retrieve and summarize Oura Ring health, sleep, activity, readiness, and biometric data through an authenticated command-line interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruhrpotter](https://clawhub.ai/user/ruhrpotter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People with an Oura account use this skill to let an agent fetch Oura CLI data and answer questions about sleep, readiness, activity, heart rate, and other health metrics. It is most useful when the user wants a natural-language summary of authenticated Oura API data for a specific date or date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Oura data can include sensitive health, sleep, activity, profile, and biometric information. <br>
Mitigation: Use the skill only in conversations where the user is comfortable exposing that information, and summarize only the data needed to answer the request. <br>
Risk: Oura client secrets and token files can grant access to health data if disclosed or mishandled. <br>
Mitigation: Protect the Oura client secret and token file, and prefer a trusted pinned version of the external CLI before installation. <br>


## Reference(s): <br>
- [Oura Ring Integration on ClawHub](https://clawhub.ai/ruhrpotter/oura) <br>
- [Oura Developer Portal](https://cloud.ouraring.com/oauth/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with Oura CLI commands and summarized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Oura CLI and resolves requested dates into YYYY-MM-DD ranges.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
