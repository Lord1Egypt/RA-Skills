## Description:

ICP Filing rule consultation skill for Huawei Cloud that answers whether filing is required, filing process and materials questions, account and entity limits, change filing, access filing, cancellation filing, APP filing, and migration or transfer filing without performing filing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud after-sales technical engineers and support agents use this skill to answer Mainland China ICP filing questions with concise customer-facing guidance and relevant Huawei Cloud documentation links. It covers filing requirement, process, materials, access, change, cancellation, account limits, APP filing, and migration scenarios.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can use network-based document lookup beyond embedded guidance.

Mitigation: Allow network access only when documentation lookup is needed, and prefer the embedded knowledge base or direct Huawei Cloud support document URLs first.

Risk: Remote Chrome configuration may expose browser state or reachable internal resources if pointed at a non-isolated browser.

Mitigation: Use remote Chrome only in an isolated browser session with no sensitive logins and no internal-network reachability.

Risk: The helper tools are broader than the consultation scope.

Mitigation: Restrict fetch and search usage to approved Huawei Cloud documentation domains during deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-icp-rule-consult)
- [ICP Filing workflow](https://support.huaweicloud.com/usermanual-icp/zh-cn_topic_0000002127712329.html)
- [Regional ICP filing requirements](https://support.huaweicloud.com/prepare-icp/icp_02_0005.html)
- [Access filing workflow](https://support.huaweicloud.com/usermanual-icp/zh-cn_topic_0000002581758204.html)
- [APP characteristic information](https://support.huaweicloud.com/usermanual-icp/zh-cn_topic_0000002085120221.html)
- [references/catalog.yml](references/catalog.yml)
- [references/filing-rules.yml](references/filing-rules.yml)
- [references/doc-commands.md](references/doc-commands.md)
- [references/knowledge-base.md](references/knowledge-base.md)
- [references/prerequisites.md](references/prerequisites.md)
- [references/verification-method.md](references/verification-method.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text, shell commands]

**Output Format:** [Markdown or plain text with concise customer-facing answers and relevant document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include copyable shell commands for local document fetch or search setup when operational verification is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
