## Description:

Info Magnet lets an agent configure topic, RSS, and URL monitors, scan them periodically, and surface relevant new findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain local information trackers for topics, RSS feeds, and page URLs, then ask an agent to scan, de-duplicate, summarize, and group new findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves monitored topics, feed URLs, page URLs, seen history, and digests locally, which may expose sensitive interests or internal URLs on the user's machine.

Mitigation: Avoid adding sensitive topics, localhost, private-network, cloud metadata, file-scheme, or internal URLs; review and clear ~/.openclaw/memory when needed.

Risk: RSS feed and page text fetched from the network may contain untrusted content that could mislead downstream summaries.

Mitigation: Treat retrieved feed and page text as untrusted, and have the agent summarize only after filtering for relevance and checking source trust.

## Reference(s):

- [ClawHub skill page: Info Magnet](https://clawhub.ai/besty0121/skills/info-magnet)
- [ClawHub publisher profile: besty0121](https://clawhub.ai/user/besty0121)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style agent summaries, with local JSON and JSONL state files for magnets, seen URLs, and digests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library commands; stores monitored topics, feed URLs, page URLs, seen history, and digests under ~/.openclaw/memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
