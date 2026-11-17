## Description:

Provides a Chinese-default technical learning assistant for computer science, AI, machine learning, reinforcement learning, software engineering, interview preparation, code analysis, study planning, knowledge review, and deeper research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and technical learners use this skill to receive structured explanations, interactive tutoring, interview practice, code walkthroughs, study plans, flashcards, review prompts, and locally maintained learning records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store learner goals, experience level, weak points, mistakes, progress, tags, and review schedules in local Markdown files.

Mitigation: Review the workspace files before installation and use; decide whether profile persistence is acceptable and request a no-profile, delete, or export workflow when needed.

Risk: Broad activation triggers may route ordinary learning, code, review, or research requests into profile and study-history workflows.

Mitigation: Confirm the desired mode before longer sessions and review generated profile, index, and study artifacts before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchen913/skills/learning-assistant)
- [Knowledge analysis module](references/01-knowledge-analysis.md)
- [Interaction modes module](references/02-interaction-modes.md)
- [File templates module](references/03-file-templates.md)
- [Code adaptation module](references/04-code-adaptation.md)
- [Domain adaptation module](references/05-domain-adaptation.md)
- [Research strategy module](references/06-research-strategy.md)
- [Index and review module](references/07-index-and-review.md)
- [Session continuity module](references/08-session-continuity.md)
- [Profile operations module](references/09-profile-operations.md)
- [Workspace README](workspace/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Chinese-default Markdown with structured sections and optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learner profile, learning index, anchor, plan, summary, confusion, mistake, flashcard, interview, code note, and review Markdown files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
