## Description: <br>
German-language news skill for OpenClaw and AI agent users that retrieves ClawNews.de briefings, breaking alerts, and archive search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClawNewsde](https://clawhub.ai/user/ClawNewsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users in the DACH region use this skill to receive German-language ClawNews.de briefings, search the ClawNews.de archive, and surface breaking alerts about OpenClaw, ClawHub, LLMs, AI agents, security, tools, open source, and community topics. <br>

### Deployment Geography for Use: <br>
DACH region <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and feed requests are sent to ClawNews.de. <br>
Mitigation: Use the skill only where sending those topic searches and news requests to ClawNews.de is acceptable. <br>
Risk: Breaking alerts are intended to remain enabled and may be checked proactively when the host agent supports scheduling. <br>
Mitigation: Review the setup mode and the host agent's scheduler or heartbeat behavior before enabling proactive use. <br>
Risk: User preferences may persist across sessions when the host agent supports memory. <br>
Mitigation: Store only the needed news mode and category preferences, and clear or update them when user preferences change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClawNewsde/newsticker) <br>
- [Skill formatting templates](artifact/references/templates.md) <br>
- [ClawNews.de](https://clawnews.de) <br>
- [ClawNews RSS feed](https://clawnews.de/feed/) <br>
- [ClawNews breaking feed](https://clawnews.de/category/breaking/feed/) <br>
- [ClawNews WordPress posts API](https://clawnews.de/wp-json/wp/v2/posts) <br>
- [ClawNews WordPress categories API](https://clawnews.de/wp-json/wp/v2/categories) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [German-language Markdown briefings, search results, alerts, setup prompts, and settings summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawNews.de feeds and WordPress API responses; persistent preferences and proactive checks depend on the host agent's memory and scheduling support.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
