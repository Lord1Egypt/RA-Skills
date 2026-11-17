## Description:

Generate evidence-based project weekly reports from local repository history, tags, documentation, and uncommitted artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, and project contributors use this skill to turn local repository evidence into weekly project reports. It helps separate committed work, uncommitted artifacts, tags, and unverifiable external claims while producing detailed and brief report versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize incomplete or contradictory repository evidence.

Mitigation: Keep reports conservative and label claims as unverified when local evidence or user-provided context does not support them.

Risk: Broad status-summary requests may activate the skill and produce a Chinese report by default.

Mitigation: Ask for the desired language or report style when the default Chinese format is not wanted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangchao228/skills/project-weekly-report)
- [Project Weekly Report Source Homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/work/project-weekly-report)
- [Publisher GitHub Profile](https://github.com/yangchao228)
- [Publisher X Profile](https://x.com/yangchao228)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown weekly report with detailed and brief versions, written in Chinese by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The brief version is kept under 300 Chinese characters unless the user asks for a different format.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
