## Description: <br>
Personal health assistant with drug regulations, mental health support, and pet health guidance. Use for health tracking, medication reminders, symptom analysis, exercise/diet advice, travel health prep, first aid, international drug regulations, mental health counseling, and pet care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welliu](https://clawhub.ai/user/welliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for general health tracking, medication reminders, symptom triage, wellness guidance, travel health preparation, mental health support, and pet care guidance. It is informational and should be checked against qualified professional advice for medical, veterinary, mental-health, emergency, or regulatory decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health profile data, medication records, reminders, and health records may be stored locally in plaintext under ~/.health_data. <br>
Mitigation: Use only on trusted devices, avoid storing unnecessary sensitive details, and review or delete local files when they are no longer needed. <br>
Risk: Medical, mental-health, veterinary, first-aid, and drug-regulation responses may be incomplete, outdated, or unsuitable for urgent situations. <br>
Mitigation: Treat responses as general information and verify urgent or high-stakes decisions with emergency services, qualified professionals, or official regulatory sources. <br>


## Reference(s): <br>
- [Health Assistant ClawHub page](https://clawhub.ai/welliu/health-assistant) <br>
- [Common Health Conditions Reference](references/common_conditions.md) <br>
- [First Aid Reference](references/first_aid.md) <br>
- [Travel Health Reference](references/travel_health.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, code] <br>
**Output Format:** [Markdown and structured text with optional local JSON health records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local plaintext JSON files under ~/.health_data for profiles, medications, reminders, goals, and health records.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
