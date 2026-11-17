# Component Changes

Use this workflow for OBD component add/delete. A registered component is not accepted until its runtime and product data plane recognize it.

Adding or removing Observer servers from an already registered deployment is unsupported. Report `UNSUPPORTED` before mutation and do not reinterpret a node-topology request as component addition/deletion.

## Capability and Dependency Gate

1. Record the installed OBD build and selected subcommand help, deployment/product form, component plugins, repositories, status, topology, and real runtime state.
2. Derive the dependency graph and supported component transitions from the registered configuration and installed workflows. Do not transfer a dependency order from a different product form or release.
3. Build an explicit incremental manifest: selected component and target servers, versions/releases/hashes, paths, ports, resources, network identity, and dependencies.
4. Check package compatibility and exact artifact availability. A component must not silently resolve a different release from the reviewed artifact.
5. Check target host identity, SSH, OS/runtime, canonical paths, ports, capacity, time/network, and overlap using the deployment preflight.
6. Identify application, tenant, OCP, monitoring, and Config Server dependencies and the availability impact.

Do not add a component simply because it appears in an example, bundle, or repository. Do not convert an incremental request into a replacement full configuration or redeploy.

## Add a Component

Build a schema-validated incremental config containing only the requested component and required fields. Use the installed syntax, commonly:

```bash
obd cluster component add <deploy_name> --config=<incremental_config.yaml>
```

For monitoring read [monitoring.md](monitoring.md); for OCP or Config Server, read its dedicated reference. Verify the component exactly once in registered state, actual process/listener/path ownership, dependency integration, its own health/API, and a representative consumer path.

Inspect the exact semantics of any `--confirm`-like option before using it. In inspected OBD code, `component add --confirm` skips the prompt and immediately invokes restart. Adding Config Server when OBProxy already exists builds a selector containing OBProxy plus the existing OceanBase database component; adding it without OBProxy leaves the selector empty and can expand to a whole-deployment restart. Other component additions can reach the same empty-selector full-restart branch. Never use this flag merely to make automation non-interactive. Display the exact restart set first, or omit the flag and stop if the prompt cannot be handled safely.

If no safe incremental-add path exists, stop and present the limitation. Do not substitute redeploy or manual `.obd` metadata edits.

## Delete a Component

Before deletion, derive all dependants and consumers and identify retained data/configuration. Show the exact component/servers, availability effect, residual paths, and recovery boundary, then obtain destructive authorization for that exact deletion.

Use only the installed command form. Remove dependants or migrate consumers in the derived order; do not assume one fixed monitoring deletion order across versions. After deletion, prove registered configuration, processes, listeners, dependency references, client/management paths, and separately owned data match the approved result.

Treat registration removal and runtime removal as separate required outcomes. Before invocation, capture the selected component's entries in `config.yaml` and `inner_config.yaml`, reverse dependency references, artifact identity, process executable/PID, listeners, canonical home/work/data paths, and representative consumer health. Afterward verify that both configuration files and OBD registration contain exactly the intended retained state, no live dependency points to the deleted component, its processes/listeners are absent when deletion promises to stop it, and every work/data path matches the approved remove-or-retain set. Correlate the Trace with the expected `delete_component_pre` and `delete_component` stages when the installed component exposes them.

A successful `component del` exit with removed registration but a live process, listener, stale inner configuration, or unexecuted required deletion workflow is a lifecycle gap. Report the operation or test as `FAIL`, not `PASS`; preserve the residual state and do not kill the process or delete its directory without a separately reviewed recovery action.

The established command surface commonly uses:

```bash
obd cluster component del <deploy_name> <component_name> [version-supported selectors]
```

Do not turn the placeholder into an executable command until the exact component, dependants, retained paths/data, and installed selector syntax have passed the gate above.

## Partial Failure

On failure, freeze retries and record the trace, incremental config, registered before/after state, artifact installs, real processes/listeners, product topology, and dependency health. Do not remove a partially installed component, delete its directories, rerun with force, or redeploy until the observed stage proves the recovery action safe.
