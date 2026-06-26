## Description: <br>
No waiting! Create professional-grade OpenClaw configurations in 30 seconds through natural conversation. Instantly generate enthusiast-level base configs that intelligently combine emotional and professional needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to generate personalized agent configuration packages from conversation inputs, celebrity templates, and profession templates. It produces draft identity, memory, tool, user, soul, and agent workflow files for review before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send profile details such as names, profession, use case, communication style, and avatar prompts to a remote service. <br>
Mitigation: Provide only information suitable for the remote service and avoid sensitive personal, customer, or confidential data. <br>
Risk: Generated MEMORY.md, TOOLS.md, and AGENTS.md can change agent behavior and tool access. <br>
Mitigation: Review generated files before applying them, remove unnecessary high-privilege tools, and back up existing OpenClaw configuration files. <br>
Risk: The avatar workflow may return a local file path even when no file was actually saved. <br>
Mitigation: Verify that the returned avatar file exists before relying on it in a configuration package. <br>


## Reference(s): <br>
- [OpenClaw Soul Weaver on ClawHub](https://clawhub.ai/addogiavara-tech/openclaw-soul-weaver) <br>
- [Template Reference](references/templates.md) <br>
- [Tool Configuration Reference](references/tools.md) <br>
- [Generation API Endpoint](https://sora2.wboke.com/api/v1/generate) <br>
- [Online Creation Page](https://sora2.wboke.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown configuration files with a base64 ZIP package and optional avatar path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, and AGENTS.md for review before applying.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
