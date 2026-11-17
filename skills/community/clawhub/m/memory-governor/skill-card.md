## Description:

Memory governance kernel for AI agents that complements the OpenClaw 2026.6.x memory stack (Dreaming, Active Memory, Memory Wiki, People Wiki, Skill Workshop / Workboard) with explicit correction staging, target-class routing, compiled-surface boundaries, scope/privacy rules, and safer manual hardening rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakenw](https://clawhub.ai/user/sakenw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-system maintainers use this skill to define a shared memory contract for deciding what should be remembered, where it should be routed, and when it should be promoted or excluded. It is most useful in hosts with multiple memory layers, memory-writing skills, optional adapters, or OpenClaw runtime memory surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence persistent agent memory when a host deliberately integrates it.

Mitigation: Review integrations with AGENTS.md, other skills, long-term memory files, and host manifests before relying on the governance contract.

Risk: Sensitive, scoped, or short-lived information could be captured too broadly if host memory rules are applied carelessly.

Mitigation: Keep secrets out of memory, apply the exclusion rules, record scope at capture time, and review compiled memory surfaces for scope widening.

Risk: Unverified corrections or imported content could harden into durable guidance too early.

Mitigation: Stage low-confidence items in learning_candidates and require manual review before promotion to reusable lessons, system rules, or tool rules.

Risk: A host may appear integrated while required memory targets, fallbacks, or writer contracts are incomplete.

Mitigation: Run the host checker and treat the skill as validated only after the relevant checks pass or warnings are consciously accepted.

## Reference(s):

- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [Memory routing](references/memory-routing.md)
- [Promotion rules](references/promotion-rules.md)
- [Exclusions](references/exclusions.md)
- [Compiled surfaces](references/compiled-surfaces.md)
- [Installation and integration](references/installation-integration.md)
- [Host checker](references/host-checker.md)
- [Adapters](references/adapters.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional host-checking, frontmatter-validation, candidate-review, and generic-host bootstrap scripts; it does not automatically modify host files.]

## Skill Version(s):

0.3.2 (source: frontmatter, VERSION, changelog released 2026-06-23, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
