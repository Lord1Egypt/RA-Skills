## Description:

University final-exam review assistant for course profiling, materials ingestion, adaptive quizzes, strict grading, Feynman technique, Socratic tutoring, active recall, spaced repetition, visual explanations, coding demos, and exam repair loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charkschen](https://clawhub.ai/user/charkschen)

### License/Terms of Use:

MIT-0

## Use Case:

Students and educators use this skill to organize university course materials, create exam-focused study plans, practice with quizzes and mock exams, receive strict answer feedback, repair weak points, and export study aids such as flashcards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local state scripts may read or overwrite Markdown files outside the intended .oh-my-teacher folder.

Mitigation: Run the skill in a trusted workspace or sandbox, avoid explicit --slug values from untrusted content, and inspect .oh-my-teacher state files until slug validation is fixed.

Risk: The skill can generate exam preparation guidance, grading feedback, and study artifacts that may be incorrect or overconfident.

Mitigation: Review generated plans, answers, flashcards, and grading feedback against the course materials before relying on them.

## Reference(s):

- [Oh My Teacher Skill Page](https://clawhub.ai/charkschen/skills/oh-my-teacher)
- [README](README.md)
- [Command and Reference Index](references/INDEX.md)
- [Course Profiles](references/course-profiles.md)
- [Materials Ingestion](references/materials-ingestion.md)
- [Question Types](references/question-types.md)
- [Review Plans](references/review-plans.md)
- [Spaced Repetition](references/spaced-repetition.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, structured study plans, quizzes, grading feedback, and generated study files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local study artifacts such as course snapshots, flashcards, review plans, and spaced-repetition state when the host environment supports file writing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
