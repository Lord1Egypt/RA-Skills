## Description: <br>
Orchestrate the Life Control CLI skill for OpenClaw agent fleets: initialize the Life Control database, register agent personas, wire Telegram bots, and run daily routines (Morning Alignment, Body Protocol, Financial Pulse, Social Radar, Work Priming, Shutdown). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RachitSharma123](https://clawhub.ai/user/RachitSharma123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up and operate Life Control agent personas for personal tracking across wellness, finance, career, relationships, and related daily routines. It helps initialize the Life Control database, connect Telegram notifications, and coordinate routine scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External scripts and scheduled cron jobs may perform actions outside the visible skill artifact. <br>
Mitigation: Inspect the referenced repository scripts and cron template before installing or enabling scheduled automation. <br>
Risk: Telegram bot tokens and chat identifiers are required for notifications and could expose personal workflow data if mishandled. <br>
Mitigation: Store dedicated Telegram bot tokens outside shell history when possible and confirm how notification data is handled. <br>
Risk: The skill coordinates personal life-tracking data across multiple domains. <br>
Mitigation: Confirm where the Life Control database stores personal data and how scheduled jobs can be stopped. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external repository scripts, cron entries, Telegram bot tokens, and local personal tracking data stores that users should review before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
