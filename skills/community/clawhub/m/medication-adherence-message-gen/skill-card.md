## Description: <br>
Generates personalized SMS or push notification medication reminder copy using behavioral psychology principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External healthcare teams, researchers, and agent developers use this skill to draft medication reminder messages with selected behavioral principles. Generated copy should be reviewed in an approved healthcare, privacy, and compliance workflow before being sent to patients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is partly mislabeled as an academic-writing tool and lacks clear healthcare and privacy boundaries. <br>
Mitigation: Relabel it as healthcare-adjacent medication messaging, document privacy and consent expectations, and use it only within an approved healthcare or research workflow. <br>
Risk: Generated reminder copy may include unsupported adherence statistics or urgent and loss-framed claims. <br>
Mitigation: Source or remove unsupported claims and require human clinical and compliance review before sending messages. <br>
Risk: Real patient identifiers could be included in generated drafts. <br>
Mitigation: Avoid real patient identifiers unless appropriate privacy controls are in place. <br>


## Reference(s): <br>
- [Audit Reference](artifact/references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/medication-adherence-message-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text reminder message or JSON object with medication, patient, principle, tone, message, psychology insight, and alternative messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese or English output; medication is required, while patient name, dosage, time, principle, tone, and output format are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
