## Description: <br>
Generate a personalized global news briefing by asking about your interests, then searching the web and delivering a structured, readable digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christinazhang139](https://clawhub.ai/user/christinazhang139) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, writers, analysts, and curious readers use this skill to create personalized global news briefings across selected topics, regions, languages, and depth levels. It helps compare coverage from official media and public social-media sentiment while keeping source links visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved preferences may reveal sensitive news interests on shared machines. <br>
Mitigation: Use preference saving only when appropriate and remove ~/.claw/data/global-perspectives-news-prefs.json when prior interests should no longer be reused. <br>
Risk: Live news and social-media results can include stale, incomplete, or sentiment-only information. <br>
Mitigation: Review source links, prefer recent primary or recognized sources, and treat social-media sections as public sentiment rather than verified fact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/christinazhang139/global-perspectives-news-openclaw) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Tavily MCP](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefing with grouped story summaries, source links, a takeaway, and optional social sentiment notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Tavily MCP for live web search when connected and may offer opt-in local preference storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
