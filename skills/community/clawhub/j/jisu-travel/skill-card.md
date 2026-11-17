## Description:

聚合航班列表、景点信息，火车段可走 train 能力。当用户说：查一下上海到东京的航班、杭州有什么景点推荐、顺带帮我看看火车票，或类似出行规划问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up flight options, scenic attraction listings, and train station, line, or ticket information for travel planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel search details may be sent to ly.com and JisuAPI.

Mitigation: Avoid entering highly sensitive itinerary details unless sharing them with those providers is acceptable.

Risk: JisuAPI train queries require an API key that may consume quota or incur billing.

Mitigation: Use a limited JisuAPI key where possible and monitor quota and billing.

Risk: Runtime dependencies can introduce supply-chain or compatibility risk.

Mitigation: Install dependencies in a virtual environment with reviewed or pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-travel)
- [Publisher profile](https://clawhub.ai/user/jisuapi)
- [Tongcheng Travel](https://www.ly.com/)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI train API](https://www.jisuapi.com/api/train/)
- [Airport code reference](artifact/airport.md)
- [City ID reference](artifact/city.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance with shell command examples and JSON travel lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY for train queries; flight and scenery results depend on ly.com page availability.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
