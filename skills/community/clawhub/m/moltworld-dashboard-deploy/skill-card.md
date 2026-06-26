## Description: <br>
Install, harden, and run the MoltWorld Dashboard reliably for real users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumetch](https://clawhub.ai/user/guillaumetch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare, deploy, verify, and troubleshoot a MoltWorld Dashboard service on port 8787 using local, Docker, Docker Compose, or explicitly approved systemd paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation or project dependencies may execute unwanted behavior if accepted without review. <br>
Mitigation: Review package.json and lockfiles before npm commands, and use npm ci --ignore-scripts unless install scripts are explicitly reviewed and approved. <br>
Risk: Docker, Docker Compose, or systemd deployment can create a persistent service on the host. <br>
Mitigation: Use non-privileged local runtime paths first, and require explicit operator approval before Docker persistence or any privileged systemd action. <br>
Risk: A deployed dashboard may be unreachable or fail after an interactive session ends. <br>
Mitigation: Verify the listener and HTTP response on localhost:8787, then use Docker Compose or approved systemd supervision for long-running operation. <br>


## Reference(s): <br>
- [MoltWorld Dashboard Deploy Commands](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/guillaumetch/moltworld-dashboard-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with bash snippets and deployment file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local runtime scaffolding, Docker or Docker Compose deployment files, optional systemd service guidance, and port 8787 verification steps.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
