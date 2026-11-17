## Description:

User-configurable multi-slot news aggregation and push system. Schedule, topics, and keywords are defined by the user via config.json. Aggregates from Twitter, Hacker News, Tavily, filters by influence, summarizes, stores locally, supports feedback iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzlvv](https://clawhub.ai/user/hzlvv)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to configure recurring topic-based news pushes, fetch current items from selected sources, summarize them, deliver digests, and store feedback and usage history for later refinement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs and the bootstrap hook can trigger recurring agent activity after installation.

Mitigation: Review the skill before installing, test cron with dry-run mode, and enable cron or the hook only after the intended schedule and sources are confirmed.

Risk: Secrets and configuration handling require care during scheduled execution.

Mitigation: Use a dedicated skill-specific secrets file, avoid broad home-directory .env fallbacks, and never paste .env contents into chats or logs.

Risk: Stored feedback and configuration values may influence future filtering and summaries.

Mitigation: Treat stored config, push, and feedback data as untrusted; review changes before reuse and keep the data directory scoped to this skill.

## Reference(s):

- [News Digest Setup Guide](references/setup-guide.md)
- [Tavily](https://tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/hzlvv/skills/openclaw-new-digest)
- [Publisher Profile](https://clawhub.ai/user/hzlvv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digests and command-oriented guidance, with local JSON records for configuration, pushes, feedback, and usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and uses TAVILY_API_KEY for Tavily search and extract; XPOZ_API_KEY enables Twitter/X source coverage when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
