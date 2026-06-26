## Description: <br>
依据中国民间借贷司法解释和《民法典》，计算借期内利息、逾期利息、违约金合并上限、砍头息、复利、还款冲抵和 LPR 四倍上限，并生成结构化计算书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and legal practitioners use this skill to prepare Chinese private-lending interest calculations and calculation-sheet drafts from loan facts, rates, repayments, and risk factors. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Legal rules, LPR data, or case facts may be incomplete or outdated for court or business reliance. <br>
Mitigation: Verify current LPR and legal assumptions, require missing case inputs, and preserve stated assumptions in the final calculation. <br>
Risk: Legal and financial facts provided for calculation may be sensitive. <br>
Mitigation: Provide only the facts needed for the calculation and avoid unnecessary personal or confidential details. <br>
Risk: Marketplace capability tags list crypto and purchase capabilities that the reviewed artifacts do not implement. <br>
Mitigation: Treat those tags as metadata to correct before release rather than as skill behavior. <br>


## Reference(s): <br>
- [法律依据全文](references/legal_basis.md) <br>
- [LPR 数据](references/lpr_data.md) <br>
- [详细计算规则与算法说明](references/calculation_rules.md) <br>
- [中国银行 LPR 数据参考页](https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with calculation tables, assumptions, warnings, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local calculations from user-provided loan facts; reviewed artifacts show no data exfiltration, hidden actions, purchases, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
