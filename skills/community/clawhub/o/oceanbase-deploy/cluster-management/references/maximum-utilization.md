# Multi-Node Maximum-Utilization Deployment

Use this workflow when the user explicitly requests maximum utilization or when a new OceanBase cluster request does not specify resource values, a cap, or a non-maximum sizing profile. Do not ask the user to choose a deployment size in the latter case. Explicit user sizing takes precedence. Maximum utilization applies only to the resolved target hosts and requested database component; it does not add nodes, components, tenants, or topology.

For an OBD-managed community or commercial distributed OceanBase cluster, this workflow provides cluster-consistent sizing: derive each node's verified candidate independently, take the minimum for every resource key, and apply one common specification to every Observer. On shared hosts, use the capped path only after the required reserves or caps are known.

This deterministic baseline is verified against the shared `plugins/oceanbase/4.2.0.0/generate_general_config.py` implementation. The reviewed OBD source groups commercial distributed `oceanbase` and community distributed `oceanbase-ce` in the same OceanBase component family and routes their generic generation/lifecycle behavior through the common plugin tree; the formulas are therefore not community-only. Reconfirm the selected installed generator, keys, constants, and checksum before use. Do not transfer these formulas to another product/component family or to an installed distributed generator whose behavior differs, and do not silently fall back to a mini or arbitrary profile when derivation is unresolved.

## Required Shared Gates

Before live discovery or execution, read and apply:

- [product and capability resolution](../../references/product-and-capability-resolution.md);
- [operation contract](../../references/operation-contract.md), including OBD startup writes;
- [configuration-file deployment](config-deployment.md) for artifact, manifest, path, port, and execution rules;
- [completion criteria](../../references/completion-criteria.md);
- [failure recovery and evidence](../../references/failure-recovery-and-evidence.md) after any failure or mixed result.

## Meaning and Scope

Maximum utilization configures capacity limits; it does not manufacture workload. An idle Observer will not continuously consume all configured CPU or memory. Data and clog files can reserve or consume substantial disk during initialization, while CPU and memory use grow with workload.

For a multi-node cluster:

```text
cluster_value[key] = min(node_candidate[key] across every target node)
```

Calculate the minimum independently for each key. Different nodes may limit CPU, memory, data, and log disk. Do not average, sum, choose one nominally smallest host, or allow heterogeneous per-server maxima. Larger nodes intentionally retain surplus capacity.

Host maximum utilization is separate from tenant allocation. Do not create a tenant, enable `auto_create_tenant`, or pass an automatic-tenant option unless the user separately requests a tenant after the Observer cluster is accepted.

`obd perf` is a fixed-name single-node shortcut with implicit force/cleanup behavior. Route it through [quick-deploy shortcuts](lifecycle.md#quick-deploy-shortcuts). Multi-node maximum utilization uses a reviewed `obd cluster autodeploy` configuration with consistent generation; never repeat `perf` on each node.

## Eligibility and Stop Conditions

Automatic whole-host maximum sizing is allowed only on hosts dedicated to this deployment. If a host is shared, already runs OceanBase or unrelated workloads, or must preserve an absolute reserve, stop unless the user supplies explicit CPU, memory, and disk reserves or caps and accepts a capped shared-host deployment.

Before sizing, prove:

- the exact OBD executable/build, `OBD_HOME`, installed `autodeploy`, consistent-generation, and strict-check options, selected distributed component plugin, generator path, and generator checksum;
- one exact compatible OceanBase artifact, release, architecture, hash, repository source, and dependency closure for every node;
- every management address maps to a unique physical host;
- when the user supplied no deployment paths, each host's base directory was selected through the configuration-deployment [largest writable persistent filesystem rule](config-deployment.md#default-deployment-base-directory) under the established login-session user before any disk formula was evaluated;
- the deployment name, app identity, ports, and canonical home/data/redo paths do not collide with registered or unmanaged state;
- each selected path is new or empty, non-symlinked, owned by the deployment user, and located on the intended filesystem;
- blocks, inodes, user/project quota, mount identity, and future commitments are known for every selected filesystem;
- clocks, routes, SSH, firewall/security-group policy, OS, architecture, GLIBC, instruction set, and filesystem are compatible;
- no unrequested colocated component or workload consumes the budget.

Two nodes or multiple logical zones in one physical failure domain are a capacity/testing topology, not automatic production HA. Establish replica and failure-domain requirements before claiming high availability.

Stop instead of calculating an executable maximum when the selected generator cannot be inspected, host state is stale, cgroup limits are unresolved, paths map to unknown storage, package compatibility is unproved, or the deployment would require an unapproved host/system mutation.

## Capture One Sizing Snapshot

Use the same SSH identity OBD will use. Capture every node in one bounded window and repeat the volatile checks immediately before execution:

Resolve omitted deployment paths before this snapshot. The default path selection is per host: choose that host's eligible writable persistent filesystem with the greatest usable free capacity, then use the resulting canonical home/data/redo parents in the commands and formulas below. Do not measure an arbitrary home-directory path first and call that maximum utilization.

```bash
hostname
cat /etc/machine-id
cat /etc/os-release
getconf GNU_LIBC_VERSION
nproc
nproc --all
grep -c '^processor' /proc/cpuinfo
grep -E 'Cpus_allowed_list|Mems_allowed_list' /proc/self/status
cat /proc/self/cgroup
findmnt -t cgroup,cgroup2
free -b
df -B1 <home-parent> <data-parent> <redo-parent>
df -i <home-parent> <data-parent> <redo-parent>
findmnt -T <home-parent>
findmnt -T <data-parent>
findmnt -T <redo-parent>
ss -lntp
ps -eo user,pid,rss,%mem,%cpu,args --sort=-rss
```

Also inspect active containers and service managers when present. Existing deployments, processes, listeners, quotas, or future disk growth remain commitments even when instantaneous use is low.

### Effective CPU

Define `effective_cpu` as the floor of the smallest allowance imposed by online CPUs, process affinity, cpuset, and CPU quota. For cgroup v2, inspect `cpu.max`, `cpuset.cpus.effective`, `memory.max`, and `memory.current` at the process cgroup and every parent up to the cgroup2 mount. For cgroup v1, map and inspect the corresponding CPU, cpuset, and memory controller files at every applicable ancestor.

The verified generator counts `processor` entries in `/proc/cpuinfo`, subtracts two, and clamps to eight. It does not account for every offline, affinity, cpuset, quota, or memory-cgroup constraint. Reproduce it against effective capacity:

```text
generator_min_cpu_count = 8
node_cpu_candidate = max(generator_min_cpu_count, effective_cpu - 2)
cluster_cpu_count = min(node_cpu_candidate across all nodes)
```

Do not impose a Skill-specific CPU eligibility threshold on a dedicated host. Apply the verified generator formula internally, including when `effective_cpu` is below the generator floor, and continue through reviewed `autodeploy --strict-check`; do not stop, prompt, or mark acceptance failed solely because the resulting `cpu_count` exceeds that host's effective CPU count. Keep the generator floor, reserve calculation, and effective-to-configured comparison out of normal user-facing progress and completion messages. Explain them only when the user explicitly requests diagnostics or when startup or runtime health fails. For a shared host, the approved CPU reserve remains a hard boundary; apply the capped-mode stop rule below if the generator floor consumes it.

## Derive Dedicated-Host Candidates

These formulas apply only when all seven absolute resource keys and their percentage alternatives are initially unset, only Observer is selected, `max_syslog_file_count` is known, and disk capacity is sufficient to avoid the generator's shortage-recovery branches. Use integer bytes throughout (`GiB = 2^30`, `MiB = 2^20`) and normalize every formatted value back to bytes before comparing it.

For each node:

```text
cpu_count = max(8, effective_cpu - 2)
memory_raw = max(6 GiB, floor(MemAvailable * 0.9))
memory_limit = memory_raw

system_memory =
  1 GiB                    when memory_raw < 12 GiB
  5 GiB                    when memory_raw < 20 GiB
  6 GiB                    when memory_raw < 40 GiB
  7 GiB                    when memory_raw < 60 GiB
  8 GiB                    when memory_raw < 80 GiB
  9 GiB                    when memory_raw < 100 GiB
  10 GiB                   when memory_raw < 130 GiB
  floor(memory_raw * 0.08) otherwise

log_disk_size = (memory_raw - system_memory) * 3 + system_memory
slog_reserve = 4 GiB
```

For the verified generator:

```text
syslog_reserve = 1 GiB
  when max_syslog_file_count == 0

syslog_reserve = 256 MiB
  * max_syslog_file_count
  * max_syslog_type_file_count
  otherwise
```

Confirm `max_syslog_type_file_count` from the selected plugin context; the reviewed baseline used four. Do not hard-code it for another generator.

### Data and Clog on One Filesystem

Let `F` be available bytes on the shared data/clog filesystem. Let `H` equal `syslog_reserve` only when `home_path` is also on that filesystem; otherwise `H = 0`.

Calculate the capacity remaining after every fixed commitment on this filesystem, then reserve five percent of that remainder for operational growth:

```text
shared_remaining = F - H - slog_reserve - log_disk_size
require shared_remaining > 0

disk_data_budget = floor(shared_remaining * 0.95)
operational_reserve = shared_remaining - disk_data_budget
require disk_data_budget >= 2 GiB

datafile_size = min(disk_data_budget, log_disk_size)
datafile_maxsize = disk_data_budget
datafile_next = max(2 GiB, floor(datafile_maxsize * 0.10))

require 0 < datafile_next <= datafile_maxsize
require H + slog_reserve + log_disk_size
  + datafile_maxsize + operational_reserve <= F
```

`datafile_next` is an increment within `datafile_maxsize`, not an additional filesystem commitment. Never raise `datafile_maxsize` to `log_disk_size` when the remaining data budget is smaller: doing so would promise future data growth that the shared filesystem cannot hold. Recheck both inequalities after capacity formatting and immediately before execution; stop rather than reducing the operational reserve or relying on initial allocation alone.

### Data and Clog on Different Filesystems

Let `Fd` and `Fc` be available bytes on the data and clog filesystems. Let `Hd` or `Hc` equal `syslog_reserve` only on the filesystem containing `home_path`; otherwise use zero.

```text
datafile_size = 3 * memory_raw
require Fd >= Hd + slog_reserve + datafile_size

datafile_maxsize = floor((Fd - Hd - slog_reserve) * 0.95)
datafile_next = floor(datafile_maxsize * 0.10)
require datafile_maxsize > datafile_size

require Fc >= Hc + log_disk_size
```

These formulas deliberately stop before automatic disk-shortage recovery. If a requirement fails, finite cgroup memory exists, percentage or explicit values are already present, components are colocated, quota applies, or the generator differs, inspect and reproduce the exact selected branch or use user-approved conservative caps. Never launch a disposable deployment merely to discover generated values.

## Shared-Host Capped Candidates

For an explicitly approved capped deployment, use the user's absolute reserves rather than calling current free resources a whole-host maximum:

```text
node_cpu_candidate = max(8, effective_cpu - approved_cpu_reserve)
node_memory_candidate <= floor_GiB(
  min(MemAvailable, cgroup_limit - cgroup_usage)
  - approved_memory_reserve
)

for every filesystem:
  existing future commitments
  + this deployment's commitments
  + approved_disk_reserve
  <= available blocks or quota
```

Require `memory_limit >= 6 GiB`. The verified generator disables production mode below 16 GiB. If the eight-core CPU clamp consumes the approved reserve, stop and obtain revised caps or another host.

## Build the Common Configuration

Record these verified node candidates before taking minima:

```text
cpu_count
memory_limit
system_memory
datafile_size
datafile_maxsize
datafile_next
log_disk_size
```

For every key, calculate the cluster minimum independently. Enforce before and after capacity formatting:

```text
datafile_size <= datafile_maxsize
0 < datafile_next <= datafile_maxsize
```

Put the seven explicit common values in the resolved distributed component's `global` section (`oceanbase-ce.global` or `oceanbase.global`); keep only server identity, paths, ports when server-specific, and zones in named server stanzas. Do not combine absolute values with `memory_limit_percentage`, `datafile_disk_percentage`, or `log_disk_percentage`.

Render the complete YAML from exactly one matching distributed blueprint: [community](deployment-templates/community.md) for `oceanbase-ce` or [commercial](deployment-templates/commercial-distributed.md) for `oceanbase`. Replace its seven resource placeholders with the independently calculated common values. Retain artifact identity, host-specific paths, ports, and zones from the reviewed deployment manifest; do not reconstruct the surrounding schema from memory or reuse volatile values from another cluster.

`Capacity(value, 0)` can round a byte result. Use the exact selected formatter and revalidate the rounded commitment, or emit exact integer-byte literals with the `B` suffix. Never round upward past a verified budget.

Build a filesystem commitment ledger. Charge `max(datafile_size, datafile_maxsize)` plus the 4 GiB slog reserve to the data filesystem, `log_disk_size` to the clog filesystem, and retained syslog to the home filesystem. `datafile_next` is already bounded by `datafile_maxsize` and is not a separate charge. Combine charges once when paths share a filesystem; never sum unrelated free-space figures or use one filesystem's surplus for another filesystem's deficit. After formatting every value, require each filesystem's combined commitments plus its explicit operational reserve to remain within that filesystem's current available blocks or quota; treat a violation as a pre-execution stop condition.

Keep `auto_create_tenant` absent or false. Add no OBProxy, OBAgent, monitoring, OCP, or other component unless explicitly requested and budgeted separately; the verified generator's Observer memory calculation does not automatically reserve every colocated component.

## Execute

Immediately before execution, repeat effective CPU/cgroup, `MemAvailable`, filesystems/quotas, competing processes, ports, path ownership, and mount identity. If any allowance decreased, workload appeared, or mount changed, stop and recompute all affected candidates and cluster minima.

Complete the configuration-deployment [host-environment remediation](config-deployment.md#host-environment-initialization) on every target before invoking `autodeploy`. Run the installed public precheck as the actual deployment user, apply the narrow owning remediation for each reported host or user-limit finding, reconnect when login limits changed, and prove the repeated precheck passes. Do not use broad `obd host init` for an isolated limit or kernel finding unless its complete path/permission change set is proved and authorized. Because `autodeploy` combines configuration generation, deployment initialization, and start, it must not be used as the first environment probe. Retain the reviewed `home_path`, `data_dir`, and `redo_dir` plus their canonical mount identities, owner, and mode before execution.

Inspect the final YAML and its checksum. Confirm all seven common values, the exact artifacts, the complete named-server-to-zone map, and that automatic tenant creation is absent. Apply the authorization rules from the shared operation contract, then use only syntax proved by installed help, commonly:

```bash
obd cluster autodeploy <deploy_name> \
  --config=<reviewed_config.yaml> \
  --generate-consistent-config \
  --strict-check
```

`autodeploy` is the OBD maximum-specification deployment command: it generates configuration from target-host resources, then deploys and starts the cluster. For a multi-node deployment, use the installed equivalent of `--generate-consistent-config` so every supported generated resource key is reduced to the minimum candidate across all target nodes. The preflight derivation is an expected bound and acceptance reference; the generated and registered configuration is the execution result, because the documented generator can overwrite resource fields from the input YAML.

Because the command is integrated, validate the source server names, sibling server sections, zone placement, paths, ports, artifacts, and every non-generated field before launch, then verify the generated configuration and exact server-to-zone map immediately after it returns. Do not replace `autodeploy` with separate `deploy` and `start` to create an inspection pause. If the invocation fails, reconcile its reached state through the configuration-deployment failure matrix before any next command; never rerun it blindly.

Do not pass an automatic-tenant option. An explicit tenant request starts only after Observer acceptance and follows [tenant management](../../tenant-management/SKILL.md) as a separate operation.

On failure, freeze retries and preserve the OBD trace, exact command, input checksum, registered/generated configuration, status, per-host processes/listeners/mounts/disk use, initialized paths, symlinks, and ownership. Classify the reached state before changing anything. Do not use `init4env`, force, cleanup, redeploy, path deletion, removal of generated custom storage values, manual creation of Observer-internal directories, or another deployment as generic recovery. Route an environment-check finding through [host environment initialization](environment-initialization.md) with an exact reviewed persistent diff; when initialization is necessary to the requested deployment, do not request duplicate confirmation solely because the diff persists. If the failure reached deployment initialization or start, also apply the [failed-initial-start and storage-topology recovery](../../references/failure-recovery-and-evidence.md#failed-initial-start-and-storage-topology).

## Verify

Do not report success from command exit alone. Apply the shared completion layers and verify:

1. The OBD task reached a successful terminal state and the exact artifact/configuration is registered.
2. Every expected Observer process and listener is present and owned by this deployment; no unrequested component or residual object exists.
3. The generated and registered configuration gives every node exactly the same seven resource values, and each equals the pre-deployment `cluster_value[key]` after byte normalization.
4. Configured `cpu_count` equals the selected generator's verified dedicated or capped formula.
5. Runtime process affinity and cgroup inheritance are recorded, every finite memory constraint fits the explicit memory cap, and no OOM event or unexplained competing workload invalidates the memory snapshot. On dedicated hosts, a generator-floor CPU result above effective CPU is not by itself an acceptance failure after strict startup and runtime health checks pass; retain that comparison only as internal diagnostic evidence.
6. Authenticated SQL proves the intended cluster identity and all servers are visible. When supported, compare runtime capacity through `oceanbase.GV$OB_SERVERS`.
7. `auto_create_tenant` remains absent or false, and no user tenant was created by this workflow. The `sys` tenant is expected.
8. Filesystem commitments, actual mount identities, paths, inodes, quotas, and retained OS/operational reserves remain valid after initialization.

Report host-level sizing separately from tenant resources. State the common values, identify which node limited each resource, and quantify surplus intentionally left on larger nodes. Do not include generator-floor details, CPU reserve arithmetic, or effective-to-configured CPU comparisons in the normal report; surface them only on an explicit diagnostic request or when they explain an observed startup or runtime failure.
