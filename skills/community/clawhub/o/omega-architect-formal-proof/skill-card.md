## Description:

Formal theorem proving with omega-architect: install the CLI, configure a Lean 4 toolchain and an LLM backend, and drive the generate -> compile -> verify loop (`omega prove`), including strategy modes, budgets and no-LLM smoke tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and researchers use this skill to install and operate the omega-architect CLI for Lean 4 proof search, compile-gated candidate proofs, and no-LLM smoke tests before spending model tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run a research CLI from GitHub and execute Lean-related tooling.

Mitigation: Pin the documented version, install in a clean project environment, and review commands before execution.

Risk: Proof generation can send theorem prompts to an LLM provider and incur token or compute costs.

Mitigation: Protect API keys, start with low sample, round, and timeout settings, and use local backends only after measuring quality and cost.

Risk: Results are not compiler-verified when the Lean toolchain is missing or unavailable.

Mitigation: Check Lean availability before interpreting proof results and treat only compiler-accepted candidates as verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/omega-architect-formal-proof)
- [omega-architect homepage](https://github.com/diamond2nv/omega-architect)
- [Lean 4 toolchain installer](https://github.com/leanprover/elan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash and Lean command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, configuration, proof-search, budget-control, and verification-checklist guidance.]

## Skill Version(s):

0.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
