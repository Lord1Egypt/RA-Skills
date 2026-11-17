## Description:

Turns release notes and migration materials into a grounded interactive digital-human course for adopting a product update, feature launch, migration, or breaking change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, customer success teams, and enablement teams use this skill to create a grounded adoption course for a concrete product update, feature launch, migration, or breaking change. The course explains impact, required steps, deadlines, caveats, and support paths using the user's supplied source materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can install or upgrade the local PersonWise CLI.

Mitigation: Require explicit approval before installation or upgrade and use the bundled verifier for the official PersonWise release.

Risk: The workflow uses browser OAuth and account-scoped PersonWise access.

Mitigation: Use browser OAuth only, never request or handle passwords, tokens, authorization codes, cookies, or other secrets, and pin the selected account alias.

Risk: The workflow can upload user-selected source materials to PersonWise.

Mitigation: Upload only files the user named, attached, or explicitly selected, and keep course access private unless the user requests broader access.

Risk: Creating a course can consume existing PersonWise course credits.

Mitigation: Check account readiness before creating a course, create only the requested number of courses, and never purchase credits automatically.

Risk: Unsupported assumptions could produce misleading adoption guidance.

Mitigation: Keep the course evidence-locked to supplied materials, carry dates and required actions exactly, and flag unclear information for user confirmation.

## Reference(s):

- [Product Change Adoption Course on ClawHub](https://clawhub.ai/personwiseai/skills/personwise-product-change-adoption)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, text]

**Output Format:** [Markdown prose with JSON payloads and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a bounded local blueprint file, invoke the PersonWise CLI with JSON responses, and return concise status evidence plus the appropriate course URL when creation succeeds.]

## Skill Version(s):

2.1.9 (source: server release metadata and skill attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
