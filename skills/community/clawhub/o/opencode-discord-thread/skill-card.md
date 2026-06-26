## Description: <br>
Use this skill when OpenClaw should hand a coding task to OpenCode, keep the OpenCode run model-compatible with Z.AI Coding Plan / GLM plans, and mirror execution progress into a Discord thread for live review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r0s-org](https://clawhub.ai/user/r0s-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding work to a local OpenCode run while mirroring progress, status updates, and final summaries into a Discord thread for live review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coding prompts, execution details, errors, and repository-derived content may be posted to a Discord thread. <br>
Mitigation: Use a private Discord destination, start with non-sensitive repositories, and avoid prompts or code that contain secrets or confidential information. <br>
Risk: The bridge depends on local OpenCode authentication and Discord bot access being correctly scoped. <br>
Mitigation: Confirm OpenCode authentication, bot permissions, and the target thread or channel before running the bridge. <br>


## Reference(s): <br>
- [OpenCode Discord Bridge Reference](references/opencode_discord_bridge.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/r0s-org/opencode-discord-thread) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline bash examples and Discord status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors OpenCode event summaries and transcript chunks to Discord while OpenCode performs local repository changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
