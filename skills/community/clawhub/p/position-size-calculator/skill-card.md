## Description:

Calculates share count and position risk from a user's account size, risk limit, entry, stop, and optional target, with a self-contained HTML view prefilled from delayed market data.

This skill is for research and development only.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to calculate share count, position value, account allocation, stop risk, and an optional target R multiple from their own trade inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual insertion of market-data text into the template can expose the page to crafted content that executes as browser code.

Mitigation: Use the bundled --out command, which safely escapes API text; avoid the documented manual insertion method until it provides equivalent escaping.

Risk: Daily-range context may be less reliable when price history is sparse.

Mitigation: Treat the daily-range comparison cautiously when history is sparse.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thesentitrader/skills/position-size-calculator)
- [SentiSense](https://sentisense.ai)
- [SentiSense API key](https://app.sentisense.ai/get-api-key)

## Skill Output:

**Output Type(s):** [Files, HTML, Guidance]

**Output Format:** [Self-contained HTML file with setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The page renders offline and calculates from user-provided inputs; its bound market price is delayed.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
