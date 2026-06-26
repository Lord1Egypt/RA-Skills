## Description: <br>
Fetch and display Hacker News stories about AI, agents, and Claude. Default is past week. Use when the user asks for HN news, Hacker News AI stories, latest AI news or "what's AI trending on Hacker News". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operators use this skill to fetch recent Hacker News stories about AI, agents, and Claude and reformat them into a concise digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the public HN Algolia API. <br>
Mitigation: Before installing or running it, confirm that outbound access to hn.algolia.com is allowed in the target environment and that Python with requests is available. <br>


## Reference(s): <br>
- [HN Algolia search_by_date API](https://hn.algolia.com/api/v1/search_by_date) <br>
- [ClawHub skill page](https://clawhub.ai/goog/hn-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown digest with story titles, authors, points, timestamps, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to the past week unless the user asks for latest results; shows the top 20 when many results are returned.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
