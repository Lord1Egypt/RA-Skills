## Description:

Hotel search, comparison, and booking with live room rates and real-time availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tourmind](https://clawhub.ai/user/tourmind)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to search hotels worldwide, compare live room rates and availability, review booking terms, and complete booking, payment, cancellation, or order lookup workflows through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order actions use a reusable user_key stored in a local plaintext file.

Mitigation: Treat the key like a password, keep it out of prompts, logs, screenshots, backups, and repositories, and restrict local file access where supported.

Risk: The package includes a remotely driven self-update workflow.

Mitigation: Verify TourMind support and update sources independently before applying an update, and do not proceed unless the agent asks for confirmation.

Risk: Booking, payment, and cancellation actions can affect real travel orders and charges.

Mitigation: Review the displayed room, price, fee, cancellation, and payment details before confirming any order operation.

## Reference(s):

- [Hotel Booking AI ToC API and Field Reference](references/parameter_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
- [TourMind Skills Product Page](https://tourmind.com/skills)
- [TourMind API Base URL](https://api.tourmind.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with structured hotel options, room-rate details, booking summaries, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localized read-only result links when returned by the TourMind API]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact metadata.version declares 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
