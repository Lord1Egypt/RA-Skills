## Description: <br>
Personal Health Journal helps an agent record daily symptoms and vital signs, generate structured daily health summaries, identify trend changes, and provide risk-tiered care reminders without replacing clinical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangforsix](https://clawhub.ai/user/yangforsix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and care-support agents use this skill to keep dated symptom, vital-sign, medication, and care-history notes, then summarize recent trends and red-flag symptoms for safer follow-up. It is intended for tracking and triage support, not diagnosis or emergency care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive symptom, vital-sign, medication, and care-history notes in a local folder. <br>
Mitigation: Keep the folder private, avoid adding direct identifiers or account details, and review records before sharing them. <br>
Risk: Health guidance could be mistaken for clinical diagnosis or emergency medical advice. <br>
Mitigation: Use the output for tracking and triage support only, and seek timely in-person medical care when urgent or worsening symptoms appear. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangforsix/personal-health-journal) <br>
- [Symptom record template](references/symptom-template.md) <br>
- [Daily health summary template](references/daily-summary-template.md) <br>
- [Risk tiers and care reminders](references/risk-flags.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown health records, daily summaries, and concise chat summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores sensitive health notes locally and should avoid identifiers such as ID numbers, account details, real names, hospital numbers, and inspection barcodes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
