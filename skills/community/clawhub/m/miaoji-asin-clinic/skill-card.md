## Description: <br>
Miaoji Asin Clinic helps Amazon sellers diagnose listing health across compliance, advertising, reviews, visuals, and content, then prioritize repair guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and marketplace operators use this skill to score an ASIN listing, identify weak health dimensions, and receive prioritized repair recommendations and handoff templates for related optimization skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide more seller or customer data than the diagnostic requires. <br>
Mitigation: Use summarized ASIN, advertising, review, image, and video metrics, and avoid credentials, private seller exports, or full customer records. <br>
Risk: Generated listing repair guidance may be based on incomplete or estimated marketplace metrics. <br>
Mitigation: Cross-check recommendations against Amazon Seller Central data and treat estimated fields as inputs for review before making listing changes. <br>
Risk: Compliance and advertising recommendations may not reflect every current marketplace policy or campaign constraint. <br>
Mitigation: Review proposed changes against current Amazon policy, account requirements, and campaign goals before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/miaoji-asin-clinic) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [评分矩阵](references/diagnosis-matrix.md) <br>
- [使用指南](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown diagnostic reports and optional JSON analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes five-dimension scores, lifecycle-aware repair priority, recommended related skills, and input templates for follow-up remediation.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
