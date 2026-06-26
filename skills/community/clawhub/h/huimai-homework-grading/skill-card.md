## Description: <br>
中国中小学作业批改与学生学业综合评估。教师拍照扫描批改作业、生成单生/全班单科及综合学科知识掌握评估图并给出指导建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, class advisers, grade leaders, and school administrators use this skill to review photographed or scanned homework, connect question results to knowledge points, and generate individual, class, subject, or cross-subject learning assessment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student homework, names, IDs, grades, and assessment reports can contain sensitive personal data. <br>
Mitigation: Use local or private OCR where possible, limit access by role, and desensitize data before sending it to cloud services. <br>
Risk: OCR services and provider credentials may be exposed during deployment or integration. <br>
Mitigation: Restrict service ports, store API keys in protected secret management, and review network exposure before production use. <br>
Risk: Automated grading and learning guidance may be inaccurate, especially for handwriting, formulas, and subjective answers. <br>
Mitigation: Keep teacher review in the workflow for subjective items and audit generated guidance before sharing it with students or families. <br>
Risk: Commercial deployment terms may require publisher confirmation. <br>
Mitigation: Confirm the applicable license and any school, institutional, or commercial agreement with the publisher before deployment. <br>


## Reference(s): <br>
- [数据模型参考](references/data-model.md) <br>
- [权限模型参考](references/permission-model.md) <br>
- [评估图表规格](references/chart-spec.md) <br>
- [OCR引擎选型与拍照批改技术方案](references/ocr-implementation.md) <br>
- [OCR 技术选型建议](references/ocr-selection.md) <br>
- [知识点-教材版本映射方案](references/textbook-mapping.md) <br>
- [教材版本知识点映射方案](references/textbook-version-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, code snippets, shell commands, configuration examples, charts, and assessment report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe OCR workflows, role-based access models, knowledge-point mappings, and homework grading outputs; no executable payload is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
