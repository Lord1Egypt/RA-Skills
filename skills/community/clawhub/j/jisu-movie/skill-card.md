## Description:

查上映影片、影院排片、影片详情与城市影院列表等。当用户说：最近有什么好看的电影？附近哪家影院放映《xxx》？或类似电影影讯问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer movie availability, theater scheduling, movie detail, and city theater lookup questions through JisuAPI movie endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JisuAPI account key and sends lookup parameters such as city, theater, date, movie name, or movie ID to JisuAPI.

Mitigation: Use a restricted or quota-limited JISU_API_KEY, avoid unnecessary sensitive detail in queries, and rotate the key if it is exposed.

Risk: Returned image or ticket links may include non-HTTPS URLs.

Mitigation: Treat returned links as untrusted external content; verify links before opening or sharing them with users.

Risk: API quota, permission, maintenance, or rate-limit errors can interrupt movie lookup results.

Mitigation: Surface JisuAPI error messages clearly and avoid presenting failed or incomplete responses as confirmed schedules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/jisu-movie)
- [JisuAPI Movie API Documentation](https://www.jisuapi.com/api/movie/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON API results with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends movie lookup parameters to JisuAPI.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
