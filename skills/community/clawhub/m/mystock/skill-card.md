## Description: <br>
MyStock is a stock analysis assistant for quotes, market analysis, limit-up tracking, shareholder activity, investment research, portfolio management, and AI-assisted stock questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangz](https://clawhub.ai/user/wangz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent users use this skill to query Chinese stock data, review watchlists and portfolio notes, inspect limit-up and shareholder activity signals, and draft AI-assisted market analysis. It supports local web UI workflows and API-backed responses for stock research, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local finance API is unauthenticated and may expose portfolio, watchlist, memo, stock-search, or chat data if reachable beyond the intended host. <br>
Mitigation: Bind the backend to localhost, add authentication before shared deployment, and review network exposure before use. <br>
Risk: Stock searches, chat messages, and portfolio or watchlist context may be shared with configured market-data or AI providers. <br>
Mitigation: Use the default non-AI mode or explicit opt-in for AI chat, and avoid sending sensitive portfolio context to external providers unless acceptable. <br>
Risk: The security review flags broader exposure of sensitive portfolio-related data than users are clearly told. <br>
Mitigation: Present clear user notice about data sharing and review the implementation before installation. <br>


## Reference(s): <br>
- [Mystock ClawHub page](https://clawhub.ai/wangz/mystock) <br>
- [Usage examples](references/usage_examples.md) <br>
- [AI service configuration](backend/AI_CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, local API examples, and stock-analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local portfolio, watchlist, memo, market-data, and configured AI-provider context.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
