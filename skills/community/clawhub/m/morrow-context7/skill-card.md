## Description: <br>
Look up current, accurate documentation and code examples for any library or framework using context7-mcp when an agent needs API details, configuration examples, method signatures, or integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timesandplaces](https://clawhub.ai/user/timesandplaces) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to retrieve current library documentation and examples before answering implementation, API, configuration, or integration questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation queries may disclose private library names, proprietary APIs, or sensitive implementation details to an external documentation service. <br>
Mitigation: Review prompts before using the skill with private codebases or sensitive implementation details, and avoid sending confidential identifiers unless approved. <br>
Risk: The skill runs an MCP server through npx and requires network access. <br>
Mitigation: Use it in environments where npx execution and outbound network access are allowed, and review the resolved package and command before deployment. <br>


## Reference(s): <br>
- [Context7](https://context7.com) <br>
- [ClawHub skill page](https://clawhub.ai/timesandplaces/morrow-context7) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tool-call examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and network access; no API key is required. Documentation queries may leave the user's environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
