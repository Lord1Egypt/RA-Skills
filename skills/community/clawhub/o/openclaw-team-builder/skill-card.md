## Description: <br>
Manage OpenClaw agent teams by adding agents, deploying templates, running health checks and fixes, viewing org trees, rolling back changes, and suggesting team structures from goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to manage multi-agent teams, configure channel bindings, inspect health, fix configuration issues, and generate suggested team structures from a business goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad persistent changes to OpenClaw agents, SOUL files, channel bindings, agent-to-agent permissions, and gateway state. <br>
Mitigation: Install only if the publisher is trusted, request an exact change summary before write actions, and review backups and rollback options before approving changes. <br>
Risk: Channel setup may involve bot tokens, app IDs, and app secrets. <br>
Mitigation: Do not paste secrets into ordinary chat or shell commands; use a secure local prompt, environment reference, or secret manager where possible. <br>
Risk: External channel bindings can expand where an agent can receive or send messages. <br>
Mitigation: Approve external channels one by one and verify each binding after creation. <br>


## Reference(s): <br>
- [ClawHub Openclaw Team Builder page](https://clawhub.ai/eggyrooch-blip/openclaw-team-builder) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw install documentation](https://docs.openclaw.ai/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local OpenClaw CLI actions that persist agent, SOUL, channel binding, gateway, and backup state.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
