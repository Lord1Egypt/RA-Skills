## Description: <br>
Local-first, privacy-first OpenClaw inference plugin that routes routine queries to local Ollama models and uses cloud fallback for complex prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivaclaw](https://clawhub.ai/user/shivaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this plugin to reduce cloud inference costs and keep routine agent queries local while retaining optional cloud fallback for complex prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may be routed to third-party cloud providers automatically, and the security evidence says this can be less safe than the privacy claims imply. <br>
Mitigation: Review before installing in sensitive workspaces; use strict local-only mode by disabling cloudFallback for privacy-sensitive use. <br>
Risk: The plugin writes local audit, cache, metrics, and memory-related files. <br>
Mitigation: Keep enforceContextBoundary and audit logging enabled, and regularly review the local audit trail for unexpected cloud routing or privacy boundary violations. <br>
Risk: Sanitization and cloud routing behavior may not fully support the claim that private data never leaves the system. <br>
Mitigation: Avoid relying on that claim until routing and sanitization behavior is reviewed; test with representative sensitive prompts before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shivaclaw/project-nirvana-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/shivaclaw) <br>
- [Project repository](https://github.com/ShivaClaw/nirvana-plugin) <br>
- [Issue tracker](https://github.com/ShivaClaw/nirvana-plugin/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audit, metrics, cache, and memory files when installed and used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
