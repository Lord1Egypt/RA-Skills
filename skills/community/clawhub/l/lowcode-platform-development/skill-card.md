## Description:

Automates the creation of required development roles, scaffolds the project structure, and generates code for a low-code development platform with Vue2 + ElementUI front-end and Java (Spring Boot) back-end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmyg11](https://clawhub.ai/user/mmyg11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold a low-code platform from scratch, including a Vue2 + ElementUI front end, a Spring Boot back end, role documentation, deployment configuration, and next-step implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced PowerShell generator script and real starter templates are not present in the artifact.

Mitigation: Verify or supply the missing generator script and concrete Vue2 and Spring Boot templates before installing or executing the skill.

Risk: The intended setup may run npm and Maven commands that download dependencies and execute package build hooks.

Mitigation: Choose the target directory deliberately and approve dependency installation and build commands only after reviewing the generated project inputs.

## Reference(s):

- [Architecture Overview for Low-Code Platform](references/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summary with generated project files, code, configuration, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scaffolds a local Vue2 and Spring Boot project structure and reports manual follow-up actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
