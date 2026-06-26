## Description: <br>
Enables the bot to manage Docker containers, images, and stacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, diagnose, and manage Docker containers, images, and stacks from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker management commands can remove containers, images, volumes, or networks and may cause irreversible data loss. <br>
Mitigation: Require explicit user confirmation before destructive Docker operations, bulk stop or kill actions, and commands using force flags. <br>
Risk: Docker logs, inspect output, and environment variables can contain credentials or other sensitive data. <br>
Mitigation: Keep Docker output local, avoid sending it to external endpoints, and redact secret values before including results in responses. <br>
Risk: Pulling, building, pushing, or executing containers can introduce untrusted code or publish sensitive image contents. <br>
Mitigation: Confirm unverified image pulls and image pushes, verify target registries and tags, review Dockerfiles before builds, and confirm sensitive docker exec requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/moltbot-docker-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/moltbot-docker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize lengthy Docker output and redact secret values before responding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
