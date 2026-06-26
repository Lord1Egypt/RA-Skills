## Description: <br>
Autonomous engagement bot for Twitter, Farcaster, and Moltbook that fetches trending content, generates persona-driven contextual replies, and tracks replied posts to prevent duplicates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Story91](https://clawhub.ai/user/Story91) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate social engagement across connected Twitter, Farcaster, and Moltbook accounts while applying a configured persona and duplicate-reply tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post public replies from connected social accounts. <br>
Mitigation: Run manual tests first, keep reply limits low, and add a dry-run or explicit confirmation step before enabling live posting. <br>
Risk: The configuration handles API keys and Farcaster wallet signing material. <br>
Mitigation: Use dedicated low-value accounts and a low-balance Farcaster wallet, keep config.json out of git, restrict file permissions, and rotate credentials if exposed. <br>
Risk: Cron-based automation can amplify unwanted posts or configuration mistakes. <br>
Mitigation: Avoid cron until manual tests are complete, monitor logs and platform rate limits, and review state files after each run. <br>


## Reference(s): <br>
- [Persona Configuration Guide](references/persona-config.md) <br>
- [Platform APIs Reference](references/platform-apis.md) <br>
- [Reply Strategies Guide](references/reply-strategies.md) <br>
- [Multi-Channel Engagement Agent on ClawHub](https://clawhub.ai/Story91/multi-channel-engagement-agent) <br>
- [Story91 Publisher Profile](https://clawhub.ai/user/Story91) <br>
- [X Developer Portal](https://developer.x.com/en/portal/dashboard) <br>
- [Neynar Developer Portal](https://dev.neynar.com) <br>
- [Moltbook API](https://www.moltbook.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the included script may post public replies through platform APIs and write local engagement state files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
