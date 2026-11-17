## Description:

Develop Noir (.nr) codebases. Use when creating a project or writing code with Noir.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jp4g](https://clawhub.ai/user/jp4g)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, compile, test, prove, and verify Noir programs while choosing an appropriate proving backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the skill may run local Noir developer tools or install Barretenberg tooling with bbup, which can affect a developer environment.

Mitigation: Review generated commands, tool versions, and backend choices before executing them in sensitive projects.

Risk: Incorrect assumptions about private inputs, public inputs, public outputs, or the proving backend can lead to unusable Noir workflows.

Mitigation: Define inputs and outputs before implementation, confirm the proving backend, and validate Noir implementations with nargo test.

## Reference(s):

- [Noir Documentation](https://noir-lang.org/docs/)
- [Noir GitHub Codespaces Documentation](https://noir-lang.org/docs/tooling/devcontainer#using-github-codespaces)
- [Barretenberg Reference](references/barretenberg.md)
- [Barretenberg Documentation](https://barretenberg.aztec.network/docs/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
