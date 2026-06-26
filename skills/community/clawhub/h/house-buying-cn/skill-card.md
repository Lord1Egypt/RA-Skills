## Description: <br>
国内买房全流程助手，覆盖新房/二手房选购、预算计算、贷款规划、税费计算、合同审查、过户流程、看房检查清单、落户学区分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbmchina](https://clawhub.ai/user/xbmchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for China-focused home-buying planning, including budget ranges, mortgage comparisons, tax and fee estimates, new-home versus resale-home tradeoffs, contract review prompts, transfer timelines, and viewing checklists. It is most useful as practical guidance before confirming local rules with banks, agencies, or official housing authorities. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Mortgage, tax, and fee outputs may be inaccurate for a user's city, bank, property type, or current policy period. <br>
Mitigation: Treat calculations as estimates and verify city-specific rules, bank approvals, and official housing-agency requirements before making purchase decisions. <br>
Risk: The security guidance notes that the personal income tax exemption can be misapplied because the calculator does not separately ask whether the seller's home is the family's only housing. <br>
Mitigation: Confirm both holding period and family-only-home status before relying on any personal income tax exemption estimate. <br>


## Reference(s): <br>
- [贷款全攻略](references/loan_guide.md) <br>
- [新房 vs 二手房 完整对比](references/new_vs_secondhand.md) <br>
- [房产税费全解析](references/tax_fees.md) <br>
- [买房看房检查清单](assets/house_checklist.md) <br>
- [ClawHub skill listing](https://clawhub.ai/xbmchina/house-buying-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, calculation summaries, and optional Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are estimates and planning aids; tax, mortgage, eligibility, and school-district details require local verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
