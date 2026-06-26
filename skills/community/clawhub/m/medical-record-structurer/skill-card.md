## Description: <br>
Medical Record Structurer converts oral, handwritten, or free-text clinical notes into standardized electronic medical record fields with optional payment, OCR, and speech-to-text integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andyxcg](https://clawhub.ai/user/Andyxcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operators, clinicians, and developers can use this skill to transform unstructured medical notes into structured EMR JSON for review, filing, or downstream clinical documentation workflows. Outputs should be verified by qualified healthcare professionals before use in care decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Under-disclosed self-modifying background code may change skill behavior after review. <br>
Mitigation: Review or remove auto-evolve-daemon.sh and scripts/self_evolve.py before installation, and re-scan any modified package before deployment. <br>
Risk: The skill handles sensitive medical records and may write PHI to output files or interact with billing, OCR, or speech-to-text services. <br>
Mitigation: Use real patient data only after verifying data flows, consent, retention, access controls, and applicable healthcare compliance requirements. <br>
Risk: Structured medical record output may be incomplete or inaccurate. <br>
Mitigation: Require review by qualified healthcare professionals before using outputs in clinical documentation or care decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Andyxcg/medical-record-structurer) <br>
- [EMR Schema Reference](references/emr-schema.md) <br>
- [Skillpay.me API Reference](references/skillpay-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Structured EMR JSON returned through Python functions or printed/saved by command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include patient demographics, clinical fields, treatment plan fields, metadata, trial or billing status, and optionally the original source text.] <br>

## Skill Version(s): <br>
1.4.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
