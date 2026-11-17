## Description:

Installs the 5-package multi-chip software stack (vLLM, FlagTree, FlagGems, FlagCX, and vllm-plugin-FL) inside a running GPU container with network mirror detection, dependency ordering, wheel selection, and package validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after GPU container setup to install and validate a multi-chip inference software stack in dependency order. It is intended for running containers with PyTorch and GPU access where the agent can resolve the container name, GPU vendor, network path, and package compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad Docker shell commands inside a running GPU container.

Mitigation: Run only in a disposable or snapshotted container, confirm the exact container name before execution, and avoid accepting container names from untrusted input.

Risk: The installation flow uses mutable external package sources and source repositories.

Mitigation: Prefer direct verified sources, pin commits and package hashes where possible, and review package source choices before installation.

Risk: The skill may append FLAGCX_PATH to ~/.bashrc inside the target container.

Mitigation: Review the shell profile change before allowing it and keep the change scoped to the intended disposable container.

## Reference(s):

- [Network and Mirror Configuration](references/network-mirrors.md)
- [Vendor Mappings for FlagCX](references/vendor-mappings.md)
- [ClawHub skill page](https://clawhub.ai/wbavon/skills/install-stack-flagos)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and a structured JSON final report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package-level install status, versions, gate status, network mirror status, environment details, and errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
