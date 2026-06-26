## Description: <br>
Unified web search skill with fallback from Brave web_search to DuckDuckGo to Claude.ai, with automatic search-result caching in memory/research/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to retrieve current web information through Brave, DuckDuckGo, or Claude.ai fallback paths and to preserve search notes for later research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and results may be sent to Brave, DuckDuckGo, or Claude.ai. <br>
Mitigation: Avoid sensitive queries unless using a trusted provider, and force a specific method when provider choice matters. <br>
Risk: Search records may be saved locally under memory/research/. <br>
Mitigation: Periodically review or delete cached research files, especially after sensitive or regulated work. <br>
Risk: The Claude.ai browser fallback requires a logged-in browser session and may be slow or hit account limits. <br>
Mitigation: Prefer Brave or DuckDuckGo for routine searches and use the browser fallback only when analysis-oriented search is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-web-claude) <br>
- [Publisher profile](https://clawhub.ai/user/mupengi-bot) <br>
- [Claude.ai new chat](https://claude.ai/new) <br>
- [Mupeng GitHub profile](https://github.com/mupeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save search query, timestamp, method, links, summaries, and insights to memory/research/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
