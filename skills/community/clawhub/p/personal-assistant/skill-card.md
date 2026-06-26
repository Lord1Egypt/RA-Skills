## Description: <br>
Personal daily briefing and productivity assistant that generates morning briefings with priorities, habits, and self-care reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GustavoZiaugra](https://clawhub.ai/user/GustavoZiaugra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals use this skill to start the day with a structured personal briefing, set top priorities, track daily habits, and close with evening reflection. It supports lightweight personal productivity, routines, and well-being without external dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefings are written to a local output path and may contain routine, location, or productivity details. <br>
Mitigation: Choose an output path you are comfortable storing locally and review the generated file before sharing or syncing it. <br>
Risk: Daily automation can keep generating briefings until the schedule is removed. <br>
Mitigation: Only add the cron schedule when daily generation is intended, and remove the schedule when it is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summary or JSON briefing file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard library only; generated briefings may be saved to a local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
