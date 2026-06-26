## Description: <br>
Audits Makefiles for build correctness, portability, and recipe duplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Makefiles before committing build, automation, CI/CD, or portability changes. It helps map Make-related files, analyze dependencies and duplicated recipes, identify portability issues, and summarize recommended follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends command execution while reviewing Makefiles. <br>
Mitigation: Inspect every suggested command before running it and limit use to deliberate Makefile auditing tasks. <br>
Risk: The skill can lead to applied Makefile target generation or repository changes. <br>
Mitigation: Use any --apply or generated-target workflow only in a clean git diff or sandbox after explicitly deciding that Makefile changes are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-makefile-review) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with review findings, file references, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested Makefile refactors or target-generation guidance that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
