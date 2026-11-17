## Description:

Bake, inspect, and manage lnd macaroons for least-privilege agent access, including pay-only, invoice-only, read-only, signer-only, and custom credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and Lightning node operators use this skill to generate and inspect scoped lnd macaroons for agents that need limited node access without using admin.macaroon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Macaroon rotation guidance may leave old credentials unrevoked if the revocation steps are not correct for the target lnd version.

Mitigation: Verify revocation with listmacaroonids and deletemacaroonid for the deployed lnd version before relying on the documented rotation flow.

Risk: Admin macaroons or copied macaroons can expose sensitive Lightning node access, especially in shared containers or uncontrolled environments.

Mitigation: Use only credentials and containers the operator controls, avoid baking or inspecting admin macaroons in shared containers, and prefer scoped role macaroons with restrictive file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roasbeef/skills/lnd-macaroon-bakery)
- [ClawHub publisher profile](https://clawhub.ai/user/roasbeef)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline bash and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role presets, permission URIs, macaroon output paths, inspection steps, and rotation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
