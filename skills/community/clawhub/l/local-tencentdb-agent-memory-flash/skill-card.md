## Description: <br>
Provides a local deployment guide for the TencentDB-Agent-Memory OpenClaw plugin, including SQLite-based memory storage and recall, cleanup, context protection, and installation verification steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, verify, and troubleshoot a local conversation-memory plugin that can persist and recall user preferences and dialogue context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured memory plugin can persist conversation content, including sensitive or regulated data if users place it in memory. <br>
Mitigation: Avoid storing secrets or regulated data in memory and review retention, cleanup, and recall settings before deployment. <br>
Risk: Remote embedding configuration may send memory content to an external provider if enabled. <br>
Mitigation: Keep the default local embedding mode unless the remote provider and endpoint are trusted and approved. <br>
Risk: The optional patch script can modify the local OpenClaw runtime behavior. <br>
Mitigation: Inspect or skip the patch script when runtime changes are not desired; the artifact states base conversation recording can still work without it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudcode-hans/local-tencentdb-agent-memory-flash) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install checks, restart commands, local memory configuration, verification prompts, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
