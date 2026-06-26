## Description: <br>
Reviews Go code for idiomatic patterns, error handling, concurrency safety, interface design, resource lifecycle, naming, and version-gated language guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Go changes for error handling, concurrency, interface design, resource lifecycle, naming, and version-gated language guidance before reporting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings may be inaccurate if version-gated Go guidance is applied without checking the target repository baseline. <br>
Mitigation: Read go.mod first and apply advice only when it matches the recorded go directive. <br>
Risk: Findings may be misleading if based only on a diff hunk instead of the surrounding Go code. <br>
Mitigation: Read the full enclosing function or logical unit for each changed file before reporting issues. <br>
Risk: A separately referenced review-verification-protocol skill can influence the review process when present. <br>
Mitigation: Verify that referenced protocol in the local environment before relying on findings governed by it. <br>


## Reference(s): <br>
- [Go Code Review on ClawHub](https://clawhub.ai/anderskev/go-code-review) <br>
- [Common Mistakes](references/common-mistakes.md) <br>
- [Concurrency](references/concurrency.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Interfaces](references/interfaces.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown review findings with file and line references, severity, and issue descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are gated by the repository go.mod baseline, surrounding code context, scoped checklist references, and pre-report verification.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
