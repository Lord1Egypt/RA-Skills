## Description:

沿指标树定位内容电商 GMV、转化率、ROI、费比、新客、复购和内容效率等指标波动的首个异常节点，并输出一个可验证的运营动作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External content-commerce operators and business owners use this skill to diagnose metric fluctuations across platforms such as Xiaohongshu and Douyin. It locks metric definitions, checks comparable baselines, excludes false fluctuations, drills into metric trees, and turns the first negative signal into a concrete test action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-run promotional onboarding and external WeChat contact suggestions may be unwanted in some deployments.

Mitigation: Review the onboarding behavior before installation and remove or disable promotional prompts where they do not fit the deployment policy.

Risk: The skill may write a marker file in the user's home directory and may persist business-sensitive diagnosis records in brand archive files.

Mitigation: Run it only in workspaces where persistence is acceptable, opt out of archive writes when needed, and avoid storing sensitive brand data unless retention is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-zhibiao)
- [内容电商指标树与公式](references/metric-trees.md)
- [子指标与运营动作映射](references/action-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic questions, preliminary judgments, or final diagnostic cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operating actions with freeze items, owners, observation windows, guardrail metrics, recovery standards, and stop standards.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
