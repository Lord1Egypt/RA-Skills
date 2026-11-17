## Description:

Builds or refactors GameLearningRuntime adapters and trainable environments for authorized game runtimes while preserving privacy, action boundaries, and learner-neutral contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold or refactor authorized game-runtime adapters, research manifests, reward configuration, and reproducible training projects for GLR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated package checks may run in a shell with unrelated secrets.

Mitigation: Run checks in a clean shell or CI job without unrelated secrets.

Risk: Loader or live-runtime integration may interact with an unintended game target.

Mitigation: Limit runtime work to explicitly permitted offline or test targets and verify exact target binding before actions.

Risk: Synthetic scaffold checks may be mistaken for proof of live runtime support.

Mitigation: Verify the referenced GLR CLI workflow separately and require a bounded authorized runtime trace before claiming live acceptance.

## Reference(s):

- [GLR Adapter Builder on ClawHub](https://clawhub.ai/loonghao/skills/glr-adapter-builder)
- [Runtime host integration](artifact/references/runtime-host.md)
- [Validation gates](artifact/references/validation-gates.md)
- [Research and reward safeguards](artifact/references/research-and-reward.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Guidance]

**Output Format:** [Python project files, JSON/TOML configuration, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scaffolds are synthetic until validated against an authorized runtime.]

## Skill Version(s):

0.26.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
