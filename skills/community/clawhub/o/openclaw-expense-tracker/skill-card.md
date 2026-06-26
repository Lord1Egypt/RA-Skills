## Description: <br>
智能记账本 helps agents record Chinese natural-language expense entries, classify spending, and summarize local expense history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GlorySunshine](https://clawhub.ai/user/GlorySunshine) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and agents use this skill to record daily spending from Chinese-language messages, classify expenses such as food, transport, shopping, entertainment, and medical costs, and request day, week, or month summaries from locally stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense history is saved locally in a JSON file and may contain sensitive personal finance information. <br>
Mitigation: Use the skill only where local file permissions are appropriate, and delete or protect data.json on shared machines. <br>
Risk: Broad trigger words such as record or add may create unintended expense entries. <br>
Mitigation: Use explicit phrasing such as "记账" with a clear amount and review recent entries when precision matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GlorySunshine/openclaw-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Chinese text responses with local JSON expense records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records are stored locally in data.json; no network access or external data collection is indicated by the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
