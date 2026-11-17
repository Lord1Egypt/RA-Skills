## Description:

Transforms rough email drafts into polished, professional medical correspondence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn rough medical, academic, or patient-facing email drafts into professional correspondence with a suggested subject, tone assessment, and change summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts may contain real patient or confidential medical content.

Mitigation: Use de-identified drafts and review all output before use in real medical or patient communication.

Risk: Draft text can be supplied through command-line arguments where it may be exposed through shell history or process listings.

Mitigation: Do not pass PHI or sensitive details as command-line arguments; use only sanitized examples or a safer input path if the skill is adapted.

Risk: The package claims HIPAA-aware communication, but the evidence does not prove compliance safeguards.

Mitigation: Treat HIPAA-aware output as editorial assistance only and require qualified human review for policy, privacy, and clinical appropriateness.

## Reference(s):

- [Medical Email Polisher ClawHub listing](https://clawhub.ai/aipoch-ai/skills/medical-email-polisher)
- [Medical Email Polisher References](references/guidelines.md)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON object containing polished_email, subject_line, changes_made, tone_assessment, and recipient_type.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inputs include a rough draft, recipient type, and optional context; avoid sensitive medical details or PHI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
