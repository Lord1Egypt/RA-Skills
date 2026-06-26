## Description: <br>
Configure and validate OpenClaw memory recall for persistent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SyaJask](https://clawhub.ai/user/SyaJask) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OpenClaw memory files, enable memory search, validate recall behavior, and troubleshoot poor memory matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may contain sensitive, regulated, or secret information. <br>
Mitigation: Avoid placing secrets or regulated data in MEMORY.md or memory/*.md, and prefer the local provider for sensitive workspaces. <br>
Risk: Remote memory providers may require API keys and send memory content outside the local workspace. <br>
Mitigation: Use protected environment variables or secret storage for remote-provider API keys, and choose remote providers only when appropriate for the workspace data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SyaJask/memory-setup-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/SyaJask) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output for configuring and validating OpenClaw memory recall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
