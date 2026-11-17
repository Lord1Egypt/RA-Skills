## Description:

AI-native spec-driven development tool. Create, manage, and apply specifications with your agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcoleongdev](https://clawhub.ai/user/marcoleongdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use LightSpec to guide an agent through installing and operating the LightSpec CLI for spec-driven development workflows, including initialization, spec creation, validation, and implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to install the LightSpec npm package globally.

Mitigation: Confirm trust in the LightSpec npm package and publisher before installation, and avoid running global npm installs with elevated privileges.

Risk: LightSpec commands such as init or apply can create or modify project files.

Mitigation: Review project changes from LightSpec before keeping them, especially after initialization or apply workflows.

## Reference(s):

- [LightSpec repository](https://github.com/augmenter-dev/lightspec)
- [Node.js](https://nodejs.org)
- [LightSpec ClawHub listing](https://clawhub.ai/marcoleongdev/skills/lightspec)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead an agent to install an npm package and run commands that create or modify project files.]

## Skill Version(s):

0.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
