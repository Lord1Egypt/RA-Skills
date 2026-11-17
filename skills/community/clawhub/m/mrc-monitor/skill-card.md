## Description:

Monitors MRC canteen order tokens in Firebase Firestore and notifies supported chat channels when tracked orders are ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wysh3](https://clawhub.ai/user/wysh3)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to monitor one or more MRC canteen order tokens and receive channel notifications when orders are ready for pickup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a listed Firebase project and may read more order data than the requested token status.

Mitigation: Install only where this Firebase access is acceptable, and prefer a revised version that queries only requested tokens.

Risk: The skill leaves local logs containing channel identifiers and order tokens.

Mitigation: Redact, rotate, expire, or disable logs before use in environments where these identifiers are sensitive.

Risk: Broad command triggers can start background polling for unintended token numbers.

Mitigation: Confirm extracted tokens before launching monitoring and use a clear stop path for background processes.

Risk: The source includes an embedded Firebase API key.

Mitigation: Move the key to a managed secret or environment configuration and rotate it if exposure is a concern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wysh3/skills/mrc-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a background polling process and may send channel notifications through the local OpenClaw CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
