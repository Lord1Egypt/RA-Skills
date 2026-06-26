## Description: <br>
Local-first health record management with strict privacy boundaries for organizing medications, symptoms, vital signs, medical history, emergency summaries, and doctor-visit notes without diagnosis or treatment advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to keep local personal health records organized, generate emergency health summaries, and prepare concise information for clinician visits. It is not intended for diagnosis, treatment decisions, or replacement of professional medical care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-rely on medication interaction checks or symptom warnings for medical decisions. <br>
Mitigation: Treat built-in checks as reminders only and verify medication questions, symptoms, and care decisions with a doctor, pharmacist, or emergency services as appropriate. <br>
Risk: Local health records and emergency cards may contain sensitive medical details. <br>
Mitigation: Keep the device and backups private, control local retention and deletion, and review emergency-card contents before placing them on a lock screen or in a wallet. <br>


## Reference(s): <br>
- [Medical on ClawHub](https://clawhub.ai/AGIstack/medical) <br>
- [AGIstack ClawHub Profile](https://clawhub.ai/user/AGIstack) <br>
- [Emergency Health Summary](references/emergency-card.md) <br>
- [Personal Medical History](references/medical-history.md) <br>
- [Medication Manager](references/medication-manager.md) <br>
- [Symptom Tracker & Appointment Preparation](references/symptom-tracker.md) <br>
- [Vital Signs & Chronic Condition Monitoring](references/vital-signs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Concise structured text, Markdown summaries, JSON records, and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores health records locally under ~/.openclaw/workspace/memory/health and can generate phone, wallet, or JSON emergency-card formats.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
