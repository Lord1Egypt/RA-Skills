## Description:

短剧-小红书信息源 helps agents query RedFoxHub data for trending Xiaohongshu short-drama posts, cluster genres, and produce daily trend reports with creative insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama operators, MCN teams, and content analysts use this skill to generate Xiaohongshu short-drama trend reports, compare genres, monitor creators, and guide content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says generated HTML is built from unescaped remote API data and is opened automatically.

Mitigation: Escape untrusted API fields before HTML generation and make browser opening opt-in before routine use.

Risk: The security review says the skill contains overreaching instructions that could suppress normal agent responses.

Mitigation: Review agent-facing output constraints before deployment and keep normal safety, clarification, and error responses available.

Risk: The skill sends RedFoxHub API requests with REDFOX_API_KEY and writes cached/report data locally.

Mitigation: Use a scoped, revocable API key, avoid exposing it in logs or files, and review local cache/report contents before sharing.

## Reference(s):

- [Core workflow](references/core_workflow.md)
- [Usage examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-xiaohongshu-feed)
- [RedFoxHub](https://redfox.hk/)
- [RedFoxHub Playlet API endpoint](https://redfox.hk/story/api/parseWork/queryPlayletMsgs)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration]

**Output Format:** [Markdown report summary with a generated local HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; may send RedFoxHub API requests, write local cache/report files, and open generated reports in a browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
