## Description:

提供中文日常营养支持，包括热量与宏量营养素估算、餐食规划、食物替换、外食估算，以及用户明确要求的饮食和饮水记录。仅在用户明确请求营养或饮食帮助时使用；不要因“吃什么”“减肥”“记录”等孤立通用词自动触发。不得用于医疗诊断、疾病治疗、孕期或进食障碍管理，也不得默认读写本地健康数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamyeed](https://clawhub.ai/user/yamyeed)

### License/Terms of Use:

MIT-0

## Use Case:

面向明确寻求日常饮食帮助的成年人，用于估算食物与餐食的热量和宏量营养素、规划普通餐食、比较食物替换方案，以及在明确授权后整理饮食或饮水记录。它不用于诊断或治疗疾病，也不提供孕期、进食障碍或其他高风险情境的个体化方案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved dietary and body-related records may contain sensitive personal information, and plaintext files may be accessible to other local programs or backups.

Mitigation: Keep data in the current conversation by default. Before saving, explain the fields, exact path, purpose, and plaintext-storage risk, then wait for confirmation; do not upload or sync the records.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yamyeed/skills/nutrition-advisor)
- [Calculation and estimation guidance](references/calculations-and-estimation.md)
- [Logging and local storage guidance](references/logging-and-storage.md)
- [Special contexts and safety boundaries](references/special-contexts.md)
- [NIH Office of Dietary Supplements](https://ods.od.nih.gov/factsheets/list-all/)
- [NCCIH Herbs at a Glance](https://www.nccih.nih.gov/health/herbsataglance)
- [Chinese Nutrition Society](https://www.cnsoc.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese-language estimates, explanations, and meal suggestions; optional structured summaries of user-provided food and water records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ranges and states assumptions and uncertainty. Saved records are not created by default and require explicit user request and confirmation.]

## Skill Version(s):

4.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
