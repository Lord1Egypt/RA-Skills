## Description:

Provides AI-assisted stock research for single-asset, multi-asset, and industry comparison questions, producing markdown analyses across financials, valuation, technical indicators, capital flows, market sentiment, and deeper research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlujing](https://clawhub.ai/user/sunlujing)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and investment advisors use this skill to identify securities, request quick overviews, compare assets, and generate informational investment research reports with ratings, risks, and suggested follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends stock symbols, investment queries, and an API token to a configurable remote endpoint.

Mitigation: Install only if the user trusts the 财搭子/Facaidazi service, use a scoped and revocable token, and keep TOOL_API_URL at the HTTPS default unless the endpoint is fully controlled.

Risk: The skill can produce strong trading-style ratings, targets, stop-losses, and position suggestions.

Mitigation: Treat outputs as informational research rather than personal financial advice, and review recommendations against independent sources before acting.

Risk: Changing TOOL_API_URL can redirect requests and bearer tokens away from the default service.

Mitigation: Use custom endpoints only when the endpoint owner, transport security, and data handling are understood.

## Reference(s):

- [Tool Client Usage Guide](references/tool-client-usage.md)
- [Tool Interface Specification](references/tool-specs.md)
- [ClawHub skill page](https://clawhub.ai/sunlujing/skills/invest-buddy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include investment ratings, target ranges, stop-loss levels, position suggestions, timestamps, and risk factors based on external API responses.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
