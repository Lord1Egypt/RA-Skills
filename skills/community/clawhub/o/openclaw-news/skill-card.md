## Description: <br>
Aggregates and delivers curated briefings about OpenClaw releases, skills, security items, community discussions, and ecosystem news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to collect OpenClaw ecosystem updates from public GitHub, ClawHub, search, and community sources, then send concise briefings on demand or on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public news, registry, GitHub, and search-provider lookups, which can reveal what ecosystem topics the agent is monitoring. <br>
Mitigation: Use it for public OpenClaw ecosystem monitoring and avoid adding private or sensitive search queries. <br>
Risk: Scheduled runs can create recurring external API calls and recurring briefings. <br>
Mitigation: Add cron entries only when recurring briefings are desired; otherwise run the skill on demand. <br>
Risk: Briefings depend on external source availability and may be incomplete or stale. <br>
Mitigation: Treat the briefing as a curated summary and verify linked source material before acting on release or security information. <br>


## Reference(s): <br>
- [OpenClaw News on ClawHub](https://clawhub.ai/arc-claw-bot/openclaw-news) <br>
- [ClawHub Registry](https://www.clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings with JSON collection state and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports incremental or full scans and keeps local state to reduce repeated items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
