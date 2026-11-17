## Description:

newsflash helps agents create personalized daily news briefings and real-time breaking-news alerts from newsflash.sh using deduplicated events with corroboration counts and confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zatmonkey](https://clawhub.ai/user/zatmonkey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for daily news digests, ad-hoc topic briefings, and breaking-news alerts backed by Newsflash event data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned npm CLI in the workspace.

Mitigation: Prefer a version-pinned CLI or direct HTTPS workflow, and require user approval before running npm-based commands.

Risk: The skill can create persistent configuration, start live streams, and schedule recurring briefing activity.

Mitigation: Require explicit approval before creating newsflash.json, starting background streams, or scheduling cron jobs.

Risk: The CLI process could be exposed to unrelated workspace secrets.

Mitigation: Run commands with a minimal environment and avoid passing unrelated credentials to the Newsflash CLI process.

## Reference(s):

- [Newsflash homepage](https://newsflash.sh)
- [Newsflash events API example](https://newsflash.sh/api/events?limit=1)
- [ClawHub skill page](https://clawhub.ai/zatmonkey/skills/newsflash)
- [ClawHub publisher profile](https://clawhub.ai/user/zatmonkey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings and alerts with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are intended to stay concise and to label single-source items as unconfirmed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
