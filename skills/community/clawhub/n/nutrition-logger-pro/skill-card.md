## Description:

Logs Chinese-language diet entries, calculates or estimates nutrition from user-provided values and labels, and supports daily or weekly summaries, undo, and correction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to record meals in Chinese, distinguish user-provided, label-calculated, and estimated nutrition data, and maintain local nutrition logs with summaries and corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may treat vague messages as requests to append, undo, or update nutrition records.

Mitigation: Require user confirmation before append, undo, or update actions when intent or target record is ambiguous.

Risk: User-controlled text is written to CSV logs, which can be unsafe if opened from untrusted inputs in spreadsheet software before CSV formula neutralization is added.

Mitigation: Use a dedicated nutrition-log directory and avoid opening exported CSV files in spreadsheet software unless inputs are trusted or CSV formula neutralization is added.

Risk: Nutrition estimates and lightweight diet tips can be mistaken for precise or medical guidance.

Mitigation: Clearly label estimated values and confidence, preserve user-provided data priority, and keep guidance non-diagnostic with escalation to a clinician for medical needs.

## Reference(s):

- [Nutrition label parsing rules](references/label_parsing_rules.md)
- [Common Chinese food portion assumptions](references/common_food_portions.zh.md)
- [Common Chinese food nutrition reference](references/common_food_nutrition.zh.csv)
- [Response templates](references/response_templates.md)
- [Non-medical healthy eating guidance](references/healthy_eating_guidelines.md)
- [WHO healthy diet topic page](https://www.who.int/health-topics/healthy-diet)
- [WHO healthy diet fact sheet](https://www.who.int/en/news-room/fact-sheets/detail/healthy-diet)
- [CDC healthy eating tips](https://www.cdc.gov/nutrition/features/healthy-eating-tips.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese natural-language responses with JSON-producing CLI calls and local JSONL/CSV nutrition logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists food_log.jsonl and food_log.csv under a local nutrition-log directory; nutrition values are labeled by source and confidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
