## Description: <br>
Merge Check Paid helps maintainers and teams analyze pull request merge readiness in batches, with multi-dimensional scoring, historical trends, CI/CD gate integration, custom rules, risk alerts, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and team leads use this skill to triage open pull requests, predict merge readiness, configure team-specific rejection rules, and generate dashboards or reports for code quality governance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines broad activation language with shell/write access, GitHub credentials, and CI gate behavior that may affect repositories or tokens outside the intended workflow. <br>
Mitigation: Review before installing, grant least-privilege GitHub credentials, avoid broad PATs, require confirmation before CI gates or blocking actions, and invoke it only for PR merge-analysis workflows. <br>
Risk: CI/CD gate and custom rule outputs may block or influence merges based on incomplete or incorrect analysis. <br>
Mitigation: Require maintainer review for blocking decisions, keep an audited manual bypass path, and tune thresholds against historical repository outcomes before enforcing gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/merge-check-paid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, shell command snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR scores, summaries, dashboard/report instructions, rule configuration examples, and CI/CD gate guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
