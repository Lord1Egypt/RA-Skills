## Description:

Helps users find Korean restaurants and beauty services and request reservations in their preferred language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmp-dev](https://clawhub.ai/user/hmp-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and locals use the skill to find Korean food and beauty venues, review venue details, and request bookings in the language they use in chat.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: A reservation request shares the guest's name, phone number, optional email, and note with HeyYumi and the venue; the hosted service's retention practices were not verified.

Mitigation: Collect only the details needed for the request, review them with the user, and send them only after the user clearly confirms. Configure credentials outside chat.

Risk: A live-status question notifies the venue staff.

Mitigation: Tell the user that their question will contact the venue before sending the request.

## Reference(s):

- [HeyYumi website and MCP guide](https://heyyumi.ai/mcp)
- [HeyYumi developer guide](https://heyyumi.ai/developers)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Localized conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include venue details, reservation request status, and the venue's response; a booking is confirmed only after the venue accepts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
