## Description:

Run email marketing for agency clients: switch between the client accounts and brands this connection can reach, create a new brand with its own Brand Kit, build each brand's flows and newsletters, and keep each one's sender and contacts separate. Use for marketing agencies and freelancers managing several brands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing agencies and freelancers use this skill to manage email marketing for multiple client brands, keep each brand's sender and contacts separate, and prepare campaigns and flows for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Work or delivery could target the wrong client if the active account or brand is assumed.

Mitigation: Check the available accounts and brands, ask the user to choose, and confirm the selected account and brand before preparing delivery.

Risk: Client contacts or sender details could be mixed across brands, or a campaign could be sent before its audience is approved.

Mitigation: Keep each brand's senders and contacts separate, review the saved delivery target, and launch or schedule only after the user explicitly approves the audience.

## Reference(s):

- [Agency email marketing guide](https://nitrosend.com/agency-email-marketing)
- [Agency Client Email on ClawHub](https://clawhub.ai/nitrosend/skills/nitrosend-agency-client-email)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Natural language guidance and structured actions through Nitrosend tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are scoped to the selected account and brand; sending requires explicit audience approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
