## Description: <br>
User-configurable multi-slot news aggregation and push system that fetches from Twitter, Hacker News, and Tavily, then filters, summarizes, stores, and delivers digest updates based on user-defined schedules and topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hzlvv](https://clawhub.ai/user/Hzlvv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure recurring news digest slots, gather relevant items from supported news and social sources, summarize them, and send manual or scheduled updates through OpenClaw-supported messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled agent runs may execute automatically after cron is enabled. <br>
Mitigation: Review cron entries before enabling them and install only where scheduled OpenClaw sessions are expected. <br>
Risk: The scheduled runner loads .env files before starting OpenClaw, which can expose broader environment configuration than intended. <br>
Mitigation: Use a dedicated .env containing only TAVILY_API_KEY and XPOZ_API_KEY, and avoid relying on ~/.env for this workflow. <br>
Risk: Resetting configuration can overwrite the saved news schedule. <br>
Mitigation: Confirm schedule reset intent before running manage-config.mjs reset and keep a copy of important slot settings. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Hzlvv/openclaw-new-digest) <br>
- [Publisher Profile](https://clawhub.ai/user/Hzlvv) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest messages with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include source URLs, summaries, usage counts, stored push records, and feedback-aware configuration guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
