## Description: <br>
Capture, normalize, and report metrics across any domain with reusable dimensions, programmable formulas, and scalable reporting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external teams, and developers use this skill to define metric contracts, govern formulas, produce decision-oriented reports, and design alert policies across business, product, operations, finance, personal, and other domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metric memory may contain sensitive or outdated business context when the user enables local retention under ~/metrics/. <br>
Mitigation: Enable memory only when retention is desired, avoid storing secrets or unrelated personal data, and periodically review or delete ~/metrics/. <br>
Risk: Ambiguous metric definitions, formula drift, or failed data quality checks can lead to misleading reports. <br>
Mitigation: Use metric contracts, formula version history, and data quality gates before publishing reports or recommendations. <br>
Risk: Alerts without owners or response rules can create noise and missed escalations. <br>
Mitigation: Attach severity, owner, first response action, cooldown, and escalation criteria to every threshold policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/metrics) <br>
- [Skill homepage](https://clawic.com/skills/metrics) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with templates, tables, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local metric memory under ~/metrics/ when memory is enabled by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
