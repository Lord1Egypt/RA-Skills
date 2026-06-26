## Description: <br>
Minor Detection estimates whether speakers in chat sessions may be minors or students and returns structured evidence, risk, trend, and next-step fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohanzhang2005](https://clawhub.ai/user/xiaohanzhang2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to run a fixed minor-detection pipeline over single-session or multi-session chat payloads. It supports age tendency, school/student indicators, evidence review, uncertainty notes, risk level, and recommended next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends chats, identifiers, profile context, and user-derived text to configured remote classifier services. <br>
Mitigation: Use only trusted classifier endpoints, send only data you are allowed to process off-device, and prefer dedicated low-privilege API keys. <br>
Risk: Sensitive conversation and profile details may appear in local stderr observability logs. <br>
Mitigation: Review log handling before deployment and avoid retaining or sharing logs that contain sensitive user data. <br>
Risk: Remote embedding calls may be enabled if embedding endpoints and keys are configured. <br>
Mitigation: Leave embedding credentials unset unless retrieval is required, and configure only trusted embedding services when enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohanzhang2005/minor-detection) <br>
- [Output Schema](artifact/references/output-schema.md) <br>
- [Evidence Rules](artifact/references/evidence-rules.md) <br>
- [ICBO Guidelines](artifact/references/icbo-guidelines.md) <br>
- [Classifier System Prompt](artifact/references/classifier-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Single JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON includes decision, user_profile, icbo_features, evidence, reasoning_summary, trend, uncertainty_notes, and recommended_next_step fields.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
