## Description: <br>
Display user group memberships on the system. Shows all groups a user belongs to for permission auditing and access control verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and security reviewers use this skill to inspect local Unix group memberships for permission auditing and access-control verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Group names can reveal sensitive access, administrative roles, or permission structure. <br>
Mitigation: Treat output as local security information and avoid sharing results unless the audience is authorized to see access-control details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/groups-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lists local Unix group names for the current or specified user; results can reveal sensitive access or administrative roles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
