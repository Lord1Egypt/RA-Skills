## Description: <br>
Look up Norwegian waste collection schedules, find providers, search addresses, and retrieve upcoming pickup dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrikkvamme](https://clawhub.ai/user/henrikkvamme) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to identify a Norwegian waste provider for an address, retrieve upcoming pickup schedules, and optionally prepare calendar subscriptions or reminders. <br>

### Deployment Geography for Use: <br>
Norway <br>

## Known Risks and Mitigations: <br>
Risk: Address or location lookup details are sent to henteplan.no when searching for providers and schedules. <br>
Mitigation: Use the skill only when the user is comfortable sending those lookup details to henteplan.no. <br>
Risk: Reminder workflows may store provider and locationId values for recurring automated checks. <br>
Mitigation: Use one-time lookups or ask the agent not to remember provider and locationId values when persistence is not desired. <br>


## Reference(s): <br>
- [Henteplan service](https://henteplan.no) <br>
- [ClawHub skill page](https://clawhub.ai/henrikkvamme/henteplan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with schedule summaries, inline shell commands, and optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include iCal subscription URLs and OpenClaw reminder examples.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
