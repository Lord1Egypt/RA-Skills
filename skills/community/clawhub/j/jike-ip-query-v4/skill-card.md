## Description:

Queries a supplied IPv4 address through Jike API and returns country, province, city, ISP, and long_ip values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer IPv4 geolocation and carrier questions by validating an IPv4 address, calling the Jike data API, and returning the lookup result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IPv4 addresses and the Jike AppKey are sent to the provider during lookup.

Mitigation: Use the skill only for lookups appropriate to share with Jike API, and configure the AppKey through a protected environment variable.

Risk: An altered JIKE_API_BASE_URL environment variable could redirect the queried IP and AppKey to another server.

Mitigation: Run the skill in a trusted environment where untrusted users cannot set JIKE_API_BASE_URL, and leave the variable unset for normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-ip-query-v4)
- [Jike API Homepage](https://www.jikeapi.cn/)
- [Jike IPv4 Query API Endpoint](https://api.jikeapi.cn/v1/ip/query/v4)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Jike AppKey and one IPv4 address per lookup.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
