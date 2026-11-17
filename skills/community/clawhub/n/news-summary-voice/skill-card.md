## Description:

News Summary Voice helps agents collect RSS news sources, draft multilingual news briefings, and optionally prepare text-to-speech playback across macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realorange1994](https://clawhub.ai/user/realorange1994)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather current news from selected RSS feeds, summarize it into a briefing, and optionally produce or play a spoken version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some listed RSS feeds may be questionable, insecure, or misidentified.

Mitigation: Replace questionable or HTTP feeds with verified HTTPS first-party sources before installing or running the skill.

Risk: RSS feed content can include untrusted or sensitive news text that may be summarized or spoken aloud.

Mitigation: Treat feed content as untrusted text, require confirmation for broad news or voice requests, and review sensitive news before voice broadcast.

Risk: The optional audio flow downloads remote media to /tmp before playback.

Mitigation: Avoid that pattern unless it is hardened with trusted media URLs, safe temporary-file handling, and cleanup.

Risk: Linux setup examples include sudo package installation commands.

Mitigation: Run package installs only manually after reviewing the packages and installation source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realorange1994/skills/news-summary-voice)
- [BBC World RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Reuters World RSS](https://www.reutersagency.com/feed/?best-topics=world-news)
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml)
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml)
- [The Guardian World RSS](https://www.theguardian.com/world/rss)
- [Hacker News RSS](https://news.ycombinator.com/rss)
- [TechCrunch RSS](https://techcrunch.com/feed/)
- [Ars Technica RSS](https://feeds.arstechnica.com/arstechnica/index)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with optional shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RSS source links and optional text-to-speech or audio playback steps.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
