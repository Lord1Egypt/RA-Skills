## Description:

Plan and track cryptographic key rotations for API keys, encryption keys, signing keys, and service credentials. Inventory all keys, assess rotation urgency, generate rotation runbooks, and verify post-rotation health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and operations teams use this skill to inventory service credentials, rank rotation urgency, produce rotation runbooks, and verify post-rotation health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory commands may expose real secret values in command output, chat, reports, tickets, logs, or transcripts.

Mitigation: Scope scans to the intended repository, use redacted or metadata-only scanner output, avoid copying discovered secret values into shared systems, and rotate any exposed value as compromised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/key-rotation-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inventory reports, prioritized schedules, rotation runbooks, and verification steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
