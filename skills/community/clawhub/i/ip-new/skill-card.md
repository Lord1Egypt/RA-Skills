## Description:

聚合数据IP归属地查询V3.0，支持IPv4查询国家/省份/城市/运营商

This skill is ready for commercial/non-commercial use.

## Publisher:

[365bug](https://clawhub.ai/user/365bug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query the country, province, city, and carrier for an IPv4 address through Juhe's IP lookup API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Juhe API key and queried IP address may be exposed because requests use plaintext HTTP.

Mitigation: Use only approved IP lookup data, avoid sensitive internal or customer IP addresses, and prefer a release that uses a verified HTTPS endpoint.

Risk: The skill requires a Juhe API key in the JUHE_API_KEY environment variable.

Mitigation: Protect the key as a secret, restrict access to runtime environments that need it, and rotate it if exposure is suspected.

Risk: The script depends on the Python requests package and network access to an external API.

Mitigation: Review dependencies and runtime network policy before deployment; use pinned dependencies where operational policy requires them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/365bug/skills/ip-new)
- [Juhe IP lookup API endpoint](http://apis.juhe.cn/ip/ipNewV3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON response printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, network access to Juhe, and JUHE_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
