## Description: <br>
Hope OpenTask helps agents query and manage OpenTask jobs for OpenClaw containers, including task listing, creation, state transitions, statistics, and logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect queued OpenTask work, create tasks, and update task state for OpenClaw containers through a local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reusable API key is documented in the skill materials and may grant task-management access if reused unchanged. <br>
Mitigation: Rotate the exposed key if it is real, move credentials to an environment-provided secret, and avoid committing live credentials. <br>
Risk: Create, start, complete, fail, retry, and cancel operations can change real task state. <br>
Mitigation: Use the skill only with controlled OpenTask services and require explicit user confirmation before write operations. <br>


## Reference(s): <br>
- [OpenTask API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linux2010/hope-opentask) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local OpenTask API endpoints and task state values.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
