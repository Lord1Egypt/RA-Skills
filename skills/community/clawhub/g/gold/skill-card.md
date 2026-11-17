## Description:

Queries JisuAPI-backed reference prices for Shanghai, Hong Kong, bank, London precious-metal, jewelry-store, and historical gold-market data, with returned change fields used only to describe observed movement and not as investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer gold-price questions by calling JisuAPI endpoints for exchange, bank, London, store, and historical market data. It is suited for reference-price lookup and concise movement summaries, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gold-price lookup parameters are sent to JisuAPI.

Mitigation: Deploy only where sharing those lookup parameters with JisuAPI is acceptable, and configure the API key through the documented environment variable.

Risk: Returned prices are reference market data and may be time-sensitive or unsuitable for investment decisions.

Mitigation: Present timestamps and source context when available, and avoid predictions or investment recommendations beyond the returned API fields.

Risk: The skill requires a JISU_API_KEY credential.

Mitigation: Store the key in an environment variable or managed secret and avoid exposing it in prompts, logs, or committed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/gold)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Gold Price API](https://www.jisuapi.com/api/gold/)
- [JisuAPI Gold API base endpoint](https://api.jisuapi.com/gold)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; the helper script returns API result JSON or structured error JSON.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
