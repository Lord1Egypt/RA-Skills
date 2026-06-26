## Description: <br>
管理个人血糖数据，支持手动记录、文件导入、血糖趋势预测和健康建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liningg](https://clawhub.ai/user/liningg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents assisting them use this skill to record local blood glucose readings, import glucose logs, review trends, generate reports, estimate short-term risk, and receive informational diet, exercise, medication, and care-seeking guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data stored locally under the workbuddy directory. <br>
Mitigation: Use it only when local storage of glucose records is acceptable, and protect the device and files according to the user's health-data privacy requirements. <br>
Risk: The skill can produce treatment-style diabetes, prediction, insulin, medication, diet, exercise, and care-seeking guidance. <br>
Mitigation: Treat all guidance and predictions as informational and do not use them to change medication, insulin dose, or emergency care decisions without a clinician. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liningg/glucose-manager) <br>
- [Glucose Reference Ranges](artifact/references/glucose_ranges.md) <br>
- [Glucose Guidelines](artifact/references/glucose_guidelines.md) <br>
- [Blood Glucose Analysis Methods](artifact/references/analysis_methods.md) <br>
- [Prediction Algorithms](artifact/references/prediction_algorithms.md) <br>
- [Data Schema](artifact/references/data_schema.md) <br>
- [Exercise Guidelines](artifact/references/exercise_guidelines.md) <br>
- [Glycemic Index](artifact/references/glycemic_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Natural-language responses, command examples, JSON or CSV data files, and exported HTML, Markdown, PNG, or chart reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores glucose records locally and may generate predictions or health guidance that should remain informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
