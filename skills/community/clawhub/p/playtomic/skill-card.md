## Description:

This skill helps agents guide users through searching, booking, listing, canceling, installing, and authenticating for Playtomic padel court workflows with the `padel-tui` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipp-eisen](https://clawhub.ai/user/philipp-eisen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to operate the `padel-tui` terminal workflow for Playtomic court search, booking, active match listing, cancellation, setup, and interactive login guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party CLI from an unverified source can introduce supply-chain risk.

Mitigation: Confirm the `padel-tui` source before installation and prefer a pinned release with checksum or signature verification.

Risk: Booking or cancellation commands can change a user's real Playtomic reservations.

Mitigation: Run booking and cancellation commands only after explicit user intent and review the court, time, and match details before approval.

Risk: Playtomic credentials or session material may be exposed if handled by the agent.

Mitigation: Use interactive login only, do not ask for credentials, and do not pass credentials inline.

## Reference(s):

- [Installation Reference](references/INSTALLATION.md)
- [ClawHub Skill Page](https://clawhub.ai/philipp-eisen/skills/playtomic)
- [Publisher Profile](https://clawhub.ai/user/philipp-eisen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and booking workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires interactive user confirmation before installation, booking, cancellation, or login-sensitive actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
