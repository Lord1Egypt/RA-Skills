## Description:

Gold price query tool supporting CNY (RMB/gram) and USD (USD/oz) currency options for real-time spot gold price lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghaolie](https://clawhub.ai/user/yanghaolie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query current spot gold prices in either USD per ounce or CNY per gram and receive structured price, change, volume, and update-time data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts jijinhao.com for each query and sends normal request metadata, including browser-like headers.

Mitigation: Use only in environments where this outbound network request and metadata exposure are acceptable.

Risk: The artifact does not declare network permissions explicitly and does not show a request timeout.

Mitigation: Review network access before deployment and consider adding explicit permissions plus a request timeout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanghaolie/skills/gold-price-query)
- [jijinhao real-time quote API](https://api.jijinhao.com/quoteCenter/realTime.htm)
- [cngold quote source page](https://quote.cngold.org/)

## Skill Output:

**Output Type(s):** [text, shell commands, code]

**Output Format:** [JSON text returned by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports USD by default and CNY when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
