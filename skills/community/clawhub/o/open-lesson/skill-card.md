## Description:

Interact with the openLesson tutoring API to generate learning plans, start audio-based sessions, analyze reasoning gaps, and manage tutoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dncolomer](https://clawhub.ai/user/dncolomer)

### License/Terms of Use:


## Use Case:

Learners, tutors, and agents use this skill to create openLesson learning plans, run audio-based Socratic tutoring sessions, and retrieve session summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends learning topics, session data, and audio recordings to openLesson.

Mitigation: Install and use it only when the user has approved sharing those data types with openLesson.

Risk: The documented shell command pattern can be unsafe if user-provided values are interpolated into bash commands.

Mitigation: Avoid the bash -c variable pattern with untrusted values; prefer structured API clients or carefully quoted command arguments.

Risk: Audio recording, upload, reminders, or calendar-like actions may affect user privacy or expectations.

Mitigation: Record or upload audio and perform reminder behavior only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dncolomer/skills/open-lesson)
- [openLesson Academy](https://www.openlesson.academy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENLESSON_API_KEY and uses audio recordings for session analysis.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
