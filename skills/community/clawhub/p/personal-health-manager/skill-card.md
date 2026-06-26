## Description: <br>
Personal health management and wellness assistant for tracking health data, managing medications, analyzing symptoms, receiving exercise and diet guidance, and preparing travel health essentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welliu](https://clawhub.ai/user/welliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize personal health information, medication schedules, wellness routines, symptom screening, first aid references, and travel health preparation. It is informational and should not be used as a substitute for professional medical advice or emergency care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health information may be stored as plaintext JSON files under ~/.health_data. <br>
Mitigation: Share only the minimum necessary health details, protect the local device and account, review stored files, and delete them when no longer needed. <br>
Risk: Health, medication, symptom, and first aid guidance may be incomplete, incorrect, or not appropriate for a specific person or location. <br>
Mitigation: Treat outputs as informational, verify medication and reminder behavior independently, consult qualified healthcare professionals, and use local emergency services for urgent symptoms. <br>


## Reference(s): <br>
- [Common Health Conditions Reference](references/common_conditions.md) <br>
- [Emergency First Aid Reference](references/first_aid.md) <br>
- [Travel Health Preparation Checklist](references/travel_health.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON examples, Python helper usage, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local plaintext JSON health records under ~/.health_data when helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
