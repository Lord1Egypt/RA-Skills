## Description: <br>
Verify Mode guides an agent to inspect completed work, run tests or builds, validate assumptions, and produce an evidence-based verification report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after code changes or during bug investigation to check logic, edge cases, security concerns, tests, builds, and lint or formatting status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification may run the project's normal test, build, lint, or formatter commands, which can modify files, contact services, or rely on sensitive local configuration. <br>
Mitigation: Review project scripts and local configuration before execution, and run commands in an appropriate workspace with only the needed permissions. <br>
Risk: A verification report can miss issues or overstate confidence if checks are incomplete. <br>
Mitigation: Tie conclusions to concrete evidence such as code locations, command output, and pass or fail counts, and distinguish blocking issues from advisory findings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-openclaw-verify-mode) <br>
- [Skill homepage](https://github.com/zhaobod1/huo15-openclaw-enhance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown verification report with checklist, findings, severity, and conclusion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include results from project test, build, lint, or formatter commands.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata; artifact frontmatter lists 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
