## Description: <br>
交互式部署多 Agent 团队协作架构，支持自定义团队结构、预设模板和混合模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaybeMarvel](https://clawhub.ai/user/MaybeMarvel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure multi-agent team structures with preset, custom, or mixed team layouts, then generate configuration they can review and merge into an OpenClaw deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment helper copies the main agent's authentication and model profile files into persistent team and member agent directories. <br>
Mitigation: Run it only in a trusted OpenClaw environment, review the generated directories and copied profiles, and remove unused generated agents or copied profiles when finished. <br>
Risk: Custom team and member names influence generated paths and agent identifiers. <br>
Mitigation: Prefer interactive mode, use simple lowercase IDs without slashes or dot paths, and inspect generated paths and team names before merging configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaybeMarvel/multi-agent-teams) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, markdown, guidance] <br>
**Output Format:** [Interactive shell prompts plus generated OpenClaw JSON configuration and agent template guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and an existing OpenClaw environment; generated configuration should be reviewed before merging.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
