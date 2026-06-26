## Description: <br>
Diagnose and repair Hermes Agent runs that silently stop and require manual "continue" messages even though no user input is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose Hermes continuation stalls and make bounded, regression-tested local repairs when Hermes stops after a non-final work-status response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner output may include snippets from prior Hermes conversations. <br>
Mitigation: Review scanner output before sharing it and redact sensitive conversation content. <br>
Risk: Repairs can change local Hermes control-loop behavior. <br>
Mitigation: Apply patches only after the scanner shows relevant continuation-stall evidence, then run the focused regression and compile checks before relying on the change. <br>
Risk: Already-running Hermes CLI sessions do not hot-load code edits. <br>
Mitigation: Exit and reopen stale interactive Hermes sessions after applying a repair. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hollis9087/hermes-continuation-maintainer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and concise repair reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output can be text or JSON; final reports summarize root cause, counts, files changed, tests run, and restart status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
