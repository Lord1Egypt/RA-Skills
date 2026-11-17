## Description:

Weekly/periodic engineering retrospective skill that generates delivery reviews based on git history and code quality metrics, with 24h, 7d, 14d, and 30d windows plus contributor analysis and growth recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate periodic delivery retrospectives from repository git history, code-change metrics, contributor activity, and backlog notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads git history, contributor identity metadata, changed-file paths, and TODOs from the target repository.

Mitigation: Use it only in repositories where those details may be analyzed by the agent and review the retrospective before sharing it outside the intended team.

Risk: The skill runs a normal git fetch against the configured origin before producing the retrospective.

Mitigation: Run it only in repositories with an expected origin remote and network behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis, Guidance]

**Output Format:** [Markdown retrospective report with tables, histograms, contributor summaries, backlog review, and next-focus recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports /retro, /retro 24h, /retro 14d, and /retro 30d time windows; default window is 7 days.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
