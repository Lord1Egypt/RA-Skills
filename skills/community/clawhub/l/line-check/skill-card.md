## Description: <br>
Use when asked to audit a repository, assess project health, find the highest-value improvements a repo needs, check whether a project is ready for contributors or coding agents, or decide what to work on next in a codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to perform read-only repository health audits, score project readiness across seven stations, and produce a prioritized backlog of actionable improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill conditionally runs local Brigade diagnostics when Brigade wiring is present, which may inspect sensitive repository handoff or memory data. <br>
Mitigation: Review the local behavior of `brigade handoff doctor` and `brigade memory care scan` before using the skill on sensitive repositories. <br>


## Reference(s): <br>
- [Line Check on ClawHub](https://clawhub.ai/solomonneas/line-check) <br>
- [Publisher profile](https://clawhub.ai/user/solomonneas) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report with scorecard, findings, prioritized backlog, and not-checked section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit output; fix sketches may include commands, but repository changes are outside the audit step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
