## Description:

查配件品牌、OE 号模糊搜、适用车型与替换件等。当用户说：这个原厂零件号对应什么件？有没有替换件？或类似汽车 OE 配件问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query automotive OE part data from JisuAPI, including part brands, fuzzy OE number matches, compatible vehicle models, and replacement parts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automotive part lookup inputs and the configured JisuAPI AppKey are sent to JisuAPI.

Mitigation: Use a dedicated, limited-quota API key, avoid sensitive business context in lookup fields, and treat URL or query-string logs for this traffic as sensitive.

## Reference(s):

- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Automotive Parts OE API](https://www.jisuapi.com/api/parts/)
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/parts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
