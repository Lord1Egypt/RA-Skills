## Description: <br>
OpenViking 上下文数据库 helps OpenClaw agents manage layered L0/L1/L2 context, semantic search, session memory, and token usage for OpenViking-backed workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyonepice](https://clawhub.ai/user/onlyonepice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and configure OpenViking for OpenClaw, index project resources, search context semantically, inspect layered summaries, and track token savings across agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can run unpinned external code. <br>
Mitigation: Inspect the install scripts before use and replace the optional curl-to-bash CLI install path with a pinned or manual install when deploying on trusted machines. <br>
Risk: Provider API keys may be stored locally. <br>
Mitigation: Use scoped provider API keys and protect local OpenViking configuration files under ~/.openviking. <br>
Risk: The skill can persist or index user-selected content. <br>
Mitigation: Avoid importing directories that contain secrets, private repositories, or regulated data unless the deployment has been reviewed for that data. <br>


## Reference(s): <br>
- [OpenViking GitHub](https://github.com/volcengine/OpenViking) <br>
- [OpenViking Website](https://www.openviking.ai) <br>
- [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers) <br>
- [NVIDIA NIM API](https://build.nvidia.com/) <br>
- [OpenClaw Skill Documentation](https://docs.openclaw.ai/tools/creating-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local scripts and OpenViking/OpenClaw commands; token statistics are shown as text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
