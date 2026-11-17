## Description:

Generate a personalized global news briefing by asking about your interests, then searching the web and delivering a structured, readable digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christinazhang139](https://clawhub.ai/user/christinazhang139)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to request customized global news digests across topics, source regions, languages, and briefing depth. It is aimed at readers, researchers, writers, analysts, and curious users who want multiple media perspectives in a single structured briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends installing with an unpinned npx command, which can execute mutable package code during installation.

Mitigation: Review the installation path, prefer a pinned ClawHub CLI version or manually reviewed installation, and avoid elevated privileges.

Risk: Saved topics and language or depth preferences may be stored locally under the user's Claw data directory.

Mitigation: Ask users before saving preferences and avoid entering sensitive interests when local preference persistence is not appropriate.

Risk: Live news and social media results can include stale, misleading, or sentiment-only signals.

Mitigation: Prefer recent recognized publications or primary sources, label social media as sentiment rather than verified fact, and flag stories older than the stated recency window.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/christinazhang139/skills/global-perspectives-news-openclaw)
- [OpenClaw](https://openclaw.ai)
- [Tavily MCP](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefing with grouped stories, summaries, source links, takeaway text, and optional social sentiment section.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save user-selected topics, source regions, language, and depth preferences under the local Claw data directory when the user opts in.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
