# Top-Level OBD Host Tools

Use this workflow only when the user requests the installed build's top-level `obd host` precheck, bare-host initialization, or host-user operation. These tools prepare or inspect a physical host; they are not a routine lifecycle step for an already managed cluster and are not interchangeable with deployment-scoped environment initialization.

- `host precheck` evaluates host-level prerequisites; it does not validate a deployment configuration.
- `host init` applies the installed build's host baseline and can persistently mutate the operating system.
- `host user init` prepares an operating-system account through the authentication modes exposed by that build. Do not use it merely to repair controller-to-node key authentication when the shared SSH workflow can preserve the existing account and append its public key directly.

## Resolve the Physical Hosts

Record the controller, target hostname and management address, stable machine identity, SSH user/port/key source, operating system, architecture, current accounts, live kernel/limit values, persistent configuration, and every existing OBD deployment on the host. Deduplicate aliases that identify the same physical machine.

Read the exact installed subcommand help and implementation. Some builds default omitted host or user arguments to localhost or the current user; never rely on those defaults for a remote or privileged operation.

Prefer an explicit SSH key or agent route. When password authentication is required, collect the value through a protected local input path, avoid displaying the command with the value, restrict terminal and trace access, and redact it from reports. Inspected development implementations can include the password in verbose connection failures; if that occurs, treat the affected output as sensitive and rotate the credential when exposure warrants it.

## Precheck

Treat a host precheck as read-only only after confirming the installed implementation and selected arguments. Preserve the exact checks, targets, non-secret output, and OBD identity; redact secret values without discarding the trace ID or failure context. A host-level pass does not prove that a particular deployment's packages, topology, paths, ports, resources, or component configuration are valid.

## Host Initialization

Host initialization can persistently change kernel parameters, limits, packages, services, directories, ownership, or permissions. Before execution:

1. do not use `host init` merely to fix an isolated `nofile`, `nproc`, `vm.max_map_count`, or similar precheck result when a narrower supported or documented remediation exists;
2. treat changes to existing data-path ownership or mode as a separate mutation, never as an implicit side effect of host preparation;
3. create byte-preserving backups of every existing configuration file the workflow can rewrite, then derive the exact per-host live and persistent diff from the installed workflow;
4. detect duplicate or conflicting entries and identify file ownership;
5. show reboot/reconnect and availability effects;
6. define itemized rollback to captured original values;
7. obtain authorization per unique physical host.

If the exact changes cannot be established, stop. Do not run initialization first and inspect afterward. Do not use it to bypass port/path overlap, architecture or package mismatch, insufficient resources, network failure, or an unknown process.

After initialization, rerun the same precheck and independently verify every requested change in both live and persistent state. Command success or a printed “success” is not proof that an item changed. In particular:

- verify MTU through the live interface and the active NetworkManager connection/profile or other actual persistence owner; a non-matching `sed` edit is no change;
- verify SELinux through both the live enforcement mode and persistent configuration, and report when a reboot is still required;
- verify required packages by the executable/package state, not by an installation suggestion in precheck output;
- verify limits in a newly established session when the setting is session-scoped.

Report any uncorrected warning as partial or failed according to its effect; do not convert it to PASS because `host init` exited successfully.

## Host User Operations

Resolve whether the operation creates or changes an account, group, home directory, sudo rule, SSH material, credential, or ownership. Read the installed command's supported SSH authentication and interaction modes before choosing it. Some builds require password authentication and a real PTY even when `host precheck` accepts a key. On a key-only host, report that limitation; do not enable SSH password authentication, set or rotate a root password, or weaken the host policy merely to make `host user init` run.

Preserve existing access and obtain authorization for the exact account and paths. Do not grant passwordless sudo, replace authorized keys, rotate credentials, or recursively change ownership unless explicitly included. Drive required password prompts through a real PTY and a protected input path; ordinary pipe input is not evidence that the command can run non-interactively.

After any mutation, compare live and persistent state with the approved diff, verify the intended SSH/privilege path, and confirm unrelated users and deployments remain functional. Restore item by item; never use broad account, sudoers, limits, or sysctl cleanup.
