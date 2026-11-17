## Description:

Turns approved partner program materials into an askable interactive digital-human course for channel partners and resellers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Partner-program and enablement teams use this skill to turn approved partner materials into a grounded interactive course. Learners receive the product story, deal-flow guidance, program rules, and a self-check while unsupported commercial or contractual questions are routed back to the partner team.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving an opaque PersonWise update command could change the CLI or installed Skill.

Mitigation: Review update prompts before approval, run only the exact update action after explicit user approval, and stop if approval is declined.

Risk: The workflow uses browser OAuth, uploads user-selected training materials, consumes existing course credits, and can broaden course access when requested.

Mitigation: Use only named or attached materials, avoid handling secrets, check course readiness before creation, and keep courses private unless broader access is explicitly requested.

Risk: Partner training can create public exposure if it overstates commissions, territories, claims, branding permissions, or commercial terms.

Mitigation: Keep course content evidence-locked to approved materials and route unsupported commercial or contractual questions back to the user's partner team.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/personwiseai/skills/personwise-partner-training)
- [PersonWise publisher profile](https://clawhub.ai/user/personwiseai)
- [Signed PersonWise service descriptor](artifact/assets/service-descriptor.signed.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status and delivery details with structured JSON course inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interactive digital-human course through the PersonWise workflow; the agent reports secret-free run, review, source, access, and playability evidence.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill invocation attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
