## Description: <br>
Port Manager tracks and manages system port usage for checking port conflicts, recording service ports, releasing occupied ports, and listing recorded service ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damienCronw](https://clawhub.ai/user/damienCronw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local port usage, maintain service-to-port records, resolve conflicts before starting software, and allocate available ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Freeing a port terminates the process currently using that port. <br>
Mitigation: Use query or list before free/check, and confirm termination only for processes you recognize. <br>
Risk: Bundled port records may reflect another environment rather than the user's machine. <br>
Mitigation: Clear or review the bundled ports.json records so the skill starts with local service-port assignments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damienCronw/port-manager) <br>
- [Publisher profile](https://clawhub.ai/user/damienCronw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local JSON port records and terminate processes only when the user confirms a free or conflict-resolution action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
