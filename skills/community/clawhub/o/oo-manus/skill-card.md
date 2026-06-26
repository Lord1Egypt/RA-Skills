## Description: <br>
Manus (manus.im) lets an agent read, create, update, and delete Manus data through the OOMOL `oo` CLI connector instead of calling the Manus API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Manus tasks, projects, agents, connectors, skills, browser clients, and task messages through an OOMOL-connected account. It supports read workflows as well as user-confirmed write and destructive Manus actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run authenticated Manus actions through an OOMOL-connected account, including actions that change Manus state. <br>
Mitigation: Inspect the live connector schema, confirm the exact payload and effect with the user, and run write actions only after user approval. <br>
Risk: The `delete_task` action permanently deletes a stopped Manus task. <br>
Mitigation: Confirm the target task and obtain explicit approval before running destructive actions. <br>
Risk: The skill depends on connected account credentials and may fail when the CLI, login, connection, scope, or billing state is missing or expired. <br>
Mitigation: Use first-time setup steps only after a matching command failure and avoid proactively opening login or connection flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-manus) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Manus homepage](https://manus.im) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should inspect live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
