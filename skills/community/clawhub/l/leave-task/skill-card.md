## Description: <br>
Helps an agent guide a user through leaving or unassigning from an accepted OpenAnt task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenAnt users and their agents use this skill when they need to leave an accepted task, confirm the task state, and understand the reputation consequences before unassigning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unassigning from a task can reopen it for others and count against the user's OpenAnt reputation. <br>
Mitigation: Before approving an unassign action, verify the task ID, title, reward, and status, then confirm the user understands the reputation impact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/leave-task) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash commands and confirmation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured JSON output from the OpenAnt CLI where commands are run.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
