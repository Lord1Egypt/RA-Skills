## Description:

Generates comprehensive Markdown technical documentation for a project, including overview, architecture, module, API, data model, dependency, and deployment documentation under docs/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhngdcz](https://clawhub.ai/user/hhngdcz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate project documentation for an existing codebase. It is intended for creating Markdown docs covering architecture, modules, APIs, data models, dependencies, and deployment notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent reads project source and writes generated documentation under docs/.

Mitigation: Install only when source-code reading and docs/ writes are acceptable for the target project.

Risk: Existing documentation may be overwritten or supplemented depending on the user's choice when docs/ already exists.

Mitigation: Review the overwrite or supplement choice before generation and inspect changed documentation files after completion.

Risk: Generated documentation may be incomplete or misleading if source analysis misses behavior or project conventions.

Mitigation: Review generated Markdown before relying on it for engineering, deployment, or external publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhngdcz/skills/hhngdcz-b)

## Skill Output:

**Output Type(s):** [markdown, files, guidance]

**Output Format:** [Markdown files written under docs/, with a concise completion summary returned to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documentation is instructed to be written in Chinese with English technical terms.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
