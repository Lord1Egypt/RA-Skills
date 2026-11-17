## Description:

Intelligent codebase analysis and understanding with caching that explores project structure, identifies modules, analyzes dependencies, and answers questions about code relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect unfamiliar repositories, understand module and dependency relationships, search symbols, ask codebase questions, and produce reports or diagrams before onboarding, refactoring, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default cache handling can execute code from an untrusted repository.

Mitigation: Use the skill only with trusted repositories until pickle caching is replaced with a safe format.

Risk: Repository-local cache directories may already contain unsafe or misleading cached data.

Mitigation: Clear or avoid preexisting .codebase-intelligence directories and prefer a trusted cache location outside repositories.

Risk: Generated reports, diagrams, or index exports may create or overwrite files.

Mitigation: Review output paths before running export or report commands.

Risk: Symlink boundary checks are not confirmed by the security evidence.

Mitigation: Do not run the skill on untrusted repositories until symlink boundary checks are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/oc-codebase-intelligence)
- [Publisher profile](https://clawhub.ai/user/michealxie001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON exports, Mermaid diagrams, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local cache files and optional report, diagram, or index export files.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
