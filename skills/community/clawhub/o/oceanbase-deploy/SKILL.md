---
name: oceanbase-deploy
description: Route community and commercial distributed OceanBase deployment and operations through obd. Use for general or multi-domain OceanBase/obd requests, product-form discovery, or when the correct specialized skill is unclear. Route concrete work to cluster management, OBD administration, tenant management, testing, or diagnostics.
metadata:
  author: oceanbase
  version: "2.0.3"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-deploy-operations-obd"></a>
<a id="oceanbase-deploy--operations-obd"></a>
<a id="skill-index"></a>
<a id="quick-start"></a>
<a id="installation"></a>
<a id="ocp-terminology-convention"></a>
<a id="critical-safety-rules"></a>

# OceanBase Deployment and Operations with obd

Use this entry point to identify the product form, execution mode, and owning skill. Do not turn an explanation, configuration review, or diagnostic request into a deployment.

## Community and Commercial Distributed Parity

Treat `oceanbase-ce` and `oceanbase` as different artifact identities in the same OBD-managed distributed operating family. Unless the installed public help/schema/plugin or version-matched official documentation explicitly proves a difference, apply the same distributed configuration structure, preflight, environment initialization, deployment, lifecycle, tenant, component, monitoring, upgrade, failure-recovery, and acceptance workflows to both. An example that happens to use `oceanbase-ce` is not evidence that the OBD capability is community-only.

Keep only proved differences separate: exact component/package names and dependency closure, artifact distribution channels and entitlement, compatibility modes or licensed features actually exposed by the selected product, and exact source/target package compatibility. Do not create an edition restriction from the product label alone.

## Mandatory Package Acquisition Order

Apply this rule before any online lookup or request for every package carried by the OceanBase public repositories, including OBD, database and proxy components, companion libraries, clients, test tools, and diagnostic tools. Select the **effective artifact source first**; only then select a download mechanism.

For each exact package candidate, use these effective artifact sources in order: (1) the actual package directories under `https://mirrors.oceanbase.com`, then (2) the actual package directories under `https://mirrors.aliyun.com/oceanbase`. The first actual OceanBase package request must target source 1. Keep the same source through three meaningful acquisition attempts before moving to source 2; after both sources are exhausted, move from the target-OS suffix to EL8 and then EL7 when that package family publishes EL suffixes. A generic connectivity test cannot replace or precede the first source-1 request.

A package-manager `.repo` file is only repository configuration, not a package source or package download. Count the effective base URL or final candidate URL that serves the package bytes, not the host that served the `.repo` file. Before using a repository definition or counting a package-manager attempt, resolve and record that effective URL and confirm that it belongs to the current source. Operating-system dependency repositories such as Rocky BaseOS/AppStream are a separate channel: changing one neither counts as an OceanBase source attempt nor changes this order, and must not be hidden in the same opaque command as OceanBase acquisition.

Within the current source, use applicable controller-local mechanisms such as a version-supported OBD/tool path, direct `curl` or `wget`, or the operating-system package manager. `obd mirror` imports or indexes an artifact that is already local; never use it as a network downloader. Read the detailed [fixed package-source workflow](obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) before the first package network request.

**OBD bootstrap:** the controller package is `ob-deploy`; Community and Commercial OceanBase deployments use the same OBD package from the public `community` tree. When OBD is absent and no verified controller-local RPM already exists, start under `https://mirrors.oceanbase.com/community/`, default to downloading the exact RPM on the selected controller with `curl` or `wget`, and install that local RPM with the operating-system package manager. A request to execute an OBD-dependent deployment authorizes this proved first installation and the package manager's ordinary non-interactive acceptance option such as `-y`; do not ask for separate permission to run the install command. This exception does not authorize OBD replacement, upgrade, downgrade, an unproved package candidate, or broad repository changes. Do not add a persistent OceanBase `.repo` merely as the default way to bootstrap OBD. Use a repository definition only when its effective package URL is proved to follow the current source order.

**Other packages:** default online mode lets the installed OBD/repository or owning tool workflow resolve and fetch the proved winners. When direct controller-local download or an approved relay succeeds, follow the artifact's actual consumer path: import OBD component RPMs with `obd mirror clone` and isolate the complete local closure; use the version-proved local registration or installation path for clients, test tools, diagnostic tools, images, and non-RPM artifacts; install operating-system dependencies only on the machine that consumes them. Do not turn every downloaded package into a package-manager installation on every cluster node.

## Default Controller, SSH, and Existing-State Discovery

For every OBD-based cluster deployment mode, including configuration-file, interactive, autodeploy, demo, and perf paths, keep the controller on a cluster deployment host unless the user explicitly selected a separate controller. Probe the user-supplied target hosts in their original order before choosing or installing OBD. Reuse the target host that owns the intended registered deployment, or an otherwise unambiguous existing target-host controller. Only after every target host is reachable and confirmed to have no OBD executable, package ownership, or controller metadata, install OBD on the first target host with non-interactive package-manager acceptance and without asking the user to choose or approve the install command. Never default to installing or running OBD on the automation runner.

Use the user's supplied SSH login user for every deployment machine; if no login user is specified, use `root`. If no authentication material is supplied, use passwordless SSH. After login, keep that login-session user as the identity for all subsequent work: inspect and prepare hosts, install and run OBD, own controller metadata and files, and connect from the controller to the same login user on every other node. Do not derive or switch to a second OBD execution user. If controller-to-node passwordless authentication fails but the runner already has verified access to the exact target, directly append the controller login user's public key to that same login user's `authorized_keys`, preserve existing entries and permissions, and verify `BatchMode` access without another prompt. Use narrowly scoped privilege escalation only for commands that require it; it must not change the OBD/controller owner. Never copy a private key, replace `authorized_keys`, alter passwords or `sshd_config`, bypass a host-key mismatch, or use a tunnel. Ask for access only when no already-approved path can modify the exact target or its identity remains ambiguous.

Do not ask the user whether a cluster is already deployed. Determine that through read-only inspection of candidate-controller registrations and, on every target host, relevant package/service state, processes, listeners, deployment paths, and database identity when reachable. A missing registration or stopped process alone does not prove absence. Ask only when access failed or the completed inspection leaves a genuine identity or ownership ambiguity. Follow the detailed [controller, SSH, and cluster discovery contract](references/operation-contract.md#default-controller-ssh-and-cluster-discovery).

## Default New-Deployment Directory

For a new deployment, when the user does not specify deployment or storage paths, select the default separately on every target under the established login-session user. Use the persistent mounted filesystem with the greatest usable free capacity for which that user can actually read, write, and traverse a safe parent directory, then create a new deployment-specific base beneath it. Place the component home, data, redo, log, and other deployment-owned subdirectories beneath that base as the installed schema permits. Do not default to the user's home while a larger writable persistent filesystem exists, and do not assume a path such as `/data/1` without inspecting the host. Explicit user paths override this default; existing registered paths are immutable unless the user requests a supported path-migration workflow. Follow the detailed [default deployment-directory selection](cluster-management/references/config-deployment.md#default-deployment-base-directory).

## Default New-Cluster Sizing

For a new OceanBase cluster deployment, when the user does not specify resource values, a resource cap, or a non-maximum sizing profile, default to the [maximum-utilization workflow](cluster-management/references/maximum-utilization.md) without asking the user to choose a size. For a distributed maximum deployment, `obd cluster autodeploy` is the default execution path; do not require the user to name that command and do not replace it with separate `deploy` and `start` merely because those stages are easier to inspect. Explicit user values or caps take precedence. This default maximizes only the resolved target hosts; it does not add hosts, components, tenants, or topology that the user did not request.

For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order. Do not ask the user to choose the default placement. Preserve an explicit zone mapping, do not infer extra hosts or replicas, and do not claim that logical zones sharing one physical failure domain provide high availability.

## Deployment Package Closure

Before the first package lookup or acquisition for any deployment, component addition, upgrade, or reinstall, read the shared [deployment package closure](references/deployment-package-sets.md). Build the complete package set from the final requested component graph, including selected `*-libs`, JRE, client-library, image, and conditional utility dependencies; do not stop after downloading the obvious primary component RPM. Before a cluster deployment, also prove a compatible controller-side SQL client and add `obclient` + matching `libobclient` to the pre-deployment closure when none exists. In online mode prove every closure entry is resolvable; in local-package/offline mode place and verify the complete closure on the selected remote controller, plus every required node-local image, before package selection.

## Commercial Package Boundary and Platform Fallback

The mandatory public-source order above applies only to artifacts published in OceanBase public/community repositories. For commercial database/component and standalone/centralized artifacts, first inspect the selected controller's OBD local repository for the exact complete closure. If any required package is absent, stop and ask the user to provide the exact files or an existing accessible path. Never probe community mirrors, sign in to a portal, contact support, or automatically download those artifacts. Read the detailed [commercial package-acquisition workflow](obd-administration/references/mirror-and-repositories.md#commercial-package-acquisition).

Keep source channel and platform fallback independent. For every RPM-like OBD-managed artifact, public or commercial, try the exact target-OS suffix, then EL8, then EL7 while preserving component/version/release/architecture and proving runtime compatibility. For a commercial or standalone/centralized artifact, this order identifies the exact files to request from the user; it does not authorize downloading them. The edition-neutral `ob-deploy` package is the explicit exception: it always follows the public `community` path described above.
## Default Database Bootstrap Password

For a new OceanBase cluster deployment, do not ask the user to choose the initial database `root`/`sys` password unless the user has already specified one. When no override was supplied, leave the bootstrap-password field absent and use the installed OBD workflow's proved random-password generation path; do not generate the value in the agent or substitute an empty value. Keep the generated value protected and verify authentication without printing it. Read the cluster workflow's [database bootstrap-password default](cluster-management/references/config-deployment.md#database-bootstrap-password-default) before rendering deployment YAML.

## Route the Request

| Skill | Use when |
|---|---|
| [cluster-management](cluster-management/SKILL.md) | Deploy or operate community or commercial distributed OceanBase clusters and OBD-managed components; manage configuration, upgrades, lifecycle, monitoring, OCP, Config Server, and network access. |
| [obd-administration](obd-administration/SKILL.md) | Install or update the OBD controller; manage mirrors/repositories, stored credentials, dynamic tools, OBD Web/API, top-level host commands, trace evidence, runtime environment, or telemetry. |
| [tenant-management](tenant-management/SKILL.md) | Create, inspect, optimize, back up, restore, drop, or manage physical primary/standby tenants. |
| [testing-and-benchmark](testing-and-benchmark/SKILL.md) | Run Sysbench, TPC-H, TPC-C, or mysqltest through `obd test`. |
| [obdiag-diagnostics](obdiag-diagnostics/SKILL.md) | Install-gated diagnostic collection, analysis, checks, scenes, or RCA through `obd obdiag`. |

Once the request resolves to one child skill, continue with that child and only the references selected by its routing table. Do not load sibling skills or reread the parent as an operational checklist unless the request actually spans multiple domains or new evidence makes the original route ambiguous. Shared package-source and safety summaries remain intentionally visible in directly invocable children; their linked shared references are the canonical detailed procedures.

## Resolve Product and Capability First

Before proposing an executable command or configuration, read [product and capability resolution](references/product-and-capability-resolution.md). Support community and commercial distributed deployments through the common operating model above, while resolving the actual component keys, packages, repositories, artifacts, and any proved feature difference before rendering a configuration.

Do not:

- default to a community component or public mirror when the request or artifacts indicate a commercial deployment;
- treat a source-tree feature as proof that the installed OBD package exposes it;
- substitute OCP CE, enterprise OCP, or obshell Dashboard for one another;
- infer compatibility only because every requested package exists in a repository.

## Preserve the User's Execution Mode

- **Explain, plan, review, or audit:** stay read-only. Inspect only the supplied files and already available local evidence unless the user expands the scope.
- **Diagnose:** begin with the smallest relevant read-only evidence set. High-overhead collection or tool installation is a separate action.
- **Implement:** display the resolved targets, mutations, impact, and acceptance plan before execution. Obtain authorization at the point required by the risk class.

Read the shared [operation contract](references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/API/network access, download, write, or other externally visible action. A child skill can be selected directly, so every child in the routing table must also link this contract and retain its essential safety boundary.

## Define Completion and Failure Handling

Command exit, task acceptance, process state, control-plane state, and data-plane usability are different results.

- Read [completion criteria](references/completion-criteria.md) before declaring an operation complete.
- On failure, timeout, interruption, or a mixed state, read [failure recovery and evidence](references/failure-recovery-and-evidence.md) before retrying or cleaning anything.
- Before any cleanup, removal, reset, prune, drop, uninstall, or deletion, read [cleanup and ownership boundaries](references/cleanup-boundaries.md) and enumerate the exact removed and retained objects.

Never use `redeploy`, `destroy`, `--force`, metadata deletion, repository cleanup, tenant drop, or another broad mutation as a generic repair.

## Quick Start Boundary

Do not expose an unconditional `obd demo` or `obd perf` command as the default quick start. For a quick local deployment, route to the cluster skill and use its reviewed configuration workflow. If the user explicitly selects either shortcut, inspect its fixed deployment name, generated components, paths, ports, existing processes, implicit force/cleanup behavior, and recovery boundary first.

## Sensitive Values

Do not place passwords, passkeys, access keys, tokens, private keys, or credential-bearing URIs in reusable examples, chat output, process arguments when a protected input exists, or reports. Redact secrets without discarding the non-sensitive evidence needed to reproduce a failure.
