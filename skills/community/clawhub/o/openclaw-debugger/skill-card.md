## Description: <br>
OpenClaw Debugger analyzes error logs, suggests breakpoints, traces execution flow, and helps identify root causes of issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Python traceback text or local source files, get root-cause analysis, identify useful breakpoint locations, and trace function calls during debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs and source files provided for debugging may contain secrets, customer data, or other sensitive information. <br>
Mitigation: Use only local files appropriate for analysis and redact sensitive values before sharing or storing outputs. <br>
Risk: Root-cause analysis, breakpoint suggestions, and execution traces may be incomplete or incorrect for complex runtime failures. <br>
Mitigation: Treat the output as debugging guidance and validate proposed fixes or breakpoints in the target environment before applying changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/michealxie001/openclaw-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown-style guidance with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected error text, log files, or source files and prints local debugging analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
