## Description:

Deploy frontend and full-stack projects to IGA Pages, including Pages Functions and API-route workflows when the user explicitly requests IGA Pages deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seasonrui](https://clawhub.ai/user/seasonrui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy frontend and full-stack projects to IGA Pages, configure project environment variables and integrations, and implement Pages Functions or API routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require cloud credentials for headless login.

Mitigation: Avoid pasting long-lived secrets into chat or reusable shell history; use browser login when available and use scoped AK/SK credentials only when headless login is required.

Risk: The skill can change remote deployment, environment, or integration state.

Mitigation: Confirm production deploys, environment mutations, and integration changes before executing the relevant IGA Pages commands.

Risk: Pulling project environment variables writes secrets to .env.local.

Mitigation: Run env pull only for local development, keep .env.local protected, and ensure it remains gitignored.

Risk: Mutable CLI installation can change behavior across runs.

Mitigation: Prefer a pinned project-local CLI install when possible and verify the CLI version is compatible before deploying.

## Reference(s):

- [IGA Pages ClawHub Skill Page](https://clawhub.ai/seasonrui/skills/iga-pages)
- [Environment Variables](references/env.md)
- [Serverless Functions (API Routes)](references/functions.md)
- [Integrations](references/integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment, environment, integration, and Pages Functions guidance based on the user's project and deployment intent.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter says 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
