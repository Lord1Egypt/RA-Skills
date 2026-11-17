## Description:

Gold Analysis helps agents answer gold market questions with price lookups, technical indicators, news-based fundamental context, and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can invoke this skill when an agent needs a gold market analysis report covering current prices, technical signals, news-driven fundamentals, and risk considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gold-analysis queries are sent to Tavily for external search.

Mitigation: Use the skill only when this external data sharing is acceptable, and avoid sending sensitive user or portfolio details in search queries.

Risk: The artifact includes and automatically falls back to a shared Tavily API key.

Mitigation: Prefer a release that removes and rotates the shared key, and configure a user-controlled TAVILY_API_KEY before use.

Risk: Gold market signals may be interpreted as personal financial advice.

Mitigation: Treat outputs as informational market analysis and require appropriate human review for investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fmouseboy/skills/gold-skill)
- [Gold technical indicators reference](references/technical-indicators.md)
- [Tavily](https://tavily.com/)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis report with source links and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tavily search results and market-risk caveats.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
