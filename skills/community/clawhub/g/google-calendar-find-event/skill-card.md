## Description: <br>
Atomic node skill to search for events in Google Calendar using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to search the configured Google Calendar account for events within a bounded time range, optionally filtering by title or subject with the gog CLI query flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar searches can reveal private event titles and metadata from the configured gog account. <br>
Mitigation: Use bounded date ranges, specific calendar scope, and clear query terms; only run the skill where the configured calendar account is appropriate for agent access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-calendar-find-event) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON array returned by the gog CLI, with skill guidance for constructing the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and access to the Google Calendar account configured for that CLI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
