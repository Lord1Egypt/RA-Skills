## Description: <br>
Manage Plane.so projects and work items using a zero-dependency Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiseduardoaugusto](https://clawhub.ai/user/luiseduardoaugusto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to let an agent inspect and manage Plane.so projects, issues, comments, states, labels, cycles, and modules from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Plane API key can read or modify workspace project and issue data according to its permissions. <br>
Mitigation: Use a Plane API key with only the permissions needed for the intended workspace and avoid installing it where the agent should not change Plane records. <br>
Risk: The skill sends Plane workspace and work-item data to the Plane.so API. <br>
Mitigation: Use it only with workspaces whose data may be processed by Plane.so, and verify the target workspace before running create, update, assign, comment, or delete commands. <br>


## Reference(s): <br>
- [Plane.so CLI source](https://github.com/luiseduardoaugusto/plane-so-cli) <br>
- [Plane.so](https://plane.so) <br>
- [ClawHub skill page](https://clawhub.ai/luiseduardoaugusto/plane-so-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default CLI output is human-readable text; the bundled CLI can return raw JSON with the -f json option.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
