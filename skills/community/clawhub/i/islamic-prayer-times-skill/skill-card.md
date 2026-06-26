## Description: <br>
Provides Islamic prayer times, reminders, spiritual todo management, and daily journal entries for OpenClaw users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrrqd](https://clawhub.ai/user/jrrqd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to check Islamic prayer schedules for a city and manage related spiritual productivity tasks. It also records location preferences, todos, journal entries, and reminder settings in local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City names are sent to aladhan.com when fetching prayer times. <br>
Mitigation: Use a nearby city instead of a precise private location when privacy matters, and install only if this third-party API use is acceptable. <br>
Risk: Location, todos, journal entries, and reminder settings are saved locally in OpenClaw memory. <br>
Mitigation: Avoid entering sensitive personal information and review local memory file permissions and contents as part of normal use. <br>
Risk: The skill advertises reminder and Telegram notification behavior that may not be fully implemented by the artifact. <br>
Mitigation: Do not rely on reminders for time-critical obligations unless actual scheduling and notification delivery are verified in the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jrrqd/islamic-prayer-times-skill) <br>
- [Aladhan prayer times API](https://api.aladhan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Plain text responses with Markdown and JSON local state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses city or saved location input, may call aladhan.com, and writes local memory files for location, todos, journal entries, and reminder settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
