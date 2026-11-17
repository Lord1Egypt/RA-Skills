## Description:

Helps travelers and travel advisors plan routes, refine itineraries, organize travel memories, and create shareable JourniOne Travel Journal previews when generation is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaduzhu-ai](https://clawhub.ai/user/kaduzhu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel advisors use this skill to turn destination ideas, fixed bookings, documents, photos, or existing plans into practical day-by-day travel guidance and a shareable JourniOne Travel Journal preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed itinerary details, approved images, or extracted document text may be sent to JourniOne to create a public read-only preview link.

Mitigation: Confirm user intent before generation and exclude passports, precise home addresses, health information, private photos, and other sensitive material unless the user has intentionally removed it.

Risk: Hotel, flight, booking, payment, cancellation, and account-editing actions can affect real travel plans or accounts.

Mitigation: Treat those actions as separate decisions and require explicit confirmation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaduzhu-ai/skills/journione)
- [Onboarding contract](references/onboarding-contract.md)
- [Intake contract](references/intake-contract.md)
- [Itinerary presentation](references/itinerary-presentation.md)
- [Research and agent routing](references/research-and-agent-routing.md)
- [Roadbook card rendering](references/roadbook-card-rendering.md)
- [Workbuddy runtime](references/workbuddy-runtime.md)
- [JourniOne roadbook API](https://journione.ai/api/skill-roadbook)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API requests, configuration]

**Output Format:** [Markdown travel-planning guidance with optional structured API payloads and preview URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public read-only preview links after user confirmation and successful JourniOne generation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1-workbuddy.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
