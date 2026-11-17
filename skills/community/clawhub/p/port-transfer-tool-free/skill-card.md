## Description: <br>
A personal MCP tool configuration migration skill that helps export, import, validate, and back up agent tool settings with credential placeholders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual agent users use this skill to move MCP tool configurations between AI agent environments, create portable JSON bundles, replace credential placeholders, and validate a single destination environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change agent tool configurations, and imported MCP commands can change what an agent may run later. <br>
Mitigation: Review every bundle before import, back up current agent configuration, and validate changes in one destination environment before wider use. <br>
Risk: The fill step may use real secrets. <br>
Mitigation: Use least-privilege API keys, run secret replacement only in a trusted destination environment, and keep local .env files out of version control. <br>
Risk: The security summary reports insufficient scoping or guardrails around configuration changes. <br>
Mitigation: Manually inspect target paths, MCP commands, and dependencies before allowing the imported configuration to take effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/port-transfer-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration bundle examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes portable MCP configuration bundles, credential placeholder handling, validation steps, and structured JSON-style results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
