## Description:

Provides a Chinese-language reference for iFinD/同花顺 Excel plugin formulas, parameter codes, and financial indicator definitions across stocks, Hong Kong stocks, U.S. stocks, bonds, funds, futures, and related markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to select iFinD Excel indicator codes and generate formulas or workbook-generation code for financial data retrieval. It is most relevant for workflows that already depend on iFinD/同花顺 Excel access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel formulas may query financial data through the user's logged-in iFinD environment.

Mitigation: Review formulas and target workbooks before opening, refreshing, or sharing them.

Risk: Some catalog entries may be malformed.

Mitigation: Validate selected indicator codes and parameters against the iFinD Excel plugin before relying on generated results.

Risk: The reference material is primarily Chinese-language financial data documentation.

Mitigation: Use it only in workflows where the user can interpret the Chinese indicator names, parameters, and market conventions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/ifind-excel-plugin)
- [iFinD Excel Plugin Skill Source](artifact/SKILL.md)
- [iFinD Indicator Code Catalogs](artifact/ref/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Excel formulas and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include thsiFinD Excel formulas, indicator-code selections, parameter guidance, and workbook-generation examples.]

## Skill Version(s):

10.1.0 (source: server release metadata; artifact frontmatter lists 10.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
