## Description:

Generate fullstack applications with OpenClaw, including frontend, backend, database, and deployment scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate starter fullstack application projects with selectable frontend, backend, database, Docker, CI/CD, authentication, and API scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can overwrite files in the target project directory.

Mitigation: Run it only in a new empty directory or a disposable workspace, then review the generated files before merging them into an existing project.

Risk: Generated Docker configuration can use an arbitrary database image and weak default credentials.

Mitigation: Replace database images with trusted pinned images and change generated credentials before deployment or committing the project.

Risk: Generated backend examples include permissive CORS settings.

Mitigation: Restrict CORS origins, methods, and credentials handling to the intended deployment environment before production use.

Risk: Untrusted generator arguments can affect created paths and generated configuration.

Mitigation: Use trusted project, frontend, backend, and database arguments only, and inspect the generated Docker Compose file before running services.

## Reference(s):

- [Openclaw Fullstack App release page](https://clawhub.ai/sunshine-del-ux/skills/openclaw-fullstack-app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Generated project files with command-line status output and documentation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates frontend, backend, Docker Compose, CI/CD, and documentation directories for a generated application.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
