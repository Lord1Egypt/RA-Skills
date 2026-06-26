## Description: <br>
该技能包为卫生技术评估研究人员、卫生经济学家和医药行业专业人士提供药物经济学评价流程、成本-效果与效用分析、敏感性分析和决策模型构建指导与 Python 工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlb1201](https://clawhub.ai/user/tlb1201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, health economists, HTA teams, and pharmaceutical professionals use this skill to structure pharmacoeconomic evaluations, calculate ICER and QALY measures, run sensitivity analyses, and document model assumptions for China-oriented assessment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect parameter values, assumptions, or data sources can lead to misleading pharmacoeconomic conclusions. <br>
Mitigation: Require expert review of model structure, parameter provenance, and sensitivity analysis before using results for policy, reimbursement, or clinical decisions. <br>
Risk: Local Python scripts may produce outputs that depend on user-supplied inputs and installed package versions. <br>
Mitigation: Review the scripts before execution, run them in a controlled environment, and validate outputs against independent calculations or accepted HTA methods. <br>


## Reference(s): <br>
- [中国药物经济学评价指南参考](references/china_guidelines.md) <br>
- [药物经济学模型构建方法参考](references/model_methods.md) <br>
- [参数管理指南](PARAMETER_MANAGEMENT.md) <br>
- [参数快速参考](PARAMETER_QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and generated analysis tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports pharmacoeconomic calculations, sensitivity analysis, Monte Carlo simulation, and parameter source documentation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
