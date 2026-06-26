## Description: <br>
OpenClaw Regex Engine helps agents test, explain, build, browse, and replace JavaScript-compatible regular expressions through a disclosed remote MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to test, explain, generate, browse, and apply regex patterns for code, validation, and text transformation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex patterns and sample text are sent to the disclosed remote MCP service for processing. <br>
Mitigation: Avoid sending secrets, tokens, customer records, or private production documents unless the provider and its privacy claims are trusted. <br>
Risk: Complex or poorly designed regex patterns can cause slow matching or timeouts. <br>
Mitigation: Review generated patterns, test with representative positive and negative inputs, and avoid catastrophic backtracking patterns. <br>
Risk: Regex-based checks can be misleading if treated as complete security validation. <br>
Mitigation: Use regex for format checks and pair it with application-side validation for security-sensitive workflows. <br>


## Reference(s): <br>
- [OpenClaw Regex Engine on ClawHub](https://clawhub.ai/yedanyagamiai-cmd/openclaw-regex-engine) <br>
- [OpenClaw MCP servers homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers) <br>
- [Regex Engine MCP endpoint](https://regex-engine-mcp.yagami8095.workers.dev/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and JSON-like tool results containing regex patterns, matches, explanations, test cases, and replacement previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated or transformed regular expressions, capture group details, named groups, flags, and before/after replacement previews.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
