## Description:

Deployment assistant that detects project deployment strategies and helps generate configuration, run prechecks, deploy, and monitor K8s/Helm, Docker Compose, Vercel, and Fly.io releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to initialize deployment configuration, run deployment readiness checks, execute deployments, and monitor rollout status across common container and platform targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-controlled deployment commands may run with the user's deployment privileges.

Mitigation: Use the skill only on repositories whose deployment configuration is trusted, and review each generated or selected command before execution.

Risk: Skip or force options can bypass normal deployment checks.

Mitigation: Require explicit human review before using skip or force options, especially for production deployments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment configuration such as .deploy.yaml and command recommendations for the current repository.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
