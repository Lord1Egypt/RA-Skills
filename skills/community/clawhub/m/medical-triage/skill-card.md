## Description:

Classify medical messages (emails, iMessages) as critical, urgent, or routine based on medical urgency indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binubmuse](https://clawhub.ai/user/binubmuse)

### License/Terms of Use:

MIT

## Use Case:

Developers and clinical operations teams can use this skill as human-reviewed decision support to classify incoming patient messages by apparent urgency. It helps prioritize review queues, but should not autonomously route, delay, close, or decide care for patient messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill classifies medical messages in a high-stakes workflow without documented clinical guardrails.

Mitigation: Use it only as human-reviewed decision support and require clinician or trained staff review before any triage, routing, closure, delay, or care decision.

Risk: Critical messages could be under-prioritized if the classification is wrong or incomplete.

Mitigation: Add explicit emergency-care escalation rules, conservative fallback handling, and monitoring for missed critical symptoms before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON array of triage result objects containing message id, category, reason, and confidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Categories are critical, urgent, or routine; outputs require human review before use in medical workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
