## Description: <br>
Parse personal finance CSV exports, validate schema, categorize transactions via local rules, and summarize/report income, expenses, merchants, and categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and individuals use this skill to process local bank or credit-card CSV exports, validate schema compatibility, categorize transactions with local rules, and generate spending summaries without uploading financial data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance CSV exports may contain sensitive transaction and account data. <br>
Mitigation: Keep real exports local, share only reviewed outputs, and rely on the skill's account-number masking for CLI display. <br>
Risk: Keyword-based categorization can assign an incorrect category when merchant descriptions do not match the local rules well. <br>
Mitigation: Review categorized output before using it for decisions and update config/category-rules.json for the user's merchant vocabulary. <br>
Risk: Sample account-number-style values could be reused in public examples. <br>
Mitigation: Use clearly synthetic values in public demos and avoid copying sample account-number patterns into shared material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-personal-finance) <br>
- [Publisher profile](https://clawhub.ai/user/ppopen) <br>
- [README](README.md) <br>
- [Category rules](config/category-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CSV-oriented text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally from user-supplied CSV files; account numbers are masked in CLI output, and categorized CSV files are written only when an explicit output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
