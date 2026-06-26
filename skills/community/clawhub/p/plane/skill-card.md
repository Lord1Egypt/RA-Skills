## Description: <br>
Manage Plane.so projects and work items using the `plane` CLI. List projects, create/update/search issues, manage cycles and modules, add comments, and assign members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vaguilera-jinko](https://clawhub.ai/user/vaguilera-jinko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project teams use this skill to manage Plane.so workspace projects, work items, cycles, modules, comments, states, labels, and members from an agent-assisted CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI is installed from a GitHub-hosted script. <br>
Mitigation: Inspect the script before installing or prefer a pinned release and checksum when available. <br>
Risk: Plane API credentials can authorize workspace changes through update, assignment, comment, and delete commands. <br>
Mitigation: Use the least-privileged Plane token available and confirm project and issue IDs before running mutating commands. <br>


## Reference(s): <br>
- [Plane.so](https://plane.so) <br>
- [Plane skill homepage](https://github.com/JinkoLLC/plane-skill) <br>
- [Plane CLI download script](https://raw.githubusercontent.com/JinkoLLC/plane-skill/main/scripts/plane) <br>
- [ClawHub Plane.so release](https://clawhub.ai/vaguilera-jinko/plane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI defaults to formatted tables and can return raw JSON with `-f json`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
