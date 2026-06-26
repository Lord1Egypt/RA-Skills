## Description: <br>
Interact with Kanboard project management through its JSON-RPC API for projects, boards, tasks, comments, subtasks, users, and related workflow objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyang-bsy](https://clawhub.ai/user/liyang-bsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage Kanboard projects and tasks, including creating projects, moving tasks, adding comments, managing users, and updating permissions through JSON-RPC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Kanboard Application API token can let the agent make powerful changes to a live Kanboard instance. <br>
Mitigation: Install only for trusted Kanboard servers, use a dedicated token where possible, and keep the token secret. <br>
Risk: Project, task, user, and permission-management calls can delete, disable, or otherwise change live Kanboard data. <br>
Mitigation: Verify exact project, task, user, and permission IDs before changes, and require explicit confirmation before destructive or administrative actions. <br>


## Reference(s): <br>
- [ClawHub Kanboard Skill Page](https://clawhub.ai/liyang-bsy/kanboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-RPC parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KANBOARD_URL, KANBOARD_API_TOKEN, curl, and jq; Kanboard API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
