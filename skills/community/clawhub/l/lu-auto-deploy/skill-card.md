## Description: <br>
Helps an agent generate Docker deployment guidance, compose files, and shell commands for common monitoring, media, security, and utility services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and homelab or NAS administrators use this skill to ask an agent for Docker service deployment commands, service templates, batch deployment guidance, and configuration file examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Docker commands can make high-impact changes to the host or running services. <br>
Mitigation: Review every command before execution and run only commands that match the intended host, paths, ports, images, and restart policy. <br>
Risk: Broad host mounts can expose sensitive files or media directories to containers. <br>
Mitigation: Use the narrowest practical volume mounts and avoid mounting broad host paths unless the access is required and understood. <br>
Risk: File Browser, Portainer, and similar admin surfaces can expose powerful controls when published without safeguards. <br>
Mitigation: Require strong authentication, restrict network exposure, and avoid public access unless a hardened deployment plan is in place. <br>
Risk: Mounting docker.sock gives a container host-level Docker control. <br>
Mitigation: Avoid docker.sock mounts unless explicitly required, and treat any container with that mount as highly privileged. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jesson1222-ship-it/lu-auto-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/jesson1222-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Docker Compose code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker run commands, docker-compose.yml examples, directory setup commands, service lists, and update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
