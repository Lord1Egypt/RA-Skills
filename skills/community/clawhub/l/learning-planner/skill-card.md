## Description:

Personal learning management system with goal setting, spaced repetition scheduling, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and agents assisting learners use this skill to define goals, create daily or weekly study plans, manage spaced repetition cards, organize resources, and review learning progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores learning goals, notes, cards, sessions, and progress in a local database under the user's home config directory.

Mitigation: Install in a virtual environment when possible and avoid sharing or backing up the local database without reviewing its contents.

Risk: Delete-oriented commands or data-layer functions can remove local learning records without visible confirmation prompts in the inspected evidence.

Mitigation: Review delete commands before execution and keep a backup of important learning data.

## Reference(s):

- [Learning Planner on ClawHub](https://clawhub.ai/harrylabsj/skills/learning-planner)
- [Python Documentation](https://docs.python.org)
- [MDN Web Docs](https://developer.mozilla.org)
- [AWS Whitepapers](https://aws.amazon.com/whitepapers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and structured text with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local learning goals, cards, resources, sessions, and progress stored on disk.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
