## Description:

Looks up province-level gasoline and diesel prices in China through a public oil-price API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangjian18](https://clawhub.ai/user/tangjian18)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents can look up reported provincial fuel prices, update dates and next adjustment times. City-specific prices are not provided.

### Deployment Geography for Use:

Global (price data covers China only)

## Known Risks and Mitigations:

Risk: The requested province name is sent to a third-party API over HTTPS.

Mitigation: Avoid including sensitive information in province inputs and review external API use before installation.

Risk: Third-party fuel prices may be delayed or inaccurate, and the bundled script does not produce the nationwide overview described in the documentation.

Mitigation: Check the reported update date and verify consequential price decisions against an authoritative source; query individual provinces with the bundled script.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tangjian18/skills/oil-price-query)
- [Oil-price data API](https://v1.apizero.cn/api/oil-price)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Chinese-language plain text with price listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports provincial prices in yuan per liter when the API provides them; the bundled script requires a province argument.]

## Skill Version(s):

1.3.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
