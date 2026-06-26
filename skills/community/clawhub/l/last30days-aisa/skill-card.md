## Description: <br>
Researches the last 30 days across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and web search for recent social research, company updates, comparisons, launch reactions, and trend scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather a recent research brief on a person, company, product, market, tool, or trend. It is suited for competitor comparisons, launch-reaction summaries, creator or community sentiment scans, and recent shipping updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and retrieved public-content snippets may be sent to external AISA services. <br>
Mitigation: Use only with topics whose data handling is acceptable, and avoid sensitive or regulated topics unless the AISA service has been reviewed. <br>
Risk: Optional watchlist, local storage, briefing archives, and webhook delivery can persist research history or send outbound notifications. <br>
Mitigation: Enable those features only when persistent history and notifications are intended, and review local storage and webhook configuration before use. <br>
Risk: Evaluation tooling can execute checked-out code with the user's API-key environment. <br>
Mitigation: Run evaluation only against trusted revisions and isolate credentials when comparing or testing changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bibaofeng/last30days-aisa) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [Declared repository](https://github.com/AIsa-team/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown brief or structured JSON with query plans, ranked candidates, clusters, and items by source] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include saved local report files when the user selects a save mode.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
