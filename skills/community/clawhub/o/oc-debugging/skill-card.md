## Description: <br>
Debugging assistant. Analyzes error logs, suggests breakpoints, traces execution flow, and helps identify root causes of issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Python and C/C++ error logs or source files, choose breakpoint locations, trace function flow, and identify likely root causes during debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads logs or source files selected by the user, which may contain secrets or sensitive implementation details. <br>
Mitigation: Redact secrets and sensitive data from logs and source snippets before using the skill. <br>
Risk: C/C++ tracing support depends on a local c-support library when present. <br>
Mitigation: Verify the local c-support dependency before relying on the C/C++ tracing path. <br>
Risk: Debugging recommendations can be incomplete or misleading for complex failures. <br>
Mitigation: Review suggested fixes, breakpoints, and shell commands before applying them to a codebase. <br>


## Reference(s): <br>
- [OpenClaw Debugging Assistant on ClawHub](https://clawhub.ai/michealxie001/oc-debugging) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style terminal output with suggested commands and structured debugging guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-selected logs or source files and may suggest GDB, Valgrind, breakpoint, and configuration steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
