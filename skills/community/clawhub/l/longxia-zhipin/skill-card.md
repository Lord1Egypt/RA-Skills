## Description: <br>
龙虾直聘 helps agents turn a company or industry profile into role-based ClawHub skill package recommendations and installs selected skills only after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tato447](https://clawhub.ai/user/tato447) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, founders, and operators use this skill to analyze a company or industry profile, find matching ClawHub skills, and assemble a compact role-based package for business, delivery, and growth teams. The skill is intended for recommendation and confirmation-gated installation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend an unsuitable skill package if company, industry, or role context is incomplete or inaccurate. <br>
Mitigation: Review the company snapshot and proposed skills before installation, and approve only skills that match the intended team roles. <br>
Risk: Fallback installation may introduce different skills than the first recommendation. <br>
Mitigation: Treat fallback installs as a separate confirmation decision and continue only after reviewing the replacement mapping. <br>
Risk: Company or hiring details provided for lookup-based analysis may be sensitive. <br>
Mitigation: Avoid entering confidential company details unless they are appropriate for lookup-based analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tato447/longxia-zhipin) <br>
- [行业分类词库](references/industry-taxonomy.md) <br>
- [角色技能包手册](references/role-pack-playbook.md) <br>
- [English Output Templates](references/output-templates-en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with grouped skill candidates, install confirmation prompts, and install result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawHub skill identifiers, install order, fallback recommendations, and explicit confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
