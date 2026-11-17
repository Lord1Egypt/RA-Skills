## Description:

Build a complete, production-ready full-stack web application from PRD documents, prototype images, and resource files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zai-org](https://clawhub.ai/user/zai-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn PRDs, prototype images, and resource files into runnable full-stack web applications with design documentation, seed data, backend APIs, frontend UI, verification checks, and a startup script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to install dependencies, reset data, start services, or auto-install browser tooling.

Mitigation: Use it in a disposable or version-controlled workspace and review generated start.sh before running it, especially commands that change data, install packages, or start services.

Risk: PRDs, prototypes, or generated applications may include secrets or private customer data.

Mitigation: Redact sensitive data before use and avoid providing real secrets or private customer data unless the workspace and generated outputs are approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zai-org/skills/glmv-prd-to-app)
- [Seed Data Generation Guide](references/seed_data_guide.md)
- [Visual Verification Guide](references/visual_verification_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, generated application source files, configuration, shell commands, and scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a complete workspace including docs/design.md, README.md, backend and frontend code, seed data, screenshots, and start.sh.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
