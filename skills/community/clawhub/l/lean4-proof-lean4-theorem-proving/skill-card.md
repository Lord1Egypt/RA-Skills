## Description: <br>
Use when working with Lean 4 (.lean files), writing mathematical proofs, seeing "failed to synthesize instance" errors, managing sorry/axiom elimination, or searching mathlib for lemmas - provides build-first workflow, haveI/letI patterns, compiler-guided repair, and LSP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for Lean 4 theorem proving, mathlib search, proof repair, tactic selection, type class troubleshooting, and management of sorries or custom axioms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Lean patches or proof-repair suggestions may be incorrect or incomplete. <br>
Mitigation: Review proposed patches before applying them, run repair work from version control, and verify results with Lean build checks. <br>
Risk: External search workflows may expose private theorem statements or proof states. <br>
Mitigation: Use local search first and send private proof context to external services only when that is acceptable for the project. <br>
Risk: The skill is focused on Lean 4 assistance and should not be treated as broad automation authority. <br>
Mitigation: Install and use it only for Lean 4 proof-assistance workflows. <br>


## Reference(s): <br>
- [Axiom Elimination Reference](references/axiom-elimination.md) <br>
- [Calc Chain Patterns](references/calc-patterns.md) <br>
- [Common Compilation Errors in Lean 4](references/compilation-errors.md) <br>
- [Compiler-Guided Proof Repair](references/compiler-guided-repair.md) <br>
- [Domain-Specific Patterns for Lean 4](references/domain-patterns.md) <br>
- [Guide: Avoiding Instance Pollution in Lean 4](references/instance-pollution.md) <br>
- [Lean LSP Server](references/lean-lsp-server.md) <br>
- [Lean LSP Tools API Reference](references/lean-lsp-tools-api.md) <br>
- [Lean 4 Phrasebook](references/lean-phrasebook.md) <br>
- [Mathlib Integration Guide](references/mathlib-guide.md) <br>
- [Mathlib Style Guide for Lean 4](references/mathlib-style.md) <br>
- [Measure Theory Reference](references/measure-theory.md) <br>
- [Performance Optimization in Lean 4](references/performance-optimization.md) <br>
- [Proof Golfing Patterns](references/proof-golfing-patterns.md) <br>
- [Proof Golfing Safety and Workflow](references/proof-golfing-safety.md) <br>
- [Proof Golfing](references/proof-golfing.md) <br>
- [Refactoring Long Proofs](references/proof-refactoring.md) <br>
- [Sorry Filling Reference](references/sorry-filling.md) <br>
- [Subagent Workflows for Lean 4 Development](references/subagent-workflows.md) <br>
- [Lean 4 Tactics Reference](references/tactics-reference.md) <br>
- [APOLLO compiler-guided repair paper](https://arxiv.org/abs/2505.05758) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Lean code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Lean proof edits, search workflows, build commands, and repair steps; users should inspect generated patches and run Lean builds before relying on results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
