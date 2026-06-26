## Description: <br>
Detects the optimal NCCL configuration for distributed GPU training on this machine by checking GPU topology, RDMA availability, intra-node collective bandwidth, peer-to-peer GPU bandwidth, and optional inter-node bandwidth via MPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mitsuha-M](https://clawhub.ai/user/Mitsuha-M) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when setting up multi-GPU or multi-node training, diagnosing slow NCCL collective communication, or tuning NCCL for a new cluster node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional node input can be inserted into a shell command without validation. <br>
Mitigation: Use only on GPU hosts or clusters you are authorized to benchmark, avoid untrusted node names, and prefer a fixed version that validates nodes and avoids shell=True before automatic inter-node benchmarking. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Mitsuha-M/nccl-optimizer) <br>
- [NVIDIA NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html) <br>
- [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with bash code blocks and NCCL environment variable recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local GPU, network, and MPI benchmarks; optional nodes= input enables inter-node benchmarking.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
