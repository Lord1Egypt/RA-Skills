## Description: <br>
Estimate property values using comparable sales, income approach, market context, and adjustment calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Home buyers, sellers, refinancers, investors, and their agents use this skill to prepare property value ranges, compare valuation methods, document adjustments, and explain confidence based on available market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Property details, valuation history, market notes, and preferences may be saved locally under ~/property-valuation/. <br>
Mitigation: Avoid storing SSNs, account credentials, loan documents, or other highly sensitive records, and delete the local memory file when prior context should be forgotten. <br>
Risk: Valuation estimates can be misleading when based on stale comps, missing property details, or unsupported market assumptions. <br>
Mitigation: Require key property facts, state the valuation method, document all adjustments, show confidence level, and ask the user to provide recent comparable sales or market data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/property-valuation) <br>
- [Skill Homepage](https://clawic.com/skills/property-valuation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown valuation guidance with tables, formulas, value ranges, confidence notes, and local memory updates when appropriate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not access real-time MLS data or connect to Zillow or Redfin APIs; users must provide current comparable sales or market inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
