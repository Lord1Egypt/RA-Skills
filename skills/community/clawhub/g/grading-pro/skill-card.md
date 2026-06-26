## Description: <br>
文科主观题智能批改评分系统，支持初高中英语写作、语文作文和语文阅读理解的评分、错误分析、改进建议和优化范文生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makiwinster72](https://clawhub.ai/user/makiwinster72) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers and education-focused agent users can use this skill to apply local rubric files when grading middle-school and high-school Chinese and English subjective assignments. It helps produce score breakdowns, error analysis, improvement advice, and revised exemplar answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student submissions can contain personal or sensitive information. <br>
Mitigation: Redact student identifiers when possible and supervise how student work is handled before sharing it with an agent. <br>
Risk: Incorrect rubric selection or unsupervised rubric changes could lead to unfair or inconsistent grades. <br>
Mitigation: Confirm the rubric before grading, review any proposed criteria/*.json change, and keep a backup before making permanent updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makiwinster72/grading-pro) <br>
- [README](README.md) <br>
- [初中英语书面表达 rubric](criteria/english_writing_junior.json) <br>
- [高中英语书面表达 rubric](criteria/english_writing_senior.json) <br>
- [高中英语应用文 rubric](criteria/english_practical_senior.json) <br>
- [高中英语读后续写 rubric](criteria/english_continuation_senior.json) <br>
- [初中语文作文 rubric](criteria/chinese_essay_junior.json) <br>
- [高中语文作文 rubric](criteria/chinese_essay_senior.json) <br>
- [初中语文阅读理解 rubric](criteria/chinese_reading_junior.json) <br>
- [高中语文阅读理解 rubric](criteria/chinese_reading_senior.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown or structured text grading reports with score breakdowns, comments, and optional rubric updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON rubric files and may propose changes to criteria files when teachers add standards.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
