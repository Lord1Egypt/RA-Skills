## Description: <br>
Review plugin quality with tiered checks and dependency scoping for PR and pre-release audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit plugin quality before branch, pull request, and release milestones by scoping affected and related plugins and reporting quality gates, scorecards, remediation actions, and verdicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad review-related wording may cause accidental invocation in review or documentation tasks. <br>
Mitigation: Invoke the skill with explicit, namespaced prompts and only install it when plugin review participation is intended. <br>
Risk: Repository inspection during review may expose private or sensitive project context. <br>
Mitigation: Confirm the repository scope before use and avoid private or sensitive projects unless that review scope is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-plugin-review) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, verdict summaries, inline shell commands, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include branch, PR, or release tier findings, affected and related plugin lists, quality-gate exit code guidance, scorecards, and remediation actions.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
