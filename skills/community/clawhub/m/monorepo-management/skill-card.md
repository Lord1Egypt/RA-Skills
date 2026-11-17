## Description:

Master monorepo management with Turborepo, Nx, and pnpm workspaces to build efficient, scalable multi-package repositories with optimized builds and dependency management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[watermelon11](https://clawhub.ai/user/watermelon11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, migrate, optimize, and operate JavaScript and TypeScript monorepos with Turborepo, Nx, and pnpm workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deploy and package-publishing snippets could cause unintended production deployments or package releases if copied without review.

Mitigation: Treat deploy and publish snippets as templates, require manual approval gates, and review release workflow permissions before use.

Risk: Unpinned npx tools and GitHub Actions can change behavior or introduce supply-chain risk.

Mitigation: Pin npx package versions and GitHub Actions to reviewed versions or commits.

Risk: Long-lived npm tokens in CI increase blast radius if exposed.

Mitigation: Prefer OIDC or trusted publishing and least-privilege workflow permissions over long-lived npm tokens.

## Reference(s):

- [Turborepo Schema](https://turbo.build/schema.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, YAML, TypeScript, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes template snippets for monorepo setup, dependency management, CI/CD, and package publishing workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
