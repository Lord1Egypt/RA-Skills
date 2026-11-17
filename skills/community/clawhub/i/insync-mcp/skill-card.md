## Description:

Reads appointments, medications, allergies, messages, forms, balances, and related details from a user's signed-in InSync Healthcare patient portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People using an InSync or Qualifacts behavioral-health portal can ask an agent to review portal information such as appointments, medications, messages, forms, and balances through their signed-in session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the skill can make authenticated requests and return data beyond its stated read-only patient-portal scope.

Mitigation: Use it only when this portal access is needed and trusted; review the requested access and returned information, and avoid installation if that trust is not warranted.

Risk: The security assessment says scanning was partial because two local references were missing, so the evidence is incomplete.

Mitigation: Review the complete release contents and security evidence before relying on the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chrischall/skills/insync-mcp)
- [Portal endpoint reference](artifact/references/endpoints.md)
- [Portal usage recipes](artifact/references/recipes.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Projected JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can contain sensitive health information; show only details needed for the user's request.]

## Skill Version(s):

0.5.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
