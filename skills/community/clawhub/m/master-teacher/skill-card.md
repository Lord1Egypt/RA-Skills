## Description:

Master Teacher transforms an AI agent into a structured instructor for multi-lesson courses using mastery learning, Socratic questioning, lesson authoring, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky-wzj](https://clawhub.ai/user/jacky-wzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical learners, and external users use this skill to have an agent research a topic, build a structured curriculum, deliver lessons one topic at a time, verify mastery, and preserve progress across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read USER.md or MEMORY.md during student profiling, which can expose personal, project, or company context.

Mitigation: Review memory/profile files before use and avoid using the skill in workspaces that contain secrets or sensitive personal or company information.

Risk: The skill persists course data, progress state, student responses, reports, and weak points in local files.

Mitigation: Use a dedicated course directory, keep sensitive prompts and answers out of the course, and remove or sanitize generated files when they are no longer needed.

## Reference(s):

- [Master Teacher on ClawHub](https://clawhub.ai/jacky-wzj/skills/master-teacher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown lessons, reports, progress summaries, inline shell commands, JSON state files, and course directory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local course materials, progress state, reports, student responses, and weak points in the workspace.]

## Skill Version(s):

2.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
