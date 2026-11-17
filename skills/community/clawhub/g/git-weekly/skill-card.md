## Description:

Analyzes the last seven days of Git commits and diffs to generate a weekly retrospective covering technical challenges, performance work, and AI productivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raccoon-office](https://clawhub.ai/user/raccoon-office)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill to turn recent personal Git history into a weekly technical retrospective, with emphasis on complex frontend work, performance and stability changes, and AI-assisted productivity improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically read full recent code patches from the current repository when triggered by broad summary phrases.

Mitigation: Review this skill before installing it in private or sensitive repositories, invoke it explicitly as git-weekly, and consider requiring confirmation or using git log summaries before full patch analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raccoon-office/skills/git-weekly)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown retrospective with structured sections and supporting Git analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect recent Git commit patches for the configured Git author before summarizing.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
