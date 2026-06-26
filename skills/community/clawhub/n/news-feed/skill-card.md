## Description: <br>
Fetch latest news headlines from major RSS feeds (BBC, Reuters, AP, Al Jazeera, NPR, The Guardian, DW) without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lknik](https://clawhub.ai/user/lknik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users can fetch current headlines, daily news briefings, and topic-specific news summaries from configured public RSS feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes unrelated local permission settings that could let an agent stage and commit repository changes. <br>
Mitigation: Review or remove .claude/settings.local.json before installing, and grant only the permissions needed to fetch public RSS feeds. <br>
Risk: News results come from public RSS feeds and may be incomplete, unavailable, delayed, or source-dependent. <br>
Mitigation: Verify important or time-sensitive news against the linked publisher pages before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lknik/news-feed) <br>
- [BBC News RSS](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [Reuters Top News RSS](https://www.rss.reuters.com/news/topNews) <br>
- [The Guardian RSS](https://www.theguardian.com/international/rss) <br>
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml) <br>
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml) <br>
- [DW Top Stories RSS](https://rss.dw.com/rss/en/top) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown headlines grouped by source, with optional JSON output from the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes headline title, short description, publication time, and source link when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
