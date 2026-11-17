## Description:

Search YouTube videos, channels, rankings, and trends through AIsa for YouTube research, competitor scouting, content discovery, and SERP-style analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content teams use this skill to search public YouTube results, find top-ranking videos, review competitor channels, and support trend or content-opportunity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search terms, country or language parameters, filter values, and the configured API key are sent to AIsa's API.

Mitigation: Avoid private or sensitive search queries and use a scoped API key when the provider supports it.

Risk: Returned video titles, URLs, metrics, or channel details may be incomplete, unavailable, or changed upstream.

Mitigation: Keep summaries grounded in returned results, avoid inventing missing details, and state clearly when no results are returned.

## Reference(s):

- [Openclaw Youtube ClawHub release](https://clawhub.ai/bibaofeng/skills/openclaw-youtube)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON results from the bundled CLI helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search commands may accept query, country, language, filter, count, competitor name, and topic parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
