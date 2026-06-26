## Description: <br>
Calculates itemized compensation estimates for Chinese personal-injury, traffic-accident, disability, and death claims by running the bundled local calculator and using the included legal and statistical references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal practitioners and agents use this skill to collect case facts, execute a local calculation script, and produce structured compensation breakdowns for China personal-injury matters. It supports injury and death scenarios, including disability compensation, funeral expenses, lost income, nursing, nutrition, hospital meal subsidies, and dependent living expenses. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Case facts and exported results may contain confidential legal, medical, or identity information. <br>
Mitigation: Use the skill only in environments appropriate for sensitive case details, and save Markdown, JSON, or XLSX exports only in approved confidential-record locations. <br>
Risk: Compensation estimates depend on current, jurisdiction-specific statistics and externally researched override values when local data is missing. <br>
Mitigation: Verify any researched statistics against authoritative statistical or human-resources sources before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/personal-injury-compensation-calculation) <br>
- [Calculation formulas](references/formulas.md) <br>
- [Core legal articles](references/law_articles.md) <br>
- [Disposable income data](references/disposable_income.md) <br>
- [Provincial average wage data](references/provincial_avg_wage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, files] <br>
**Output Format:** [Markdown or JSON compensation breakdowns, optional XLSX files, and shell commands for running the local calculator.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires case-fact JSON input; may require externally verified statistics_overrides when local statistical data is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
