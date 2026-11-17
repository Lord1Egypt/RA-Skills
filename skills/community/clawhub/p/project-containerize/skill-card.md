## Description:

Analyzes a software project and generates Docker-based build, deployment, configuration, and documentation assets for containerized delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyifeiruichuang](https://clawhub.ai/user/zhuyifeiruichuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to containerize existing projects by generating deployment-ready Dockerfiles, Compose manifests, configuration templates, shell commands, and supporting documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows can run Docker build and deployment commands against a real project.

Mitigation: Review generated Dockerfiles, Compose files, and shell scripts before executing them, and run only where Docker builds are acceptable.

Risk: Configuration preparation can copy live .env or other secret-bearing files into deploy/config.

Mitigation: Avoid running the skill on repositories with live secrets, inspect copied configuration files, and replace sensitive values with templates before sharing or committing outputs.

Risk: Some generated runtime containers default to root unless a non-root mode is explicitly selected.

Mitigation: Prefer non-root users, pinned base images, and pinned package-manager versions for production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuyifeiruichuang/skills/project-containerize)
- [Publisher profile](https://clawhub.ai/user/zhuyifeiruichuang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Docker, Compose, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a deploy directory with analysis reports, Dockerfiles, Compose manifests, environment templates, deployment scripts, and containerization documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
