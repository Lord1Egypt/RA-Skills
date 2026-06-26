## Description: <br>
Project Context Guide helps users understand codebase structure, trace code decisions, analyze dependencies and change impact, identify maintainers, and gather contextual information for code reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TeamoPlum](https://clawhub.ai/user/TeamoPlum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to onboard into unfamiliar repositories, trace design decisions, assess dependency and change impact, and identify likely maintainers for review or follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may expose sensitive repository and Git history details, including diffs, commit messages, contributor emails, maintainer names, collaboration relationships, and activity-time patterns. <br>
Mitigation: Install and run it only in repositories where the user is authorized to inspect source and Git history, and treat generated reports as sensitive project data. <br>
Risk: External team-system integrations such as Slack, JIRA, or Confluence can expand data access beyond the repository. <br>
Mitigation: Enable those integrations only with explicit team consent and documented data-handling rules. <br>
Risk: Contributor profiling and maintainer suggestions may be incomplete or misleading when history is sparse, stale, or lacks clear controls. <br>
Mitigation: Use ownership and activity recommendations as review aids, and confirm them with current team knowledge before acting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/TeamoPlum/project-context-guide) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Release notes](artifact/RELEASE_NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local repository analysis may include file paths, diffs, commit metadata, contributor names, and maintainer suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
