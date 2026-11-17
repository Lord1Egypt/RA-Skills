## Description:

根据 IP 查归属地与运营商类型。当用户说：这个 IP 是哪里的？是不是机房 IP？或类似 IP 归属问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query an IP address and summarize its reported geographic attribution and operator type. It is intended for IP attribution questions, including whether an IP appears to be associated with a data center.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IP addresses are sent to JisuAPI.

Mitigation: Avoid submitting sensitive internal or private IPs unless disclosure to JisuAPI is acceptable.

Risk: The JISU_API_KEY is stored in the environment and may be exposed if request URLs or process environments are logged.

Mitigation: Use a dedicated, restricted, quota-limited key and rotate it if logs may have captured request details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/ip)
- [JisuAPI IP Query API documentation](https://www.jisuapi.com/api/ip/)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the lookup script with concise natural-language guidance for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, outbound HTTPS access to JisuAPI, and a JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
