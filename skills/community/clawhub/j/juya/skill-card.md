## Description: <br>
Fetches Juya AI Daily newsletter entries from the public RSS feed and formats selected AI news items as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheerwhy](https://clawhub.ai/user/Cheerwhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for the latest or date-specific Juya AI Daily briefing and receive categorized newsletter content with titles and links in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched newsletter text and linked pages are external content and may be inaccurate or instruction-like. <br>
Mitigation: Treat fetched content as untrusted reference material and verify important AI news from primary sources before acting on it. <br>
Risk: The public RSS feed may not contain the requested date or may have changed since a prior run. <br>
Mitigation: Match entries by the feed title date and report when no matching item is available instead of fabricating content. <br>


## Reference(s): <br>
- [Juya AI Daily RSS feed](https://imjuya.github.io/juya-ai-daily/rss.xml) <br>
- [ClawHub skill page](https://clawhub.ai/Cheerwhy/juya) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown list grouped by category with titles and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to the latest feed item when no date is specified; supports date-specific lookup by YYYY-MM-DD title.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
