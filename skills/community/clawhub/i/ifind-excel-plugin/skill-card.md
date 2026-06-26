## Description: <br>
Reference guidance for using iFinD/同花顺 Excel plugin functions, indicator codes, parameter codes, and examples across stocks, Hong Kong equities, U.S. equities, bonds, funds, futures, and related financial instruments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to generate or review Excel formulas and workbook structures that reference iFinD market and financial data indicators. It is most useful when creating spreadsheet outputs that need correct thsiFinD function names, security-code formats, reporting dates, and parameter codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workbooks may contain iFinD formulas that query market data through a logged-in terminal or entitlement-bearing environment. <br>
Mitigation: Review formulas and workbook contents before opening, sharing, or running them where iFinD credentials or market-data entitlements are available. <br>
Risk: Incorrect dates, security codes, parameter codes, or unit conversions can produce misleading spreadsheet results. <br>
Mitigation: Validate generated formulas against the relevant indicator catalog and review financial outputs before using them for decisions or distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/laigen/ifind-excel-plugin) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Complete indicator catalog](artifact/ref/codes_all.json) <br>
- [Stock indicator catalog](artifact/ref/codes_stock.json) <br>
- [Bond indicator catalog](artifact/ref/codes_bond.json) <br>
- [Hong Kong equity indicator catalog](artifact/ref/codes_hk.json) <br>
- [U.S. equity indicator catalog](artifact/ref/codes_us.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Excel formulas, JSON indicator references, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces formula and reference guidance; workbook creation depends on the calling agent and the user's Excel/iFinD environment.] <br>

## Skill Version(s): <br>
10.1.0 (source: server release metadata; artifact frontmatter: 10.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
