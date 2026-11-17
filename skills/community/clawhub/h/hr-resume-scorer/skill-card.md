## Description:

简历批量筛选打分工具。支持PDF/Word/TXT格式简历解析，基于JD进行匹配度分析，多维度评分，生成Excel/JSON/Markdown报告。当用户需要筛选简历、批量评估候选人、简历打分、匹配度分析、生成筛选报告时触发此技能。适用于HR、猎头、招聘团队。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwu2495](https://clawhub.ai/user/jiuwu2495)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams, recruiters, and hiring support staff use this skill to parse resume files, compare candidates against a job description, score candidates across multiple dimensions, and generate screening reports for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive candidate resume data and can generate reports containing personal information.

Mitigation: Use it only for authorized HR workflows, define deletion and redaction rules for generated reports and temporary files, and limit processing to approved files.

Risk: Broad file selection or local-file handling may expose unintended documents.

Mitigation: Process only explicit files in a dedicated working directory and review selected inputs before running batch analysis.

Risk: Guidance around third-party compression services and elevated execution may create privacy or system-risk concerns.

Mitigation: Avoid external compression services for resumes, do not run the workflow as administrator, and pin dependencies in a virtual environment.

Risk: Subjective scoring and risk labels can be mistaken for automated hiring decisions.

Mitigation: Treat scores, recommendations, authenticity labels, and retention-risk labels as prompts for human review rather than final employment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuwu2495/skills/hr-resume-scorer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated agent outputs may include Excel, JSON, or Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes PDF, Word, TXT, and Markdown resume inputs; documented limits are 10MB per file and 100MB per batch.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
