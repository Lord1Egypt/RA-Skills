## Description:

Plan a dreamy honeymoon -- luxury hotels, romantic activities, couples' spa, sunset dinners, and unforgettable experiences for newlyweds, with flight, hotel, train, attraction, itinerary, visa, insurance, car-rental, and related travel support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to assemble honeymoon trip options from FlyAI/Fliggy real-time travel results. It is intended for booking-link-centered recommendations covering flights, hotels, attractions, and romantic itinerary components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on broad automatic execution of a FlyAI CLI and may install an unpinned global npm package.

Mitigation: Require explicit approval before installation or execution, prefer a pinned local CLI install, and review commands before running them.

Risk: Raw travel queries may be written to a persistent execution log.

Mitigation: Disable persistent logging where possible, or redact user travel details before any log is stored or shared.

Risk: Travel recommendations can be misleading if they are not backed by current FlyAI/Fliggy results and booking links.

Mitigation: Accept only outputs with valid booking detailUrl links and rerun the CLI when links or required result fields are missing.

## Reference(s):

- [Honeymoon Trip Skill Page](https://clawhub.ai/xiejinsong/skills/honeymoon-trip)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendations with comparison tables, booking links, and inline shell commands for retries or CLI setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal results require FlyAI CLI data and booking detailUrl links; failed or partial searches may produce concise retry guidance instead of recommendations.]

## Skill Version(s):

3.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
