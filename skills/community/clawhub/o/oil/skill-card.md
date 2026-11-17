## Description:

Queries gasoline and diesel reference prices for Chinese provinces and municipalities, and can list supported locations through JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer oil-price questions for Chinese provinces or municipalities, list supported locations, and summarize returned gasoline or diesel prices with update times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends JISU_API_KEY and oil-price query parameters to api.jisuapi.com.

Mitigation: Use only with a JisuAPI account and an API key intended for this service; rotate or revoke the key if exposure is suspected.

Risk: Oil-price data depends on the JisuAPI service response and may be unavailable, outdated, quota-limited, or rejected for invalid province inputs.

Mitigation: Check returned error codes and update times before presenting results as current.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/oil)
- [JisuAPI website](https://www.jisuapi.com/)
- [JisuAPI Today's Oil Price API documentation](https://www.jisuapi.com/api/oil/)
- [JisuAPI oil API endpoint](https://api.jisuapi.com/oil)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; query output is JSON returned from the JisuAPI oil endpoints.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
