## Description: <br>
按公历日期查询黄历、每日宜忌、吉凶判断、神煞冲煞，并支持区间批量筛选吉日。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leocdchina](https://clawhub.ai/user/leocdchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Chinese almanac questions such as today's auspicious activities, whether a date suits moving or marriage, and which dates in a range match a planned activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a HUANGLI_TOKEN and sends requests to an external API service. <br>
Mitigation: Keep the token private, use it only in approved environments, and rotate it if it is exposed. <br>
Risk: Changing HUANGLI_BASE can send requests and credentials to a different API endpoint. <br>
Mitigation: Leave the default API base unless the replacement endpoint is fully trusted. <br>
Risk: Calendar and activity queries may reveal personal planning details to the service provider. <br>
Mitigation: Avoid sending sensitive personal context and provide only the dates or activity keywords needed for lookup. <br>


## Reference(s): <br>
- [Huangli service homepage](https://nongli.skill.4glz.com) <br>
- [Huangli token dashboard](https://nongli.skill.4glz.com/dashboard) <br>
- [Huangli Toolkit Reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HUANGLI_TOKEN and HTTPS access to api.nongli.skill.4glz.com; HUANGLI_BASE can override the API base.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
