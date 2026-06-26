## Description: <br>
Fetches Hacker News front-page stories, ranks them using saved user interests and HN points, presents a concise briefing, and summarizes selected stories on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken7y](https://clawhub.ai/user/ken7y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hacker News readers use this skill to get a personalized morning briefing of top HN stories and quickly drill into a chosen article with a short summary and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live Hacker News RSS data and opens article URLs, so external content can change, fail to load, or contain misleading information. <br>
Mitigation: Treat briefings and article summaries as current web content, and confirm important claims against the linked article or HN discussion. <br>
Risk: Personalized ranking uses saved interests, which may over-prioritize stale or incorrect preferences. <br>
Mitigation: Ask the agent to ignore saved interests or rank by HN points only when the briefing feels irrelevant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ken7y/hn-morning-brief) <br>
- [Hacker News RSS front page](https://hnrss.org/frontpage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown briefing and summaries, with JSON story data fetched by the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes article URLs, HN discussion URLs, domains, authors, points, and comment counts when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
