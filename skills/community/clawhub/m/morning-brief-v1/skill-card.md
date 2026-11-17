## Description:

Morning Brief fetches current international, technology, science, gaming, and release headlines from selected RSS feeds and presents them as a concise briefing with clickable Markdown links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amadeus9169](https://clawhub.ai/user/amadeus9169)

### License/Terms of Use:

MIT-0

## Use Case:

Users who want a quick morning or daily world briefing can use this skill to collect current headlines from selected RSS feeds and return them as readable Markdown links. The skill is especially oriented toward Chinese-language briefings while preserving source URLs for follow-up reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public news and release feeds.

Mitigation: Run it only where outbound feed access is acceptable and review or restrict feed URLs according to local policy.

Risk: The briefing includes clickable links to external article content.

Mitigation: Treat links as external content and verify destinations before opening, sharing, or relying on them.

Risk: Output is Chinese-language by default.

Mitigation: Review the generated brief for the intended audience or adjust the skill instructions when another language is required.

## Reference(s):

- [Morning Brief on ClawHub](https://clawhub.ai/amadeus9169/skills/morning-brief-v1)
- [BBC World RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Solidot RSS feed](https://www.solidot.org/index.rss)
- [Polygon RSS feed](https://www.polygon.com/rss/index.xml)
- [ScienceDaily science RSS feed](https://www.sciencedaily.com/rss/top/science.xml)
- [OpenClaw releases feed](https://github.com/joargp/openclaw/releases.atom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefing with section headers and clickable headline links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs Chinese-language briefing text by default and preserves original article URLs as Markdown links.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
