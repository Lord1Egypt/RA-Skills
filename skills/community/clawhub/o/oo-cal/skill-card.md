## Description: <br>
Cal.com (cal.com). Use this skill for any Cal.com request, including reading, creating, updating, and deleting data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Cal.com schemas and manage bookings, event types, schedules, availability, calendars, attendees, and authenticated profile details through an OOMOL-connected Cal.com account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Cal.com bookings, schedules, event types, destination calendar settings, attendee records, and profile details. <br>
Mitigation: Require user confirmation of the exact target, payload, and expected effect before running write or destructive actions. <br>
Risk: The skill operates through an OAuth-connected Cal.com account and requires sensitive credentials handled by the OOMOL connection. <br>
Mitigation: Use the minimum Cal.com access the user is comfortable granting and install only when OOMOL's oo CLI should operate the account. <br>
Risk: Connector input and output schemas may change over time. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-cal) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Cal.com homepage](https://cal.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution and returns oo CLI JSON responses when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
