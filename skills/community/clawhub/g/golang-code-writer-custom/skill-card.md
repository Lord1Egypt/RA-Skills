## Description: <br>
A Go development guidance skill that covers logging conventions, API and MCP flow analysis, Mermaid flow diagrams, and reusable Go implementation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l2yf](https://clawhub.ai/user/l2yf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill while working on Go MCP clients, backend services, data processing, and scheduled jobs to add consistent logging and understand API execution flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logging examples may be copied in ways that record raw parameters, full response bodies, tokens, personal data, or oversized payloads. <br>
Mitigation: Before applying logging examples, redact sensitive fields, log only allowlisted values, and truncate large request or response content. <br>
Risk: MCP examples depend on service URLs from mcp-config.json, so an untrusted endpoint could receive project data. <br>
Mitigation: Verify that each configured MCP endpoint is trusted before running generated client code or API examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l2yf/golang-code-writer-custom) <br>
- [Golang logging guidance](SKILL-logging.md) <br>
- [Golang flow analysis guidance](SKILL-flow-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with Go code examples and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples should be reviewed before use in production code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
