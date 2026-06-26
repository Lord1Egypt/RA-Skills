## Description: <br>
Plane.so: Create, update, and manage issues, projects, states, labels, and pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzakirov](https://clawhub.ai/user/jzakirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project teams use this skill to operate Plane.so project management workflows from an agent, including creating, listing, updating, and deleting issues, projects, states, labels, and pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can modify or delete Plane.so project data when it has a valid API key. <br>
Mitigation: Use the least-privileged Plane API key available, confirm the target workspace and project, and require explicit user approval before delete operations. <br>
Risk: Installing an unverified CLI package could introduce supply-chain risk. <br>
Mitigation: Verify the plane-cli package source before installation and pin the installed version. <br>


## Reference(s): <br>
- [Plane.so](https://plane.so) <br>
- [Plane CLI on ClawHub](https://clawhub.ai/jzakirov/plane-cli-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON output for scripting; destructive delete commands require explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
