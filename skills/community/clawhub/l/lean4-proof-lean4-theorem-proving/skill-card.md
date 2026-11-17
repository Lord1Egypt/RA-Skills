## Description:

Use this skill for Lean 4 proof development, including mathematical proofs, compiler-guided repair, type class instance issues, sorry and axiom management, mathlib search, and LSP-assisted workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when creating, maintaining, or repairing Lean 4 proofs. It supports build-first proof work, mathlib discovery, tactic selection, compiler-error diagnosis, proof refactoring, and elimination of temporary sorries or custom axioms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed proof edits or repair steps may introduce incorrect Lean code or leave misleading proof scaffolding.

Mitigation: Review patches before applying them, run `lake build`, and verify that completed results have no remaining sorries or custom axioms.

Risk: Proof goals, identifiers, or repair logs may expose sensitive project details when external search or remote tools are used.

Mitigation: Keep repair logs local for sensitive projects and prefer local search or LSP-assisted workflows when confidentiality matters.

## Reference(s):

- [Axiom Elimination Reference](references/axiom-elimination.md)
- [Calc Chain Patterns](references/calc-patterns.md)
- [Common Compilation Errors in Lean 4](references/compilation-errors.md)
- [Compiler-Guided Proof Repair](references/compiler-guided-repair.md)
- [Lean 4 Domain-Specific Patterns](references/domain-patterns.md)
- [Guide: Avoiding Instance Pollution in Lean 4](references/instance-pollution.md)
- [Lean LSP Server](references/lean-lsp-server.md)
- [Lean LSP Tools API](references/lean-lsp-tools-api.md)
- [Lean 4 Phrasebook](references/lean-phrasebook.md)
- [Mathlib Guide](references/mathlib-guide.md)
- [Mathlib Style Guide](references/mathlib-style.md)
- [Measure Theory Reference](references/measure-theory.md)
- [Performance Optimization](references/performance-optimization.md)
- [Proof Golfing](references/proof-golfing.md)
- [Proof Golfing Patterns](references/proof-golfing-patterns.md)
- [Proof Golfing Safety](references/proof-golfing-safety.md)
- [Proof Refactoring](references/proof-refactoring.md)
- [Sorry Filling](references/sorry-filling.md)
- [Subagent Workflows](references/subagent-workflows.md)
- [Tactics Reference](references/tactics-reference.md)
- [APOLLO compiler-guided repair paper](https://arxiv.org/abs/2505.05758)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Lean code snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose proof edits, Lean commands, build checks, search strategies, and local workflow steps for agent review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
