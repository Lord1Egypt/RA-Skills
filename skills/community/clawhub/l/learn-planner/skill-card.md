## Description:

Generate 7-day learning plans, quizzes, and local study progress tracking for common technical topics without requiring an internet connection or account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and developer-support agents use this skill to generate beginner-to-intermediate study plans, quiz questions, and lightweight local progress summaries for technical subjects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Progress reset or topic changes overwrite local study progress history in ~/.local/share/education-skill/progress.json.

Mitigation: Back up the progress file before using reset or set-topic when the existing study history must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/learn-planner)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal text with command examples, learning-plan sections, quiz questions, and progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic, built-in educational content and writes study progress to a local JSON file when progress commands are used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
