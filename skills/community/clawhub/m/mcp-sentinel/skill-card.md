## Description: <br>
Audits MCP and AI agent configuration files for risky commands, broad filesystem access, inline secrets, and prompt-injection risks, reporting findings by severity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fasjdas](https://clawhub.ai/user/fasjdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run MCP Sentinel against a project root, summarize risky MCP or AI-agent configuration findings by severity, and propose safer configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on a disclosed third-party MCP Sentinel CLI and its npm dependencies. <br>
Mitigation: Review the referenced CLI and dependency set before installation or execution in sensitive environments. <br>
Risk: Scanning project roots may inspect configuration files that contain secret-looking keys or values. <br>
Mitigation: Run scans only on intended project roots and report secret findings by key name without exposing full values. <br>


## Reference(s): <br>
- [MCP Sentinel GitHub repository](https://github.com/fasjdas/mcp-sentinel) <br>
- [ClawHub release page](https://clawhub.ai/fasjdas/mcp-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, severity summaries, and optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes findings by severity and avoids exposing full secret values.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
