## Description: <br>
Code handles only the happy path — external calls, I/O, and parsing have no failure handling and crash on anything unexpected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a review checklist for identifying missing error handling around external calls, I/O, parsing, subprocesses, and user-facing versus internal errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the checklist as an automatic code audit. <br>
Mitigation: Apply it during development and review, and manually inspect relevant external call sites because the skill does not inspect or modify code. <br>
Risk: Error-handling guidance can be applied too broadly and hide unexpected defects. <br>
Mitigation: Catch specific recoverable exceptions, log context for swallowed errors, and allow unknown failures to propagate with useful context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvogt99/missing-error-handling) <br>
- [Publisher profile](https://clawhub.ai/user/mvogt99) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown checklist and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no code execution, file changes, or automatic inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
