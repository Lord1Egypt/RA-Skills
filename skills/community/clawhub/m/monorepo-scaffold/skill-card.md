## Description:

Initialize a brand-new monorepo project in an empty or near-empty folder after a structured requirements interview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold a new monorepo by confirming project requirements, selecting workspace tooling, generating project files, and verifying the resulting structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run unpinned remote initializer or package-manager commands during scaffolding.

Mitigation: Review and confirm commands before execution, and prefer pinned generator versions instead of latest-version aliases.

Risk: Generated scaffolds can create or modify many project files and initialize git state.

Mitigation: Use the skill in an empty or near-empty target folder, review the summarized scaffold plan, and confirm before writes or git initialization.

Risk: The database compose template includes default credentials and a published local port if used unchanged.

Mitigation: Use unique local secrets and bind services to localhost only, or omit published ports when they are not required.

## Reference(s):

- [Config Templates](references/config-templates.md)
- [Interview Guide](references/interview-guide.md)
- [Stack Recipes](references/stack-recipes.md)
- [Turborepo Schema](https://turbo.build/schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files, configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before writing scaffold files and may run package-manager install, build, lint, test, or project-discovery commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
