## Description: <br>
OpenClaw configuration management best practices and common pitfalls for modifying configuration, checking paths and structure, resolving configuration errors, adding providers or channels, and avoiding unsafe direct JSON edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackTian010105](https://clawhub.ai/user/JackTian010105) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to safely inspect, patch, and verify OpenClaw configuration for providers, channels, gateway settings, and agent defaults. It helps avoid common configuration mistakes such as guessing paths, directly editing JSON files, or replacing the full configuration unintentionally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration output may contain API keys, bot tokens, or gateway tokens. <br>
Mitigation: Mask secrets before sharing `gateway config.get` output. <br>
Risk: A broad configuration replacement can unintentionally remove existing settings. <br>
Mitigation: Review any `config.patch` before applying it and avoid full config replacement unless intended. <br>


## Reference(s): <br>
- [OpenClaw 配置路径速查表](references/common-paths.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no code execution behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
