## Description: <br>
Oh My Teacher helps students prepare for university final exams by profiling courses, organizing materials, generating adaptive practice, grading answers, scheduling review, and explaining concepts with diagrams or code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charkschen](https://clawhub.ai/user/charkschen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students use this skill to turn course materials into exam-focused study plans, quizzes, mock exams, strict grading feedback, weak-point repair loops, flashcards, and spaced-repetition review. It is also useful for agent-hosted study workflows that need course snapshots, material routing, and environment-aware fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read course materials, notes, knowledge bases, or workspace files during study workflows. <br>
Mitigation: Confirm the files, folders, or knowledge bases the agent may access before using it with private course or personal data. <br>
Risk: The skill may save local study progress, including course snapshots, spaced-repetition state, notes, dashboards, or memory-backed summaries. <br>
Mitigation: Use explicit opt-in for persistence features and review where .oh-my-teacher files, notes, or memory writes are stored. <br>
Risk: Implicit invocation could activate the study assistant when the user only wants a normal chat or shell task. <br>
Mitigation: Disable or avoid implicit invocation when the skill should run only after an explicit user request. <br>
Risk: Exam-preparation workflows could be misused as proxy help for an exam or graded assessment in progress. <br>
Mitigation: Follow the skill's academic-integrity policy: decline real-time exam answering or unaided assessment completion and offer to teach the underlying method instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charkschen/oh-my-teacher) <br>
- [Skill entry point](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Command routing index](artifact/references/INDEX.md) <br>
- [Environment adaptation](artifact/references/environment-adaptation.md) <br>
- [Materials ingestion](artifact/references/materials-ingestion.md) <br>
- [Question and grading workflows](artifact/references/question-types.md) <br>
- [Spaced repetition](artifact/references/spaced-repetition.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with study plans, quizzes, grading feedback, code blocks, ASCII diagrams, flashcard tables, and optional CSV/TSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local course snapshots, spaced-repetition state, notes, dashboards, and flashcard export files when the host environment supports persistence and the user requests those workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
