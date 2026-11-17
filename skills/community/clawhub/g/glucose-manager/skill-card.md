## Description:

管理个人血糖数据，支持手动记录、文件导入、血糖趋势预测和健康建议。当用户提到血糖、糖尿病管理、血糖记录、血糖预测、饮食建议、运动建议时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liningg](https://clawhub.ai/user/liningg)

### License/Terms of Use:

MIT-0

## Use Case:

External users can record and import personal blood glucose readings, review trends and reports, and receive informational diet, exercise, monitoring, and care-seeking guidance. The skill is intended for tracking and education, not diagnosis, urgent care, or treatment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive health records as plaintext local files.

Mitigation: Use it only on a trusted device and protect the local data directory with appropriate operating-system access controls.

Risk: The skill provides medical-style predictions and recommendations that may be incorrect or incomplete.

Mitigation: Treat outputs as informational and confirm care, medication, urgent symptoms, and treatment decisions with a qualified healthcare provider.

Risk: Imported files, unit handling, deletes, exports, and HTML reports can affect data integrity or expose private information.

Mitigation: Review imports and unit choices before saving, confirm destructive or export actions, and inspect reports before sharing them.

## Reference(s):

- [Blood Glucose Manager Page](https://clawhub.ai/liningg/skills/glucose-manager)
- [Data Schema](artifact/references/data_schema.md)
- [血糖分析方法说明](artifact/references/analysis_methods.md)
- [Prediction Algorithms](artifact/references/prediction_algorithms.md)
- [Glucose Reference Ranges](artifact/references/glucose_ranges.md)
- [Blood Glucose Management References](artifact/references/glucose_guidelines.md)
- [血糖管理知识库](artifact/references/glucose_knowledge.md)
- [血糖指数（GI）参考指南](artifact/references/glycemic_index.md)
- [运动与血糖管理指南](artifact/references/exercise_guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON data, HTML reports, PNG charts, guidance]

**Output Format:** [Markdown or plain text responses with optional shell commands and generated local JSON, HTML, or chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads local health records under the user's home directory; report generation may create local HTML, JSON, text, or image outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/skill.json, README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
