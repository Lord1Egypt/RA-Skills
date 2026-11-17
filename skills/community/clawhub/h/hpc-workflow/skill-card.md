## Description:

Helps an agent set up, operate, and recover a Slurm GPU workspace with durable allocation requests, job-local storage, and verified backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playeriv65](https://clawhub.ai/user/playeriv65)

### License/Terms of Use:

MIT or MIT-0

## Use Case:

Developers and HPC researchers use this skill to configure authorized Slurm GPU access, run and monitor experiments, and recover work from verified backups on their cluster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect cluster profile or resource setting could run commands or request GPUs outside the intended scope.

Mitigation: Review the private profile, transport command, archive paths, and account, GPU, and QoS settings against authorized site facts before applying a bundle.

Risk: Persistent SSH and autosave processes retain privileged access across agent sessions.

Mitigation: Keep credentials out of profiles and treat the SSH master, control socket, and autosave processes as privileged session state.

## Reference(s):

- [HPC Agent Kit repository (declared in skill metadata)](https://github.com/playeriv65/hpc-agent-kit)
- [Operating contract](references/agent-contract.md)
- [Runtime requirements](references/runtime.md)
- [Site-probing guidance](references/site-probing.md)
- [MSI connection requirements](https://msi.umn.edu/getting-started/connecting/connecting-to-msi-systems)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance, shell commands, JSON profiles, and site-specific scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Site-specific operating notes and deployment bundles; private profiles stay outside the installed skill.]

## Skill Version(s):

0.4.1 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
