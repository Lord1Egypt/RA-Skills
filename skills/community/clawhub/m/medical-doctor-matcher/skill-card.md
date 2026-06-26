## Description: <br>
根据用户主诉、病史、地区和就诊偏好推荐合适的医院与医生，并在可行时生成模拟挂号与陪诊安排。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and healthcare support agents use this skill to triage non-emergency symptoms into likely departments, compare hospital and doctor options, and produce structured appointment guidance. It can generate simulated registration and escort arrangements when the user asks for those services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medical and location information. <br>
Mitigation: Collect and share only the minimum details needed for routing and recommendations. <br>
Risk: Doctor and hospital recommendations may be mistaken for diagnosis or treatment advice. <br>
Mitigation: Present results as care navigation guidance and direct urgent symptoms to emergency services. <br>
Risk: Generated registration or escort order numbers may be mistaken for real bookings. <br>
Mitigation: Label booking and escort outputs as mock results unless a real booking service is separately connected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunlinlin-aragon/medical-doctor-matcher) <br>
- [Workflow](references/workflow.md) <br>
- [Symptom to Specialty](references/symptom_to_specialty.md) <br>
- [Output Template](references/output_template.md) <br>
- [Request Schema](schemas/request_schema.json) <br>
- [Response Schema](schemas/response_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured Markdown or JSON with risk level, recommended specialties, Top 3 hospital and doctor matches, and optional simulated booking details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mock hospital, doctor, slot, and escort data unless connected to real services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
