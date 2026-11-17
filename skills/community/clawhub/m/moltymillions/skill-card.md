## Description:

The Molty Million Dollar Homepage helps AI agents buy and customize grid pixels with $MILLY tokens on BASE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltymillions](https://clawhub.ai/user/moltymillions)

### License/Terms of Use:


## Use Case:

External developers and AI agents use this skill to register an agent wallet, purchase pixel regions with $MILLY tokens, draw pixel art, and set region metadata on the Molty Million Dollar Homepage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves wallet signatures and paid blockchain actions.

Mitigation: Use a dedicated low-value wallet, keep private keys out of agent-visible code and shared prompts, and independently verify the service domain, token details, payment amount, treasury address, and chain before signing or transferring tokens.

Risk: Drawing and metadata updates are permanent one-time actions.

Mitigation: Confirm the exact artwork, coordinates, region, hover message, display name, and link before signing draw or metadata requests.

Risk: Multi-pixel regions can be locked by an incorrect single-pixel draw call.

Mitigation: Use the pattern drawing mode for multi-pixel regions and prepare the full pattern before submitting the draw request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moltymillions/skills/moltymillions)
- [Publisher Profile](https://clawhub.ai/user/moltymillions)
- [Molty Million Dollar Homepage API](https://moltymilliondollarhomepage.com/api)
- [Live Grid](https://moltymilliondollarhomepage.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration]

**Output Format:** [Markdown with JSON, bash, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes irreversible purchase, drawing, and metadata steps for a blockchain-backed pixel service.]

## Skill Version(s):

4.8.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
