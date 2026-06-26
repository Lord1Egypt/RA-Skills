## Description: <br>
Manage Plane.so projects and work items using the `plane` CLI. List projects, create/update/search issues, manage cycles and modules, add comments, and assign members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honluk](https://clawhub.ai/user/honluk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and project teams use this skill to manage Plane.so workspace data from an agent through the `plane` CLI, including projects, work items, cycles, modules, comments, and assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses PLANE_API_KEY to access a live Plane workspace. <br>
Mitigation: Store PLANE_API_KEY as a secret and verify PLANE_WORKSPACE and PLANE_BASE_URL before use. <br>
Risk: Create, update, assign, comment, and delete commands can change live workspace data. <br>
Mitigation: Require explicit confirmation before running commands that modify or delete Plane resources. <br>
Risk: Installation depends on a downloaded GitHub release executable. <br>
Mitigation: Install only when the GitHub release source is trusted and the intended `plane` binary is being used. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/honluk/my-plane) <br>
- [Publisher Profile](https://clawhub.ai/user/honluk) <br>
- [Plane](https://plane.so) <br>
- [My Plane GitHub Project](https://github.com/HonLuk/my-plane) <br>
- [Plane CLI Release Download](https://github.com/HonLuk/my-plane/releases/latest/download/plane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `plane` binary plus PLANE_API_KEY and PLANE_WORKSPACE environment variables; Plane CLI commands can return formatted tables or JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
