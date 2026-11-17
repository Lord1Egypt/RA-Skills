## Description:

Use when 用户提供营业执照图片，或提供单位名称、经营范围和备案省份，要求检查 ICP 备案前置审批关键词及涉及/不涉及材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

面向在中国大陆办理华为云 ICP 备案的单位及其经办人员，用于按单位名称、完整经营范围和备案省份筛查随包规则中的前置审批关键词，并整理相关材料及属地模板信息。

### Deployment Geography for Use:

中国大陆

## Known Risks and Mitigations:

Risk: OCR may misread business-license details or mistake the registered address province for the filing province.

Mitigation: Confirm the company name, complete business scope, and filing province before running the screening.

Risk: The bundled rules are static and may not reflect later Huawei Cloud policy changes.

Mitigation: Check current official Huawei Cloud guidance when making filing decisions; treat this result as preliminary keyword screening.

Risk: Optional OCR dependencies are installed separately and recognized license text is returned to the agent.

Mitigation: Install reviewed dependency versions in an isolated environment and confirm extracted fields before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-icp-preapproval-check)
- [Huawei Cloud: preapproval industry categories](https://support.huaweicloud.com/prepare-icp/zh-cn_topic_0000002085124433.html)
- [Huawei Cloud: provincial preapproval templates](https://support.huaweicloud.com/prepare-icp/zh-cn_topic_0000001988829137.html)
- [Bundled Huawei rules](references/huawei-rules.json)
- [Official source verification record](references/official-sources.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with input details, a preapproval materials table, keyword matches, template information, tips, and a disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary keyword screening based on the supplied company name, complete business scope, filing province, and bundled rules; OCR fields require confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
