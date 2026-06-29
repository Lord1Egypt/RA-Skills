## Description: <br>
Helps developers and AI-agent users reduce LLM prompt and context token usage by configuring headroom compression through proxy, CLI wrapper, Python SDK, or MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and AI-agent users use this skill to compress prompts and large context before sending requests to LLM providers, wrap local coding agents, integrate compression through SDK or MCP workflows, and review token-savings reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional telemetry may send token, model, and cost metrics to mrkjai.com. <br>
Mitigation: Keep telemetry disabled unless the user explicitly accepts that reporting, avoid including prompts or identifiers in metadata, and disable reporting when it is not needed. <br>
Risk: Installer and wrapping flows may modify the Python environment or local LLM client configuration. <br>
Mitigation: Review or pin installer content before execution, prefer local scripts over remote one-liners, and run installation in an isolated environment when possible. <br>
Risk: Dashboard API key persistence can expose credentials on shared or sensitive machines. <br>
Mitigation: Avoid storing the dashboard API key in shell startup files on shared systems; use scoped environment variables or restricted-permission config files and reset the key if exposed. <br>


## Reference(s): <br>
- [Headroom API reference](references/headroom_api.md) <br>
- [OPC Headroom ingest API reference](references/api_reference.md) <br>
- [headroom upstream project](https://github.com/chopratejas/headroom) <br>
- [headroom-ai on PyPI](https://pypi.org/project/headroom-ai/) <br>
- [ClawHub skill page](https://clawhub.ai/guipi888/llm-token-compressor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, configuration steps, and optional JSON or HTML report outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local HTML dashboards and optional telemetry event JSON when the user enables reporting.] <br>

## Skill Version(s): <br>
1.6.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
