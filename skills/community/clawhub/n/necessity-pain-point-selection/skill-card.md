## Description: <br>
Helps e-commerce merchants mine utility-product reviews for concrete pain points and turn them into selection specs, product-improvement backlogs, QC checks, and validation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce merchants use this skill to analyze customer and competitor reviews for necessity and utility products, identify recurring complaint patterns, and convert those patterns into actionable sourcing, product improvement, and validation decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review exports may contain personal or confidential customer information. <br>
Mitigation: Remove or de-identify customer information before sharing generated summaries or using review data outside the intended analysis workflow. <br>
Risk: Keyword-based bulk classification can miss context or merge complaints too broadly. <br>
Mitigation: Use the script as a first-pass classifier only, then manually review, merge, and validate pain labels before making sourcing or product changes. <br>
Risk: Complaint counts can overstate the scale of a problem if they are not checked against review volume and rating distribution. <br>
Mitigation: Compare pain-label counts with total review volume, ratings, return reasons, and before/after metrics before prioritizing fixes. <br>


## Reference(s): <br>
- [Pain Point Framework](references/pain_point_framework.md) <br>
- [Review Mining Guide](references/review_mining_guide.md) <br>
- [Rijoy](https://www.rijoy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and concise recommendations, with optional shell commands for bulk review classification and JSON or table output from the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pain summary tables, selection spec lists, improvement backlogs, QC checklists, validation metrics, and script-generated pain-label counts.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
