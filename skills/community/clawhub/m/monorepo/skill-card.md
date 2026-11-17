## Description:

Build and manage monorepos with Turborepo, Nx, and pnpm workspaces, including workspace structure, dependency management, task orchestration, caching, CI/CD, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up, migrate, optimize, and operate JavaScript or TypeScript monorepos with shared packages, workspace tooling, CI/CD, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and CI examples rely on mutable third-party code.

Mitigation: Install from a pinned commit or trusted release and pin GitHub Actions to reviewed SHAs before adopting generated workflows.

Risk: The publishing example uses GitHub and npm tokens.

Mitigation: Use least-privilege workflow permissions, avoid broad or long-lived npm tokens, and prefer short-lived trusted publishing where available.

Risk: Generated workflow and release guidance can affect production build, deploy, or package publishing behavior.

Mitigation: Review generated CI/CD and publishing changes before use, especially affected-project logic, cache inputs, and release credentials.

## Reference(s):

- [Monorepo Management skill page](https://clawhub.ai/wpank/skills/monorepo)
- [Turborepo schema](https://turbo.build/schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copy-pasteable examples for workspace layout, package scripts, Turborepo, Nx, pnpm, GitHub Actions, and Changesets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
