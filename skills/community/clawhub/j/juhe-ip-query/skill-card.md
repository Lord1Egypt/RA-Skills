## Description:

Looks up IPv4 geolocation details, including country, province, city, and ISP, through the Juhe IP attribution API for single or batch IP queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jenius-cn](https://clawhub.ai/user/jenius-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify the public IPv4 location and ISP for one or more IP addresses. It is useful for routine IP attribution checks where sending queried public IP addresses to Juhe is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send the user's API key and queried IP addresses over unencrypted HTTP.

Mitigation: Use only for non-sensitive public IP lookups, prefer the JUHE_IP_KEY environment variable instead of --key, and require an HTTPS endpoint before treating the skill as low risk.

Risk: Queried public IP addresses are sent to Juhe for lookup.

Mitigation: Avoid using the skill with sensitive customer, incident-response, or internal infrastructure data unless that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jenius-cn/skills/juhe-ip-query)
- [Jenius.cn publisher profile](https://clawhub.ai/user/jenius-cn)
- [Juhe IP attribution API documentation](https://www.juhe.cn/docs/api/id/1)
- [Juhe data platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance, command examples, tables, and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_IP_KEY credential; supports single and batch IPv4 lookups.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
