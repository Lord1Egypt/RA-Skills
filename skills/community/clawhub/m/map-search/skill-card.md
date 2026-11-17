## Description:

Map Search helps agents search Amap, Baidu Maps, and Tencent Maps for keyword and nearby place results in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoucangjia1qu](https://clawhub.ai/user/shoucangjia1qu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to look up places by keyword, region, or nearby coordinates across Chinese map providers. It is useful when an agent needs terminal-readable place names, addresses, locations, and distances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, regions, and nearby-search coordinates are sent to external map providers.

Mitigation: Use the skill only for data that may be shared with Amap, Baidu, and Tencent under the configured API keys.

Risk: Installing dependencies or creating a system-wide command can affect the runtime environment.

Mitigation: Use a virtual environment with pinned dependencies and create the /usr/local/bin symlink only when a system-wide command is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shoucangjia1qu/skills/map-search)
- [Amap Open Platform](https://lbs.amap.com/)
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/)
- [Tencent Location Service](https://lbs.qq.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests package, and at least one configured provider API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
