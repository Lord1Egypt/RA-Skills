## Description: <br>
Review plugin quality with tiered checks and dependency scoping for PR and pre-release audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review plugin quality before branch, pull request, and release milestones. It scopes affected and related plugins, runs tier-specific checks, and reports pass, warning, or fail outcomes with scorecards for deeper tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send repository diffs and selected repo-relative evidence to external reviewer tools. <br>
Mitigation: Avoid using it on sensitive code unless the reviewer provider's data handling and authentication are acceptable; use narrower engine or tool options when needed. <br>
Risk: Automated code-review findings may be incomplete or misleading if treated as final decisions. <br>
Mitigation: Have maintainers review findings and quality-gate outcomes before merging or releasing plugin changes. <br>
Risk: Release-tier review may invoke broad parallel checks across the plugin ecosystem. <br>
Mitigation: Run broad release checks in an environment where repository access, external tool use, and execution time are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-plugin-review) <br>
- [Source homepage from metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, scorecards, verdicts, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tier-specific PASS, PASS-WITH-WARNINGS, FAIL, and quality-gate exit-code guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
