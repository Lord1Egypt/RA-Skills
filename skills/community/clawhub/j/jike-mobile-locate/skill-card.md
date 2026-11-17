## Description:

查询中国大陆 11 位手机号的归属地省份/城市、运营商、运营商类型、区号、邮编和行政区划编码，数据由即刻数据（jikeapi.cn）接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI agents use this skill to look up mainland China mobile number attribution, including location, carrier, area code, postal code, and administrative code. It is intended for user-requested lookups and defaults to masked number display in text output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried phone numbers and the Jike AppKey are sent to the provider, and the security evidence reports that an undocumented endpoint override can redirect them to an arbitrary server.

Mitigation: Install only when that data sharing is acceptable; avoid querying real personal numbers without consent; keep JIKE_API_BASE_URL unset or constrain outbound traffic to https://api.jikeapi.cn.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-mobile-locate)
- [Publisher Profile](https://clawhub.ai/user/jikeapi-cn)
- [Jike Data Homepage](https://www.jikeapi.cn/)
- [Jike Mobile Query API Endpoint](https://api.jikeapi.cn/v1/mobile/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text lookup results or JSON emitted by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JIKE_MOBILE_KEY; accepts one or more 11-digit mainland China mobile numbers; masks phone numbers by default unless full display is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
