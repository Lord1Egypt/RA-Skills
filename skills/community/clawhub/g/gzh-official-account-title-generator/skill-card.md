## Description:

基于公众号热门数据生成爆款标题，或对已有标题进行多维度评分并给出优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

公众号号主、内容运营、新媒体编辑、MCN 和品牌团队可用它根据公众号热门数据生成 10 个候选标题，或对已有标题进行四维度评分并获得优化建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends title keywords to redfox.hk.

Mitigation: Use a scoped or revocable key, confirm its source and scope before use, and avoid submitting sensitive or confidential title keywords.

Risk: Debug mode can expose request details, including headers or API responses, in logs.

Mitigation: Avoid --debug unless key logging is fixed, and redact credentials before sharing logs or generated output.

Risk: The helper script writes Markdown files in the working directory by default.

Mitigation: Run the skill in a directory where generated files cannot overwrite important documents, or pass an explicit safe output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/gzh-official-account-title-generator)
- [RedFoxHub](https://redfox.hk)
- [RedFox WeChat data API endpoint](https://redfox.hk/story/api/cozeSkill/getWxCozeSkillData)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown title candidates or scoring reports, with helper-script JSON status and generated Markdown data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY. Source data is limited to yesterday through 30 days prior and is not real time.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
