# Evidence required for a site profile

Keep a private probe report with observed hostname/user, command output, timestamp
and relevant official site documentation. Recheck mutable queue and access facts
before requesting resources. Do not embed passwords, tokens, private keys or MFA
responses in the profile, command arguments or repository.

| Fact | Useful evidence | Consequence |
| --- | --- | --- |
| Supported transport | Existing SSH config/CLI, successful identity check | Reuse it; name the actual login node if shared-home services require pinning. |
| Authentication ownership | Key route or persistent authenticated master | Ordinary calls reuse authentication and fail closed; explicit login owns any new challenge. |
| Scheduler | `command -v salloc srun squeue sacct scontrol`, site rules | These templates implement Slurm; another scheduler needs an adapter. |
| Helper runtime | Bash 4+, Python 3.6+, GNU tar with listed incrementals, zstd, flock, GNU coreutils/date, awk, find, sort, pgrep and tmux | Syntax checks do not establish that compute nodes have these tools or compatible flags. |
| Account and QoS | `sacctmgr show assoc` and `scontrol show partition` | Allowed QoS is the intersection, including a verified default if no QoS is specified. |
| GPU eligibility/capacity | GRES, CfgTRES/AllocTRES and partition policy | Mixed CPU state does not prove free GPUs; idle GPUs may be reserved or inaccessible. |
| Compute access | A permitted allocated-node identity probe | Direct SSH and PSC terminal bridge are different backends; never guess access. |
| Local storage | Site policy plus allocated-node `findmnt`, writability and actual environment | It must be disk-backed and scoped to the job; `/dev/shm` is memory. |
| Persistent outputs/archive | Site storage policy, quota and mount/path checks | Neither local scratch nor purgeable global scratch is a checkpoint archive. |
| Shared filesystem locks | Hold an archive lease on compute; independently try it from login | Same-host tests alone do not prove cross-host exclusion. |
| Toolchain | Modules/compiler/runtime requirements for the actual repository | Optional repository/site launchers own CUDA/GCC setup. |

Example read-only inventory: `hostname`, `id`, `squeue -u "$USER"`,
`scontrol show partition`, `sinfo -N`, `sacctmgr show assoc where user="$USER"`.
Use supported cluster commands/CLI, rather than creating a parallel connection
route. Sites can restrict accounting visibility; record that limitation explicitly.
For desktop arguments, allocated tmux namespaces and compute environment probes,
read [operating lessons](operations.md). Shared home and the same hostname do not
establish that two connections see the same process or socket context.

Inspect allocated GPU TRES as well as CPU availability; a mixed node can have all
GPUs occupied, and a drained node's unused GPUs cannot accept new work. Recheck
immediately before submission. A verified comma-separated partition list can
let one request consider several eligible queues; the profile must establish
QoS permission in every listed partition. Inspect the granted job's actual
account, QoS, partition and GPU TRES: site submission plugins can normalize
requested parameters. Keep requested and observed values distinct in evidence.

The profile's `verified` object is a summary of established evidence, not a
switch to make an untested assumption valid. If a compute probe cannot run, stage
the profile work that can be supported and label compute/storage acceptance pending.
Use a disposable, small allocation for authorized probes; inspect existing jobs
first. Retire only owned probe allocations covered by the validation scope.

`transport.exec_argv` must accept a shell script on stdin. An authenticated SSH
route can use `ssh LOGIN bash -s`. If the user's supported CLI instead exposes
literal `exec` and binary `push`, use the packaged `scripts/common/shim_exec.py` bridge:
`uv run --no-project --python 3.12 python /SKILL/scripts/common/shim_exec.py -- SHIM_PROGRAM SHIM_ARGUMENTS`.
For a Windows `.ps1` shim, its argv starts with `pwsh -NoProfile -File /PATH/SHIM.ps1`.
The bridge stages verified bytes using that same CLI; it never initiates login,
uses SCP or places a large payload in Windows process arguments. Store absolute
skill/shim paths in the private profile and test the stdin route with a small
identity script before deployment.

MSI reference: a holder on a separate always-on host can retain authenticated
SSH across desktop disconnects. Requested disk-backed scratch requires the
site's explicit local-disk resource request. PSC reference: the allocation pane
can remain attached to compute tmux and provide command dispatch when direct
login-to-compute SSH is unavailable. The source sites' names, accounts, paths,
toolchain versions and resource limits are examples, not universal defaults.
