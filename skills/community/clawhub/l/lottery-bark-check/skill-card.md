## Description:

中国彩票开奖核对与 Bark 推送技能。必须配合 Bark App 使用：抓取中彩网（双色球）与 500 网（大乐透）官方最新开奖，与用户守号比对，判定奖级与金额，按定稿蓝黑版式生成报告，并通过 Bark 推送（group 固定「彩票」，需自备 Bark device_key）到手机，每天定时核对不漏期。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonamsong96](https://clawhub.ai/user/jonamsong96)

### License/Terms of Use:

MIT

## Use Case:

Lottery players use this agent skill to compare saved 双色球 and 大乐透 numbers with the latest published draws, calculate prize tiers and amounts, and receive a formatted result through Bark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bark workflow sends notification content and a device key through Bark, and the security guidance calls for checking that the privacy description is accurate.

Mitigation: Confirm what the Bark service receives and that the privacy description reflects it; keep the device key private and use --dry-run to preview notifications.

Risk: Scheduled runs can send reports without a person reviewing each run.

Mitigation: Review the schedule and saved numbers before enabling unattended runs, and verify the output with --dry-run first.

Risk: The security review is incomplete because two local references could not be resolved.

Mitigation: Review the unresolved references and complete the security review before installation or scheduled use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jonamsong96/skills/lottery-bark-check)
- [Publisher profile](https://clawhub.ai/user/jonamsong96)
- [Bark Markdown formatting notes](references/bark-markdown.md)
- [China Welfare Lottery draw data endpoint](https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=1)
- [500.com Super Lotto results](https://datachart.500.com/dlt/history/newinc/history.php?start=26000&end=29999)
- [Bark](https://bark.day.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown notification report and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report contains draw results, matched numbers, prize tier, and amount; delivery can be previewed locally or sent through Bark.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
