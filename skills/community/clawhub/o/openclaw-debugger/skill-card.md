## Description:

Debugging assistant. Analyzes error logs, suggests breakpoints, traces execution flow, and helps identify root causes of issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Python tracebacks, identify likely root causes, choose useful breakpoints, and trace function calls while debugging local code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read log or source files explicitly provided by the user, and those files may contain sensitive information.

Mitigation: Review inputs before use and avoid passing sensitive files unless their contents are necessary for the debugging task.

Risk: Debugger suggestions may be incomplete or incorrect for unfamiliar code paths or error patterns.

Mitigation: Treat analysis, breakpoint suggestions, and traces as reviewable guidance before changing code or runtime settings.

## Reference(s):

- [OpenClaw Debugger on ClawHub](https://clawhub.ai/michealxie001/skills/openclaw-debugger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal guidance with code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads only user-provided error text or explicitly specified local files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
