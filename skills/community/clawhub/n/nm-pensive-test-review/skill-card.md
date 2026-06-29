## Description: <br>
Evaluates test suites for coverage gaps, TDD/BDD compliance, and anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review test suites, identify coverage and scenario-quality gaps, and plan remediation before releases or after failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as quality or testing may activate the skill in conversations where a full test review was not intended. <br>
Mitigation: Use the skill when test-suite inspection is desired, and confirm activation before letting the agent inspect local tests or run test and coverage commands. <br>
Risk: The skill may propose shell commands for test or coverage tooling that operate on the local workspace. <br>
Mitigation: Review generated commands before execution and run them in the intended repository context. <br>
Risk: Installing the separate upstream Claude Code plugin is outside the reviewed ClawHub release. <br>
Mitigation: Review the upstream plugin independently before installing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-test-review) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Declared homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured review sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include framework detection, coverage gaps, quality issues, remediation plans, and approval recommendations.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
