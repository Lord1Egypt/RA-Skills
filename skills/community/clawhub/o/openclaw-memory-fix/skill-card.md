## Description: <br>
Optimizes OpenClaw memory workflows with a four-layer memory architecture, dynamic decay, migration commands, and retrieval guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[githubxiaohei](https://clawhub.ai/user/githubxiaohei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure and operate a workspace memory system with layered storage, decay previews, and manual migration commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broad workspace memory and agent-governance configuration, not only a small memory utility. <br>
Mitigation: Review the bundled config files before deployment and keep only the memory, governance, and automation behavior intended for the target workspace. <br>
Risk: Automatic memory writes, heartbeat checks, delegation, and external-search guidance can expand an agent's operating scope. <br>
Mitigation: Narrow or disable these behaviors unless they are explicitly needed, and require review for sensitive operations such as deletion, external messaging, or changes to user data. <br>
Risk: Bundled profile and memory files may contain personal or platform-specific identifiers. <br>
Mitigation: Remove or replace personal workspace details before installation and avoid storing secrets or sensitive user data in memory files. <br>


## Reference(s): <br>
- [OpenClaw Memory Reference](references/MEMORY.md) <br>
- [OpenClaw Project Homepage](https://github.com/openclaw/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/githubxiaohei/openclaw-memory-fix) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown documentation with JavaScript, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for the bundled memory status, migration, and decay preview commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
