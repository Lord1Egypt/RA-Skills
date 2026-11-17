## Description:

招聘需求智能解读技能，将粘贴、上传或URL提供的岗位JD拆解为结构化岗位画像、显性与隐性需求、需求权重、差距自评、面试预测、学习路线、ATS关键词和可选薪资对标分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to understand a job description before tailoring a resume, preparing for interviews, or deciding whether to apply. It produces a structured JD interpretation and can guide follow-on resume matching or resume rewriting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute injected browser code from malicious job-description content.

Mitigation: Use the skill only with trusted job descriptions or URLs, and avoid opening generated reports from untrusted postings until report content is escaped.

Risk: analysis.json and generated HTML reports may contain private job-search notes or self-assessment information.

Mitigation: Manually delete analysis.json and generated HTML reports when they contain sensitive job-search or self-assessment data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/jd-interpreter)
- [analysis.json Schema Reference](references/analysis_schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Guidance]

**Output Format:** [Structured analysis text with JSON input for an optional generated interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report generator reads analysis.json and writes jd-interpretation-report.html; optional salary benchmarking may use web search when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
