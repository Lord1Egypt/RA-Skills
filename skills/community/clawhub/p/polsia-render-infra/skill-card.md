## Description:

Apply Render-specific deployment requirements for Polsia apps, including /health checks and migration strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentlevier](https://clawhub.ai/user/agentlevier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to adapt Polsia applications for reliable Render deployment, including health checks, startup migrations, package scripts, frontend builds, and durable file storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing or incorrect /health endpoint can cause Render deployments to fail health checks.

Mitigation: Confirm the app exposes /health, not /api/health, and returns HTTP 200 before deployment.

Risk: Running database migrations in Render's build command can fail because DATABASE_URL is not available there.

Mitigation: Run migrations during server startup and verify the startup path against the target project's database setup.

Risk: Using local disk storage for uploaded files can lose data because Render filesystems are ephemeral.

Mitigation: Use durable external storage, such as an R2-backed proxy, for user files.

Risk: Missing package.json build or start scripts can block Render deployments.

Mitigation: Review package.json before release and keep explicit build and start scripts for the app layout.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
