## Description:

Doctor-grade clinical assistant for evidence lookup, case discussion, and deliverable generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erinyu](https://clawhub.ai/user/erinyu)

### License/Terms of Use:


## Use Case:

Clinicians, medical educators, and medical researchers use this skill to route clinical, teaching, and research requests into structured outputs with evidence anchors, action plans, and safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical task data could be exposed if the API is deployed without authentication or network controls.

Mitigation: Set a strong OPENCLAW_DOCTOR_API_TOKEN before exposure and bind the service to loopback or place it behind authenticated TLS.

Risk: Clinical task content may be stored in plaintext SQLite when real patient data is submitted.

Mitigation: Avoid patient identifiers unless authorized and add encryption, retention, and deletion controls before clinical-data use.

Risk: Outbound callbacks and delivery channels could send task results to unapproved destinations.

Mitigation: Keep outbound sending disabled unless destinations are approved, and add callback allowlisting before enabling real sends.

Risk: Clinical outputs can affect care decisions if treated as autonomous medical advice.

Mitigation: Use only in clinician-supervised workflows and verify patient-specific contraindications and local protocol before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erinyu/skills/openclaw-for-doctor)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured Markdown with summaries, analysis, action plans, evidence anchors, and guardrails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role-stage selection, reasoning-mode selection, citations, task status, and delivery receipts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
