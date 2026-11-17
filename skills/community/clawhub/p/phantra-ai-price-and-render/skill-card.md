## Description:

Prices a Phantra scene or still in credits, starts it on the person's yes, and reports where it stands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

### License/Terms of Use:

MIT-0

## Use Case:

People using Phantra can get a current credit quote for scene renders or a still, approve each spend in chat, and check render progress. The skill is for pricing and rendering existing scenes or images, rather than writing scenes or applying effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering spends studio credits, and connector billing and token safeguards have not been independently verified.

Mitigation: Show the quoted model, duration, and credit cost, then wait for explicit approval for that quote before starting a render.

Risk: A retry after an uncertain approval could create a duplicate spend.

Mitigation: Check the job or scene status before retrying; do not repeat an approval when its outcome is uncertain.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zeropage-onryo/skills/phantra-ai-price-and-render)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Conversational text with Phantra render requests and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes costs and waits for explicit approval before starting each paid render stage.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
