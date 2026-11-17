## Description:

Detect the optimal NCCL configuration for distributed GPU training on this machine by checking GPU topology, RDMA availability, intra-node collective bandwidth, peer-to-peer GPU bandwidth, and optional inter-node MPI bandwidth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitsuha-m](https://clawhub.ai/user/mitsuha-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill when setting up or tuning multi-GPU and multi-node training, diagnosing slow NCCL collective communication, or validating a new GPU cluster node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-node mode can turn unvalidated node text into shell commands in the local or MPI environment.

Mitigation: Run only in a controlled GPU cluster environment with trusted nodes values; prefer a version that validates hostnames or IP addresses and uses subprocess argument arrays.

Risk: Running as root or inside broadly privileged containers can increase impact if command input is unsafe.

Mitigation: Run as an unprivileged user and avoid broadly privileged containers unless cluster operations require them.

## Reference(s):

- [NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)
- [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests.git)
- [ClawHub skill page](https://clawhub.ai/mitsuha-m/skills/nccl-optimizer)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown report with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include benchmark results, fallback NCCL environment variables, and ready-to-run inter-node MPI commands.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
