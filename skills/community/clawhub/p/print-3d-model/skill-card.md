## Description:

Open the 773 LABS custom 3D printing quote page when the user wants to print a 3D model, request a custom 3D print, get a printing quote, or order a 3D printed product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to open the 773 LABS custom 3D printing quote page when they want to request a custom print, quote, or 3D printed product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens an external quote page in Brave and may reuse an already signed-in browser session.

Mitigation: Use the skill only when that destination is expected, verify the 773 LABS page is visible, and stop before login, credentials, payment, account creation, or order submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/print-3d-model)
- [773 LABS quote page](https://773-labs.vercel.app/quote)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Text instructions for browser navigation and verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill opens a specific external quote page, reuses an existing Brave session when available, verifies the destination, and stops before login, credential entry, payment, account creation, or order submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
