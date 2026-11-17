## Description:

LYGO Sovereign Kernel Seeder helps agents plant local, Merkle-anchored kernel eggs that self-verify on insert and can be loaded after alignment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agent operators use this skill to create, verify, and list local LYGO kernel egg manifests and modules in a content-addressed seed registry. It supports consent-gated local modular capability loading after Merkle verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Seed writes may escape the intended registry path when inputs or seed roots are not tightly controlled.

Mitigation: Use trusted, simple egg IDs, set an explicit safe seed root, inspect generated paths, and avoid shared untrusted seed locations.

Risk: A mutable npx @latest installer path can change between installs.

Mitigation: Prefer pinned installer versions or pinned source references and verify provenance before installing.

Risk: Seeded module files can capture sensitive content if operators provide secret-bearing inputs.

Mitigation: Seed only reviewed, non-secret files and keep consent required for every insert.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Architecture](references/ARCHITECTURE.md)
- [Security](references/SECURITY.md)
- [Kernel Egg Schema](schemas/kernel_egg.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder)
- [Skill Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-sovereign-kernel-seeder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local seed registry and egg JSON files; verification reports ALIGNED, EMPTY, or QUARANTINE.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
