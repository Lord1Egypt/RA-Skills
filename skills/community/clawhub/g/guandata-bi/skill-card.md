## Description:

使用观远BI来进行数据获取与数据分析，帮助代理查询数据、创建图表、查看报表并分析营业额、门店、会员和订单等业务指标。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengyuhe123](https://clawhub.ai/user/zhengyuhe123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to let an agent operate Guandata BI through a local CLI: list datasets and fields, create BI cards and pages, fetch card data, search filter values, and generate chart-backed analysis. It is intended for environments where the agent can be trusted with BI credentials and access to business data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Guandata BI credentials and the artifact stores them in config.json as plaintext.

Mitigation: Use a least-privileged dedicated BI account and protect, avoid, or rotate any local plaintext credential file.

Risk: The skill can read business data and automatically cache query results locally.

Mitigation: Review local cache retention, restrict filesystem access, and clean cached CSV/JSON files according to data-handling policy.

Risk: Untrusted task names or dataset identifiers can affect cache paths or BI operations.

Mitigation: Use trusted task and dataset values only, and review agent-generated command arguments before execution.

Risk: The security evidence flags an unsafe repeated publish bug in version 7 page publishing.

Mitigation: Fix or disable version 7 release_page publishing before using page publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengyuhe123/skills/guandata-bi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON parameters, configuration examples, and CSV cache file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands may create or modify Guandata BI pages/cards and may write local CSV or JSON cache files.]

## Skill Version(s):

3.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
