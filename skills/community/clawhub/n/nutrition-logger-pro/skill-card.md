## Description: <br>
Records meals, portions, calories, protein, carbohydrates, fat, and nutrition-label data in Chinese, with support for daily and weekly summaries, undo, correction, and nutrition estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to keep a local Chinese-language food and nutrition log, calculate label-based nutrition values, estimate missing nutrition data, and review daily or weekly intake summaries. It is for personal tracking and does not provide medical diagnosis or treatment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local meal history on disk, which can include sensitive personal health or lifestyle information. <br>
Mitigation: Configure the log directory deliberately, avoid shared or synced folders when privacy matters, and review the generated log files before sharing a workspace. <br>
Risk: Natural-language meal messages may be logged unintentionally or with incorrect nutrition estimates. <br>
Mitigation: Use explicit logging requests, review confidence and source labels, and use the undo or correction workflow when an entry is wrong. <br>
Risk: Nutrition estimates and lightweight eating suggestions may be incomplete or unsuitable for medical conditions. <br>
Mitigation: Treat outputs as personal tracking guidance only and consult a qualified clinician or registered nutrition professional for medical needs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seanmwx/nutrition-logger-pro) <br>
- [Nutrition label parsing rules](artifact/references/label_parsing_rules.md) <br>
- [Common food portion assumptions](artifact/references/common_food_portions.zh.md) <br>
- [Common food nutrition table](artifact/references/common_food_nutrition.zh.csv) <br>
- [Healthy eating guidelines](artifact/references/healthy_eating_guidelines.md) <br>
- [WHO healthy diet topic page](https://www.who.int/health-topics/healthy-diet) <br>
- [WHO healthy diet fact sheet](https://www.who.int/en/news-room/fact-sheets/detail/healthy-diet) <br>
- [CDC healthy eating tips](https://www.cdc.gov/nutrition/features/healthy-eating-tips.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Chinese Markdown responses plus JSON CLI input and output for deterministic local logging commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local food_log.jsonl and food_log.csv files when logging commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
