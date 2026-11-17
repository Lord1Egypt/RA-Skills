## Description:

Monorepo internal dependency analyzer for npm/yarn/pnpm workspaces, Cargo workspaces, and Go multi-module repos that maps workspace dependencies, detects circular dependencies, finds orphaned packages, highlights coupling and version mismatches, and generates ASCII or Mermaid dependency graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to analyze monorepo workspace dependencies before refactors, detect cycles and orphaned packages, and understand internal package coupling across npm, pnpm, Yarn, Cargo, and Go workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-discovery instructions can be steered by repository-controlled patterns to read package manifests outside the chosen project.

Mitigation: Use the skill only on trusted repositories and prefer a version that rejects absolute workspace patterns, '..' path components, and symlink escapes before reading discovered manifests.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-monorepo-dep-graph)
- [Publisher Profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with ASCII trees, Mermaid diagrams, tables, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency graphs, cycle findings, fan-in/fan-out metrics, orphaned package notes, version mismatch tables, and refactor guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
