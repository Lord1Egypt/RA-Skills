## Description: <br>
High School English helps Chinese Grade 10-12 students prepare for English exams with spaced vocabulary review, grammar and reading practice, error tracking, daily reports, and achievement feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanxlab](https://clawhub.ai/user/fanxlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, especially Chinese high school students in grades 10-12, use this skill for English exam preparation, daily practice, spaced vocabulary review, grammar and reading exercises, and review of mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Feishu sync can expose study data or tokens if credentials are over-shared. <br>
Mitigation: Prefer CSV mode unless Feishu sync is needed; if Feishu is used, use a least-privilege token and avoid sharing it in chats or shared workspaces. <br>
Risk: Photos sent for OCR may contain unrelated personal information, and OCR results may be saved into learning records. <br>
Mitigation: Send only study-related photos and review stored learning records for sensitive content. <br>


## Reference(s): <br>
- [High School English on ClawHub](https://clawhub.ai/fanxlab/high-school-english) <br>
- [Ebbinghaus Memory Management Rules](references/ebbinghaus.md) <br>
- [High School Profile Template](references/high-school-profile-template.md) <br>
- [Question Design Template](references/question-design-template.md) <br>
- [Vocabulary Learning Flow](references/vocab-learning-flow.md) <br>
- [Vocabulary Template](references/vocab-template.md) <br>
- [Vocabulary Schema](references/vocab-schema.csv) <br>
- [Knowledge Schema](references/knowledge-schema.csv) <br>
- [Review Log Schema](references/review-log-schema.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, files, guidance] <br>
**Output Format:** [Markdown-style tutoring responses with optional local CSV records or Feishu learning records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a learner profile, vocabulary records, knowledge records, and review logs based on the selected storage mode.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
