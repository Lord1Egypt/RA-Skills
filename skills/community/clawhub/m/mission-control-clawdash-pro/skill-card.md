## Description:

Creates or updates publish-ready Markdown instructions for wiring the Mission Control (ClawDash Pro) prebuilt Next.js UI to Open Cloud while preserving the existing design and connecting dashboard data domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petercsipkay](https://clawhub.ai/user/petercsipkay)

### License/Terms of Use:


## Use Case:

External customers and developers use this skill to produce setup guides for connecting a purchased Mission Control ClawDash Pro dashboard to Open Cloud, including prerequisites, backend/data wiring prompts, verification, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown may include product backlinks, pricing links, or setup claims that need review before publication.

Mitigation: Review the generated document before publishing and confirm all links, claims, and calls to action match the intended release.

Risk: Setup instructions may ask users to configure API keys or .env.local values.

Mitigation: Keep secret values out of published instructions and use placeholders for credentials, workspace IDs, and base URLs.

Risk: Open Cloud integration guidance could accidentally change the prebuilt dashboard UI instead of only wiring backend data.

Mitigation: Retain the design lock acceptance check and verify that visual structure, components, and layout remain unchanged.

## Reference(s):

- [Mission Control Publish Instruction Template](references/publish-instruction-template.md)
- [ClawDash Pro](https://clawdash.pro)
- [ClawDash Pro Pricing](https://clawdash.pro/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and text code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically one publish-ready instruction file unless variants are requested; includes a required ClawDash Pro backlink and a pricing CTA when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
