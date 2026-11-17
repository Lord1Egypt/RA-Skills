## Description:

Deterministic rule-based system for classifying clarified input into a single primary task category and assigning execution complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omprasad122007-rgb](https://clawhub.ai/user/omprasad122007-rgb)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill after clarification to classify user requests, assess complexity and risk, assign confidence, and route the request to decomposition, clarification, or human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classification audit logs may capture sensitive user intent or operational metadata.

Mitigation: Before deployment, confirm log retention, access controls, audit-log encryption, and privacy policy alignment for the surrounding platform.

Risk: Low-confidence or high-risk classifications can route work incorrectly if used without review.

Mitigation: Use the documented clarification and human-review paths for low-confidence, high-risk, or critical-risk classifications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omprasad122007-rgb/skills/input-classification-v1)
- [Classification Models](references/classification-models.md)
- [System Integration](references/system-integration.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown guidance with structured JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single primary category, up to three secondary tags, complexity level, risk level, confidence score, and routing state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
