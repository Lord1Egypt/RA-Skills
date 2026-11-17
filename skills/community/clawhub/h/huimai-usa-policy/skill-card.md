## Description:

Provides bilingual querying and analysis of U.S. market policies, regulations, and investment-environment information using configurable data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business analysts, and developers use this skill to ask an agent for U.S. policy, regulatory, trade, tax, labor, environmental, and investment-environment information in Chinese or English. It supports structured policy lookup and preliminary market-analysis workflows where configured data sources are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys or sensitive data source values can appear in returned policy records, logs, or cache entries.

Mitigation: Use environment variables and non-secret data-source identifiers where possible, and review or modify the implementation before configuring real API keys.

Risk: Policy and investment-environment outputs may be incomplete or misleading if data sources remain placeholders or are not reviewed.

Mitigation: Connect vetted data sources and require human review before relying on results for business, legal, or investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-usa-policy)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Huimai documentation](https://docs.huimai.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance and structured JavaScript or JSON-like policy and analysis objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English output; result quality depends on configured data sources.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
