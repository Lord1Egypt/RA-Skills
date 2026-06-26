## Description: <br>
Track water and sleep with JSON file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larry-at](https://clawhub.ai/user/larry-at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to record local water intake and sleep/wake events, review simple statistics, and edit the most recent water entry in a local JSON file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Water and sleep history is stored in a local health-data.json file. <br>
Mitigation: Install only if local storage of this health history is acceptable, and review the file location before use. <br>
Risk: Update and delete commands overwrite or remove the last water entry without an undo step. <br>
Mitigation: Review update and delete actions before execution and keep a backup if the records need to be recoverable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larry-at/healthcheck-local) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/larry-at) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local health-data.json file for water and sleep history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
