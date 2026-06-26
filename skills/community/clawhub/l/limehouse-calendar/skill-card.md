## Description: <br>
Read and write calendar events with granular per-calendar permissions. Users control which calendars an agent can access and whether it can read, create, update, or delete events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MadeleineNakada](https://clawhub.ai/user/MadeleineNakada) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to help users inspect, create, update, and delete calendar events through Limehouse calendar APIs after the user grants calendar-specific permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change user-approved calendars, which may expose private event details or alter calendar data. <br>
Mitigation: Install only if the publisher is trusted, grant the minimum calendars and permissions needed, and confirm exact events before updates or deletes. <br>
Risk: Travel-time routing can process saved home, work, or custom addresses for directions. <br>
Mitigation: Avoid travel-time routing with saved home or work addresses unless the user is comfortable with those locations being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MadeleineNakada/limehouse-calendar) <br>
- [Publisher profile](https://clawhub.ai/user/MadeleineNakada) <br>
- [Limehouse calendar API base](https://cal.limehouse.io/api/v1) <br>
- [Limehouse calendar connection setup](https://cal.limehouse.io/connect) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CAL_API_KEY and curl; API actions depend on user-approved calendar permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
