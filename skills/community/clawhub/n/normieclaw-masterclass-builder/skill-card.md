## Description:

Create personalized multi-day masterclasses on any topic, including custom curricula, daily lessons with exercises, progress tracking, and difficulty adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create, resume, and manage personalized multi-day courses on user-selected topics. The agent builds syllabi, generates lessons and exercises, tracks progress in workspace files, and adjusts difficulty based on learner feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and update course files and progress records in the user's workspace.

Mitigation: Install only when workspace-local course storage is expected, and review generated course files as part of normal workspace changes.

Risk: Scheduled lesson delivery may involve a suggested cron command.

Mitigation: Review the suggested cron schedule and prompt before adding automated lesson delivery.

Risk: Generated lessons on broad or specialized topics may be incomplete or unsuitable for high-stakes decisions.

Mitigation: Use the lessons as learning guidance and verify important topic-specific advice with authoritative sources or qualified experts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-masterclass-builder)
- [Publisher Profile](https://clawhub.ai/user/nollio)
- [Curriculum Templates](artifact/references/curriculum-templates.md)
- [Lesson Format Template](artifact/references/lesson-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown lessons, syllabus files, JSON progress records, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace-local files under masterclasses/ for course syllabi, lessons, and progress tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
