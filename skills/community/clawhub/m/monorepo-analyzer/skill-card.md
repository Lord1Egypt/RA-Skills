## Description:

Analyze monorepo structure - detect workspace tools (npm/yarn/pnpm/lerna/nx/turbo/cargo/go), map inter-package dependencies, find unused packages, detect version inconsistencies, compute build order, and identify circular dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect large monorepos, identify workspace tooling, map package dependency relationships, find circular dependencies or version mismatches, and compute build order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented stats command can execute unintended local commands when run in a repository with specially crafted paths.

Mitigation: Use the skill only in trusted or low-privilege worktrees, and review or replace the stats command before analyzing untrusted repositories.

## Reference(s):

- [Monorepo Analyzer ClawHub release](https://clawhub.ai/charlie-morrison/skills/monorepo-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable text, JSON, Markdown, or Mermaid graph output with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not install dependencies; works from repository configuration files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
