## Description:

输入经度、纬度和坐标系，调用即刻数据反查完整地址及国家、省、市、区、乡镇和街道信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert longitude and latitude into a readable address and administrative hierarchy through the Jike geocoding API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An endpoint override can send exact coordinates and the API key to an unintended server.

Mitigation: Keep JIKE_API_BASE_URL unset or locked to the intended HTTPS Jike endpoint before running the skill.

Risk: Reverse-geocoding sensitive coordinates discloses those coordinates to a third-party API provider.

Mitigation: Avoid submitting coordinates for sensitive places unless that third-party disclosure is acceptable.

Risk: The API credential can be exposed or overused if it is broad or long-lived.

Mitigation: Use a narrow, rotatable Jike AppKey in a trusted runtime environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-map-geocode-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike geocode query endpoint](https://api.jikeapi.cn/v1/map/geocode/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from the geocoding script, typically summarized for the user in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JIKE_MAP_GEOCODE_QUERY_KEY or JIKE_APPKEY credential.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
