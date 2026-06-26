## Description: <br>
Docker container lifecycle management for listing containers, starting or stopping containers, viewing logs, checking stats, and pruning unused containers or images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Docker containers, images, logs, runtime stats, and disk usage from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Force-prune commands can delete stopped containers, dangling images, or unused images from the active Docker context. <br>
Mitigation: Require the agent to show the active Docker context, relevant `docker ps -a` or `docker system df` output, target resources, and the exact prune command before execution. <br>
Risk: Broad lifecycle commands can start, stop, restart, or inspect the wrong container when names or IDs are ambiguous. <br>
Mitigation: Require explicit container names or IDs and preview the exact Docker command before any state-changing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-docker-manager) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Docker CLI and an active Docker daemon; commands operate on the current Docker context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
