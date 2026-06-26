## Description: <br>
Supports packaging solution design, packaging material selection, and regulatory review for product packaging and material changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyxuq](https://clawhub.ai/user/cloudyxuq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Packaging designers, product teams, and compliance reviewers use this skill to draft packaging structures, choose materials, compare basic packaging costs and dimensions, and review food-package material and labeling requirements. <br>

### Deployment Geography for Use: <br>
Global; regulatory reference material is focused on Chinese GB food-packaging standards. <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports unsafe food-packaging material guidance, including recommendations that should not be relied on for food or beverage packaging compliance. <br>
Mitigation: Review and correct material guidance before use; replace unsafe food-contact recommendations with verified alternatives and validate all advice against the target market's regulations. <br>
Risk: Regulatory guidance is jurisdiction-specific and may become outdated. <br>
Mitigation: Use current official regulations for the target market before approving labels, claims, food-contact materials, or supplier specifications. <br>
Risk: The helper script provides simplified packaging cost, dimension, barrier, and shrinkage calculations. <br>
Mitigation: Treat script outputs as estimates and verify final packaging specifications with engineering tests, supplier data, and compliance review. <br>


## Reference(s): <br>
- [Food packaging material selection guide](references/material_selection.md) <br>
- [Food packaging regulatory checklist](references/package_regulations.md) <br>
- [Packaging calculator helper script](scripts/package_calculator.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON output from the packaging calculator script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write packaging specifications, material lists, and compliance notes under data/package/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
