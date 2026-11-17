## Description:

JavaScript bundle size auditor and budget enforcer that parses webpack stats JSON, Vite bundle reports, Rollup output, or Next.js build output to identify large chunks, budget violations, duplicate dependencies, treeshaking failures, and CI fail-gate commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit JavaScript application build artifacts, understand bundle-size regressions, and produce optimization guidance or CI budget checks for webpack, Vite, Rollup, Next.js, and related builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm and npx examples may introduce ordinary JavaScript supply-chain risk if dependencies are not pinned or lockfiles are ignored.

Mitigation: Use pinned project devDependencies, committed lockfiles, npm ci in CI, and least-privilege CI secrets before running package-based examples.

Risk: Bundle optimization suggestions and CI fail gates can affect application behavior or release workflows if applied without review.

Mitigation: Review generated guidance and test build outputs before committing code, dependency, or CI configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-bundle-size-audit)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, code snippets, and CI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file-analysis guidance; no external API is described by the artifact.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
