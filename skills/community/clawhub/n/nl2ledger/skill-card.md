## Description: <br>
Natural language bookkeeping that parses Chinese or English expense, income, and transfer descriptions and appends confirmed entries to a QianJi CSV ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn natural-language bookkeeping notes into reviewed QianJi ledger entries. The skill previews parsed fields for confirmation before appending rows to a local CSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit local QianJi CSV ledger data after user confirmation. <br>
Mitigation: Review the target file, amount, category, timestamp, account, currency, recorder, and note before confirming, and keep backups of important ledger files. <br>
Risk: Natural-language parsing can misclassify ambiguous expenses or choose an unintended category. <br>
Mitigation: Use the preview and modification flow to correct ambiguous entries before the append script writes to the CSV. <br>


## Reference(s): <br>
- [Category Keyword Mapping](references/category_map.md) <br>
- [QianJi CSV Schema](references/csv_schema.md) <br>
- [ClawHub release page](https://clawhub.ai/deusyu/nl2ledger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown preview text plus shell commands that append CSV rows after confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local QianJi CSV ledger entries through the bundled append script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
