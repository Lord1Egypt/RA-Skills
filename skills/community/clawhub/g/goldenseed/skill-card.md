## Description: <br>
Deterministic entropy streams for reproducible testing and procedural generation with hash verification; not cryptographically secure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beanapologist](https://clawhub.ai/user/beanapologist) <br>

### License/Terms of Use: <br>
GPL-3.0+ <br>


## Use Case: <br>
Developers and engineers use GoldenSeed to install and apply deterministic pseudo-random streams for reproducible tests, procedural generation, simulations, and verifiable seeded outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer uses an unpinned third-party Python package. <br>
Mitigation: Install in a virtual environment, review the package, and pin golden-seed for controlled builds. <br>
Risk: The generated pseudo-random data is not suitable for security-sensitive randomness. <br>
Mitigation: Use GoldenSeed only for reproducible tests or procedural generation; use secrets or os.urandom for passwords, keys, tokens, cryptography, or security-sensitive randomness. <br>


## Reference(s): <br>
- [GoldenSeed ClawHub page](https://clawhub.ai/beanapologist/goldenseed) <br>
- [GoldenSeed GitHub repository](https://github.com/COINjecture-Network/seed) <br>
- [golden-seed on PyPI](https://pypi.org/project/golden-seed/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on reproducible pseudo-random data and includes explicit cautions against cryptographic or security-sensitive use.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
