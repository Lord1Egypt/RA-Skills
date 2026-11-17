## Description:

Developer skill for running Hummingbot and Gateway from source, building wheel and Docker images, and testing against Hummingbot API running from source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, run, verify, and smoke test a local Hummingbot, Gateway, and Hummingbot API development stack from source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer scripts can download and install development dependencies, including Conda, Node.js, pnpm, Git, Docker, and Homebrew, and may make Docker-related system changes.

Mitigation: Run the skill only in an isolated development environment, review scripts before execution, and use check-only or selective install options before allowing system changes.

Risk: The development stack starts local API, Gateway, Postgres, and EMQX services and documents default local credentials and passphrases.

Mitigation: Keep services bound to localhost, do not expose their ports externally, and replace default credentials or passphrases before using any shared or networked environment.

Risk: Build and setup flows can modify local checkout state, environment files, Conda environments, Docker images, and package installations.

Mitigation: Use disposable workspaces or backups for source checkouts and configuration, then verify branch, build, service, and integration status before relying on the environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local development workflows, setup commands, build and verification steps, and smoke-test guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
