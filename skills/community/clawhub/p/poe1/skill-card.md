## Description:

Path of Exile market price query tool using the poe.ninja API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qpooqp777](https://clawhub.ai/user/qpooqp777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Path of Exile tool users use this skill to query live poe.ninja currency and item prices, compare league market values, inspect price trends, and run bundled Python helpers for currency, item, and cross-type searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live market data can be stale, low-confidence, or inaccurate for important trades.

Mitigation: Verify prices before high-value trades and consider listing counts, trend fields, and low-confidence indicators when available.

Risk: Cross-type searches can make multiple poe.ninja requests in a short period.

Mitigation: Use reasonable rate limits, narrow searches when possible, and avoid repeated broad searches.

Risk: The bundled Python helpers contact poe.ninja over HTTPS when run.

Mitigation: Review commands before execution and run the scripts only in environments where outbound access to poe.ninja is acceptable.

## Reference(s):

- [Poe.ninja API reference](references/api_reference.md)
- [poe.ninja public API](https://poe.ninja/api/data)
- [poe.ninja API documentation](https://github.com/ayberkgezer/poe.ninja-API-Document)
- [ClawHub skill page](https://clawhub.ai/qpooqp777/skills/poe1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples; bundled scripts print terminal tables or JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live HTTPS requests to poe.ninja and does not require credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
