## Description: <br>
Build and manage monorepos with Turborepo, Nx, and pnpm workspaces, covering workspace structure, dependency management, task orchestration, caching, CI/CD, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up, migrate, optimize, and operate JavaScript or TypeScript monorepos with shared packages, build orchestration, caching, CI/CD, and package publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-run setup, cleanup, dependency update, deploy, remote-cache login, and package publishing snippets can affect repository state, external services, or published packages. <br>
Mitigation: Review commands before running them in a real repository and test changes in a branch or disposable workspace first. <br>
Risk: Remote cache configuration can expose sensitive build outputs or secrets if configured too broadly. <br>
Mitigation: Review Turborepo remote cache settings and exclude secrets or sensitive build artifacts before enabling shared caching. <br>
Risk: Documentation guidance can become stale as monorepo tooling changes. <br>
Mitigation: Confirm tool-specific commands and configuration against current Turborepo, Nx, pnpm, and Changesets documentation before production adoption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/monorepo) <br>
- [Artifact installation URL](https://github.com/wpank/ai/tree/main/skills/backend/monorepo) <br>
- [Turborepo schema](https://turbo.build/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands and configuration snippets should be reviewed before use in a repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
