## Description:

亚马逊投机型选品专家。适用于寻找短窗口机会、趋势型商品、快速增长商品、高上行空间产品，并需要明确识别风险的选品场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace sellers and product researchers use this skill to find high-volume, multi-seller products with short opportunity windows, then rank candidates by user-confirmed risk and profit preferences. It supports follow-up sorting, pagination, deduplication, Excel-style exports, and scheduled scouting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags credential, endpoint override, arbitrary-script, and persistent instruction capabilities.

Mitigation: Install only in a trusted LinkFox runtime, review or remove script patching and arbitrary script execution paths, and avoid endpoint overrides outside controlled development.

Risk: Onboarding and tool output may expose sensitive operational details in stdout or logs.

Mitigation: Treat logs and terminal output as sensitive, and avoid pasting credentials or private marketplace data into shared transcripts.

Risk: Scheduled tasks and public file uploads can run or publish data beyond the immediate chat interaction.

Mitigation: Confirm schedule frequency, task content, credit cost, and upload visibility before enabling automation or sharing generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-opportunistic-product-scout)
- [Product scout API parameter catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [SellerSprite product search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [ASIN scoring example expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [Task scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)
- [File upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries with tables and file paths, plus generated Excel, CSV, and JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are constrained to SellerSprite product fields; the skill states that product-scouting results should be delivered as Excel/CSV-style data rather than HTML reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
