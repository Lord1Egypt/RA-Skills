## Description: <br>
NoodleShopOwner helps agents compare public companies by normalizing market capitalization to a 100-unit purchase price, then translating valuation, book value, profit, and ROE into plain-language shop-owner commentary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[formyreason](https://clawhub.ai/user/formyreason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to compare public companies, inspect valuation ratios, and produce educational valuation commentary in an accessible business metaphor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on public company data that is incomplete, stale, or tied to a different reporting period. <br>
Mitigation: Verify financial figures, reporting periods, and source links before relying on the analysis. <br>
Risk: Valuation commentary may be mistaken for investment advice. <br>
Mitigation: Use the output as educational analysis only and make any investment decisions through independent review. <br>
Risk: Missing PE, PB, ROE, market cap, or profit fields can make final comparisons misleading. <br>
Mitigation: Stop at partial results and request missing fields instead of producing a final recommendation when key data is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/formyreason/noodles-shop-owner) <br>
- [Reference Manual](artifact/reference.md) <br>
- [Output Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables, formulas, plain-language commentary, and optional Python calculation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be treated as educational valuation commentary, not investment advice; financial figures, reporting periods, and sources should be verified before use.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
