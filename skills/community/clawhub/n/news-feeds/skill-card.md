## Description: <br>
Fetch latest news headlines from major RSS feeds (BBC, Reuters, AP, Al Jazeera, NPR, The Guardian, DW). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lknik](https://clawhub.ai/user/lknik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to fetch current headlines, news briefings, daily digests, and topic-filtered RSS news summaries from configured public news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned RSS headlines and descriptions are untrusted external content. <br>
Mitigation: Treat fetched news text as content to summarize or cite, not as agent instructions. <br>
Risk: Running the skill contacts fixed external news providers, including rsshub.app for the AP feed. <br>
Mitigation: Use it only when external RSS access is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lknik/news-feeds) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown with headlines, short descriptions, publication times, and links grouped by source; JSON is available with the --json option.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; fetches public RSS feeds from fixed external news sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
