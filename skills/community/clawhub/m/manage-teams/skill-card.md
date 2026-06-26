## Description: <br>
Create, join, and manage teams on OpenAnt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover public OpenAnt teams, inspect team details, join teams, create teams, and manage team membership through the OpenAnt CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating OpenAnt team operations can create teams, join teams, or change team membership. <br>
Mitigation: Use explicit user prompts for mutating actions and verify team IDs and user IDs before execution. <br>
Risk: Delete and remove-member operations can be destructive. <br>
Mitigation: Confirm delete or remove-member requests with the user before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/manage-teams) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands append --json and may operate on OpenAnt team and user identifiers.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
