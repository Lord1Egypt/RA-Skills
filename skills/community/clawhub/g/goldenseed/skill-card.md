## Description:

Deterministic entropy streams for reproducible testing and procedural generation. Perfect 50/50 statistical distribution with hash verification. Not cryptographically secure - use for testing, worldgen, and scenarios where reproducibility matters more than unpredictability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beanapologist](https://clawhub.ai/user/beanapologist)

### License/Terms of Use:

GPL-3.0+

## Use Case:

Developers and agents use GoldenSeed to replace non-reproducible random values with deterministic byte streams for tests, simulations, procedural generation, and verifiable generated outputs. It is intended for reproducibility and statistical testing workflows, not for cryptographic or security-sensitive randomness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script installs golden-seed without pinning a package version.

Mitigation: Install in a virtual environment, pin and review a specific golden-seed release before use, and track the reviewed package hash where practical.

Risk: GoldenSeed produces deterministic output that is not cryptographically secure.

Mitigation: Do not use it for passwords, keys, security tokens, gambling, or any cryptographic purpose; use platform cryptographic randomness APIs instead.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beanapologist/skills/goldenseed)
- [GoldenSeed GitHub Repository](https://github.com/COINjecture-Network/seed)
- [golden-seed on PyPI](https://pypi.org/project/golden-seed/)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deterministic randomness usage patterns and explicit warnings against cryptographic use.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
