## Description:

Use when setting up or managing a Turborepo-based monorepo. Covers workspace configuration, task pipelines, caching strategies, shared packages, and CI/CD integration for multi-package repositories with Turborepo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and maintain Turborepo monorepos, including workspace configuration, task pipelines, caching, shared packages, selective builds, and CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GitHub Actions CI template exposes build and deployment secrets too broadly.

Mitigation: Scope TURBO_TOKEN and TURBO_TEAM only to Turbo steps and restrict secrets to trusted workflows.

Risk: The deploy preview workflow runs an unpinned deployment CLI with deployment credentials.

Mitigation: Pin or lock the Vercel CLI before passing deployment credentials to that step.

Risk: Remote cache outputs could contain sensitive artifacts if cache outputs are configured too broadly.

Mitigation: Confirm configured Turborepo outputs do not include secrets or sensitive generated files before enabling remote caching.

## Reference(s):

- [Turborepo Workspace Configuration Reference](references/workspace-config.md)
- [Shared Packages Patterns in Turborepo](references/shared-packages-patterns.md)
- [GitHub Actions CI for Turborepo Monorepo](references/ci-github-actions.yml)
- [Turbo JSON Schema](https://turbo.build/schema.json)
- [SchemaStore tsconfig JSON Schema](https://json.schemastore.org/tsconfig)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, YAML, TypeScript, TSX, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for workspace layouts, turbo.json tasks, shared packages, remote caching, selective builds, and GitHub Actions CI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
