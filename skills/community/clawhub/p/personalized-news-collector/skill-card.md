## Description: <br>
Get current news which matches user's recent interests. It can be triggered when user ask about current news or the events happening around without selecting a specific topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron90](https://clawhub.ai/user/zeron90) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to infer at least three recent interests from conversation or memory, collect current news from relevant sources, and receive a categorized Markdown report sorted by apparent popularity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may infer user interests from recent conversation or memory before collecting news. <br>
Mitigation: Ask the agent to confirm inferred interests first, or provide an explicit topic list. <br>
Risk: The skill contacts third-party news sources and feeds, which may vary in availability, freshness, and reliability. <br>
Mitigation: Specify preferred sources or require source citations and freshness checks in the final report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zeron90/personalized-news-collector) <br>
- [Publisher profile](https://clawhub.ai/user/zeron90) <br>
- [Bundled news source list](artifact/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with categorized news items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks news by frequency across sources, with judgment used as a tie-breaker.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
