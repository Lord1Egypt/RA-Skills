## Description:

Audits TypeScript projects for any usage, weak tsconfig safety settings, type-coverage gaps, and suppression comments, then produces prioritized remediation guidance and CI budget configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess TypeScript type safety, locate high-priority any usage, review tsconfig strictness settings, and prepare CI type-coverage enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running an unpinned npm package through npx, including examples suitable for CI, which creates a supply-chain review concern.

Mitigation: Pin type-coverage as a devDependency with a committed lockfile, run the local binary or npx --no-install, and execute audits with minimal privileges.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-ts-any-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes static-analysis findings, ranked file hotspots, tsconfig recommendations, and optional .type-coverage CI budget content.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
