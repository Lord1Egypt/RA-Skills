## Description: <br>
ICD疾病分类与手术操作编码技能。熟练掌握中国ICD-10、ICD-9-CM-3、ICD-O编码体系，精通主要诊断选择原则（含黄锋版规则），熟悉DRG/DIP分组规则，支持诊断/手术主导词双向查找（内置词条数据库）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangnan](https://clawhub.ai/user/liangnan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical coders, health information management staff, and developers use this skill to look up Chinese ICD-10, ICD-9-CM-3, ICD-O, DRG, and DIP coding guidance and review diagnosis or procedure code selection. It is coding assistance and reference support, not clinical decision-making. <br>

### Deployment Geography for Use: <br>
Global, with content focused on Chinese ICD/DRG/DIP coding practice. <br>

## Known Risks and Mitigations: <br>
Risk: Medical coding outputs can be outdated or mismatched to the applicable ICD, DRG, DIP, clinical, or payer coding source. <br>
Mitigation: Verify coding suggestions and any added datasets against authoritative coding sources before use in reimbursement, reporting, or records workflows. <br>
Risk: Optional local Python lookup tools may be run with local datasets or inputs. <br>
Mitigation: Run the tools deliberately in an appropriate local environment and review any dataset changes before relying on the results. <br>
Risk: Patient-identifying information could be entered unnecessarily while seeking coding assistance. <br>
Mitigation: Use de-identified or minimal case details whenever possible because the skill is intended for coding reference support, not clinical decision-making. <br>


## Reference(s): <br>
- [ICD-Coding on ClawHub](https://clawhub.ai/liangnan/icd-coding) <br>
- [国家医保版ICD-10查询](https://code.nhsa.gov.cn/jbzd/public/dataWesterSearch.html) <br>
- [WHO ICD-10 Browser](https://icd.who.int/browse10/2022/en) <br>
- [WHO ICD-11 Browser](https://icd.who.int/browse/11) <br>
- [Clinical Term Mapping](docs/Clinical_Term_Mapping.md) <br>
- [DRG Knowledge](docs/DRG_Knowledge.md) <br>
- [Diagnosis Selection](docs/Diagnosis_Selection.md) <br>
- [Principal Diagnosis Procedure](docs/Principal_Diagnosis_Procedure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text with coding lookup results, rationale, and optional Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ICD, DRG, and procedure codes; users should verify outputs against authoritative coding sources.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
