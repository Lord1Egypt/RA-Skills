## Description:

Turn setup guides into an askable digital-human quick-start course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Product, customer success, enablement, and support teams use this skill to turn supplied setup guides, manuals, and help articles into an evidence-grounded quick-start course for new users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update the PersonWise CLI and may ask the agent to run update commands supplied by the PersonWise CLI or service.

Mitigation: Install only when PersonWise is trusted, require explicit approval for install or update steps, and approve only normal PersonWise updater commands.

Risk: The workflow can upload selected materials, use browser OAuth, consume existing course credits, and create or publish courses as requested.

Mitigation: Use only materials the user selected or approved, keep the account and service explicit, and require a new request before payments, extra courses, broader visibility, deletion, transfer, or organization administration.

Risk: A generated course can mislead learners if source materials are incomplete, unsupported, or describe high-risk or regulated operations.

Mitigation: Keep course content grounded in supplied materials, avoid unsupported setup or compatibility claims, and require qualified on-site confirmation before high-risk operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-product-first-success)
- [PersonWise service](https://personwise.ai)
- [PersonWise CLI release origin](https://releases.personwise.ai/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON inputs and CLI commands for course creation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interactive digital-human course through the PersonWise CLI and reports concise, secret-free run evidence.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
