## Description:

学习知识管理系统，支持知识点录入、分类存储、每日早间学习建议推送、晚间知识回顾推送、专项备考管理、知识点查询与维护。

This skill is ready for commercial/non-commercial use.

## Publisher:

[elle-yu](https://clawhub.ai/user/elle-yu)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and exam-prep users use this skill to record knowledge points, organize them by category, manage focused study projects with deadlines, and receive daily review, quiz, and study recommendation messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic triggers may route unrelated user messages into this learning workflow.

Mitigation: Prefer explicit command-style triggers and review the activation scope before installing.

Risk: The OCR workflow can download image URLs and process them with shell commands.

Mitigation: Disable or constrain the OCR URL download path, restrict web fetching, and use unique private temporary directories.

Risk: Scheduled review features persist learning notes and review history in local JSON data.

Mitigation: Avoid storing sensitive notes unless the workspace is trusted, and confirm how retained JSON data can be deleted or exported.

Risk: Greeting retrieval can call external web sources during push workflows.

Mitigation: Restrict web fetching where needed and rely on the local fallback greetings when external access is unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elle-yu/skills/knowledge-review)
- [知识点分类规则](references/classify-rules.md)
- [专项管理规范](references/special-project-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style chat responses, JSON records, and command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces study records, review prompts, quiz content, progress summaries, and maintenance guidance for a local knowledge-review workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact body lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
