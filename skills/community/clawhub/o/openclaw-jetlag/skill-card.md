## Description: <br>
Scans your Google Calendar for upcoming flights and writes a personalized circadian adjustment plan back to your calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chadholdorf](https://clawhub.ai/user/chadholdorf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can run this OpenClaw skill to detect upcoming flight events in Google Calendar and generate a calendar-based jet lag adjustment plan. It is intended for personal travel planning where the user accepts Google Calendar read/write access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires durable Google Calendar read/write access and stores an OAuth token locally. <br>
Mitigation: Install only if that access is acceptable, protect the .env and .oauth-token.json files, and revoke the OAuth grant when the skill is no longer needed. <br>
Risk: Setup guidance includes unsafe credential-sharing advice. <br>
Mitigation: Create dedicated Google OAuth credentials instead of asking another bot or service to reveal a client secret. <br>
Risk: The skill may automatically add many calendar events. <br>
Mitigation: Review the calendar after each run and remove or correct unexpected entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chadholdorf/openclaw-jetlag) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Plain text summary with shell commands and Google Calendar events] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports detected flights, skipped flights, created event counts, or setup and authorization errors; writes circadian adjustment events to Google Calendar when authorized.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
