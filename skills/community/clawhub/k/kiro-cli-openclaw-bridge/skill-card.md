## Description: <br>
Connects OpenClaw, or any OpenAI-compatible client, to the kiro-cli ACP backend through a local ACP-to-OpenAI bridge with streaming responses and tool-call support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoshixi](https://clawhub.ai/user/luoshixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and run a local bridge that lets OpenClaw or another OpenAI-compatible client send chat requests to kiro-cli through ACP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge depends on kiro-cli authentication and may expose project-local tool execution through the configured working directory. <br>
Mitigation: Run it only in trusted project directories, keep the service bound to localhost, and review tool activity before using it on sensitive repositories. <br>
Risk: The security scan marked the artifact suspicious because unrestricted local execution patterns and external reviewer flows can expose repository diffs or local context. <br>
Mitigation: Follow the scanner guidance: install only in a trusted maintainer workspace, review generated commands before execution, and prefer safer no-yolo review modes unless unrestricted access is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoshixi/kiro-cli-openclaw-bridge) <br>
- [Project homepage](https://github.com/LuoShiXi/kiro-cli-openclaw-bridge) <br>
- [GitHub releases](https://github.com/LuoShiXi/kiro-cli-openclaw-bridge/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash, JSON, and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes localhost bridge setup, OpenClaw provider configuration, API endpoint checks, and platform-specific build notes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
