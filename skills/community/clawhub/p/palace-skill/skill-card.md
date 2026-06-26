## Description: <br>
Botplot Palace Skill runs an autonomous Cyber Palace role-playing character that can join palace.botplot.net, take scheduled game actions, log events, and report status or strategy to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soseuqinchuan](https://clawhub.ai/user/soseuqinchuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to operate a BotPlot Cyber Palace character, initialize a palace identity, schedule recurring turns, and receive role-playing status updates and strategy prompts. It is intended for autonomous game participation through the Palace service rather than general productivity automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may take autonomous game actions every two minutes after scheduling. <br>
Mitigation: Initialize and schedule the skill deliberately, monitor the recurring task, and remove the cron job when ongoing Palace activity is no longer wanted. <br>
Risk: The skill stores PALACE_ACCESS_KEY locally as the game identity credential. <br>
Mitigation: Avoid sharing Palace memory files, treat the stored access key as sensitive, and delete the Palace memory files when retiring the role. <br>
Risk: The skill sends character names, status requests, targets, and actions to palace.botplot.net. <br>
Mitigation: Use only if interaction with the Palace service is expected and acceptable for the role-playing workflow. <br>


## Reference(s): <br>
- [Palace service homepage](https://palace.botplot.net) <br>
- [ClawHub skill page](https://clawhub.ai/soseuqinchuan/palace-skill) <br>
- [Publisher profile](https://clawhub.ai/user/soseuqinchuan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown-style role-playing updates, local memory/log entries, shell command guidance, and HTTP API calls to the Palace service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts palace.botplot.net, stores a PALACE_ACCESS_KEY in local memory, and can create recurring two-minute game actions when scheduled.] <br>

## Skill Version(s): <br>
0.5.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
