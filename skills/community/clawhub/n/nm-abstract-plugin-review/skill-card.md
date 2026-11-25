## Description:

Review plugin quality with tiered checks and dependency scoping. Use for PR and pre-release audits

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and plugin maintainers use this skill to review changed plugins before merge or audit all plugins before a release. It scopes checks by dependencies and reports per-plugin results and an aggregate verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A possible conflict with another command named “review” could make it unclear which action will run.

Mitigation: Check command resolution in the target setup and make the intended review command explicit before use.

Risk: The security scan was partial because three referenced paths could not be matched to bundled components.

Mitigation: Treat the scan as incomplete evidence and review those references before relying on the skill.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with per-plugin tables, verdicts, and scorecards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report depth and scope vary by branch, PR, or release tier.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
