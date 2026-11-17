## Description:

High School English helps Chinese Grade 10-12 students practice exam-focused English through vocabulary review, grammar drills, reading and cloze practice, error tracking, study reports, and achievement tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanxlab](https://clawhub.ai/user/fanxlab)

### License/Terms of Use:

MIT-0

## Use Case:

Students and tutoring agents use this skill to run structured high-school English study sessions for vocabulary, grammar, reading comprehension, cloze practice, and wrong-answer review. The skill also guides setup of a learning profile and study-data storage in local CSV files or Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student learning data and study history may be saved to workspace files or Feishu tables without clear retention boundaries.

Mitigation: Use local CSV storage by default, keep the workspace private, and periodically review or delete stored profile, vocabulary, knowledge, and review-log records.

Risk: Photo uploads can produce OCR-derived text that is saved into learning records.

Mitigation: Upload only study images the student is comfortable storing, and confirm extracted content before saving it to vocabulary or knowledge records.

Risk: Feishu App Tokens and Table IDs may be stored in a plain profile file when Feishu storage is selected.

Mitigation: Use limited-scope Feishu credentials, avoid sharing the workspace, and rotate or revoke tokens if the profile file may have been exposed.

## Reference(s):

- [Ebbinghaus Memory Management Rules](references/ebbinghaus.md)
- [High School Profile Template](references/high-school-profile-template.md)
- [Question Design Template](references/question-design-template.md)
- [Vocabulary Learning Flow](references/vocab-learning-flow.md)
- [Vocabulary Template](references/vocab-template.md)
- [Vocabulary CSV Schema](references/vocab-schema.csv)
- [Knowledge CSV Schema](references/knowledge-schema.csv)
- [Review Log CSV Schema](references/review-log-schema.csv)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational tutoring guidance, Markdown study reports, and CSV-compatible learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning-profile and study-data files when the user selects local CSV storage.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
