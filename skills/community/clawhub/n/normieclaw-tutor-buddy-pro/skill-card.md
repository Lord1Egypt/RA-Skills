## Description:

Tutor Buddy Pro provides step-by-step Socratic homework help, adaptive quizzes, study plans, progress tracking, and learning-style-aware tutoring across core school subjects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Students, parents, and learners use the skill for guided homework support, practice quizzes, exam study planning, and progress review without simply receiving final answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learner profiles, quiz history, session logs, and study plans can contain sensitive student data, including data about minors.

Mitigation: Review the skill before child or student use, keep learner data local where possible, and store only the minimum information needed for tutoring.

Risk: Dashboard sync can expose learner data if the destination, fields, or storage controls are not verified.

Mitigation: Avoid dashboard sync until the data sent and storage location are confirmed.

Risk: Custom progress-report output paths and unescaped learner data can create file-handling or HTML rendering risk.

Mitigation: Use the default reports location and do not pass custom output paths until report output is constrained to a safe directory and learner data is escaped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-tutor-buddy-pro)
- [README](artifact/README.md)
- [Security audit and guarantees](artifact/SECURITY.md)
- [Setup instructions](artifact/SETUP-PROMPT.md)
- [Tutor configuration](artifact/config/tutor-config.json)
- [Dashboard companion spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Tutoring session example](artifact/examples/tutoring-session.md)
- [Quiz mode example](artifact/examples/quiz-mode.md)
- [Study plan example](artifact/examples/study-plan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tutoring responses, JSON learner records and study plans, setup commands, configuration files, and optional HTML or PNG progress reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learner profile, quiz history, session log, study plan, configuration, and progress report files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
