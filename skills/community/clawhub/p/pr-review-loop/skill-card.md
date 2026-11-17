## Description:

Autonomous PR review loop with Greptile. Use when an agent creates a PR and needs to autonomously handle code review feedback by reading Greptile reviews, fixing issues, pushing fixes, re-triggering review, and auto-merging when the score is 4/5+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cemoso](https://clawhub.ai/user/cemoso)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to process Greptile pull request reviews, apply review feedback, track review rounds, and decide when to merge or escalate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation can drive merges and branch deletion even when the stated review score gate has not been met.

Mitigation: Use only in tightly scoped trusted repositories with branch protection, least-privileged GitHub tokens, and explicit human approval before any merge or branch deletion.

Risk: Force-merge behavior and Telegram escalation can create governance risk if they are not deliberately configured and audited.

Mitigation: Remove or disable force_merge behavior and Telegram escalation unless they are intentionally configured, reviewed, and audited.

## Reference(s):

- [Greptile Feedback Patterns](references/greptile-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write review-state.json in the workspace when the helper script is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
