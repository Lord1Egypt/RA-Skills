## Description: <br>
Analyzes symptom descriptions, optional demographics, and vital signs to return preliminary triage levels, red-flag findings, differential considerations, and care recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andyxcg](https://clawhub.ai/user/Andyxcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare providers, telemedicine teams, and developers use this skill to support preliminary symptom triage and route users toward appropriate urgency levels. It is informational support and not a substitute for emergency care or professional diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive symptom information and may save assessments, timestamps, and user identifiers under ~/.openclaw despite privacy claims. <br>
Mitigation: Use --no-save-history or modify the code to disable local history, protect access to ~/.openclaw, and avoid entering unnecessary patient identifiers. <br>
Risk: The release includes an unrelated persistent auto-evolution daemon. <br>
Mitigation: Do not run auto-evolve-daemon.sh, and review any script that changes skill behavior before deployment. <br>
Risk: Medical triage output can be mistaken for diagnosis or emergency medical advice. <br>
Mitigation: Treat results as informational triage support only and require qualified clinical review for medical decisions or urgent symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Andyxcg/intelligent-triage-symptom-analysis) <br>
- [Triage systems reference](references/triage-systems.md) <br>
- [Disease database reference](references/disease-database.md) <br>
- [Clinical specifications](references/clinical-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON or console text containing triage level, red flags, differential considerations, recommendations, and disclaimer text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save symptom-history records locally unless history saving is disabled.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
