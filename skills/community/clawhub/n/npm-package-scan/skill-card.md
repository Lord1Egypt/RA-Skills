## Description:

Audit JavaScript and TypeScript repository dependencies for security, supply-chain, maintenance, version, lockfile, and cleanup risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffrey-xiao](https://clawhub.ai/user/geoffrey-xiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review npm, pnpm, Yarn, or Bun dependency risk without changing the repository by default. It helps separate observed evidence from recommendations for security, supply-chain, maintenance, version, lockfile, and cleanup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry-backed checks may send package names and versions to the configured package registry.

Mitigation: Run registry-backed checks only when that metadata can leave the environment; otherwise use the skill's offline-first review path.

Risk: Dependency reports can expose private package names, versions, registry configuration, or repository structure.

Mitigation: Review generated reports before sharing them and avoid running the skill where dependency or private registry metadata is sensitive.

Risk: Automatic dependency fixes or package-manager commands can mutate manifests, lockfiles, installs, or lifecycle behavior.

Mitigation: Keep the review read-only by default and require explicit user approval before upgrades, removals, installs, audit fixes, or lockfile regeneration.

## Reference(s):

- [Review checklist](references/checklist.md)
- [Read-only command guide](references/commands.md)
- [Structured report schema](references/report-schema.md)
- [Report template](references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/geoffrey-xiao/skills/npm-package-scan)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report by default, with optional structured JSON export and read-only shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include explicit network-check context; export writes Markdown or JSON only when requested.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
