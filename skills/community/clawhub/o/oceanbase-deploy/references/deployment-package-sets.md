# Deployment Package Closure

Read this reference before the first package lookup, download, mirror import, or bundle import for a new deployment, `autodeploy`, an explicitly selected `demo`/`perf` run, component addition, upgrade, or reinstall. Build the package closure from the final requested component manifest before acquiring the first artifact. The obvious primary package alone is not a complete closure.

The names below are a maintained planning baseline, not permission to deploy every listed component. Select only the rows required by the requested topology. Confirm every component key, package name, version constraint, dependency, and alias against the installed OBD plugin and repository before execution.

## Keep Four Artifact Classes Separate

1. **Controller package:** `ob-deploy`, installed on the selected OBD controller, or supplied by an owning OceanBase/OCP All-in-One bundle.
2. **OBD component artifact:** the RPM, archive, or repository object that implements a selected YAML component, such as `oceanbase-ce`, `obproxy-ce`, or `prometheus`.
3. **Companion runtime artifact:** a package selected through the component's requirement map, such as `oceanbase-ce-libs`, `openjdk-jre`, or `libobclient`. It may not have its own YAML stanza but is still part of a deterministic local/offline closure.
4. **External prerequisite:** `clockdiff`, an existing MetaDB, object storage, or a system library supplied outside the OBD component repository. Record and verify it separately; do not pretend it is an OBD package.

An artifact already present with the exact reviewed identity can satisfy the closure; do not download it again merely to follow this list. A running dependency does not prove that its package is available to a later package-selecting workflow, and a package in the controller repository does not prove that the corresponding service is running.

`ob-deploy` is the same public controller package for community and commercial deployments. Resolve it from `https://mirrors.oceanbase.com/community/` first; it is never part of the commercial database/component entitlement set.

## Keep Distribution Channel and Platform Suffix Separate

Artifact edition decides **where** a package may be acquired; target compatibility decides **which platform build** may run. Do not merge those decisions:

- public/controller/community artifacts use the fixed public mirror order;
- commercial database/component and standalone/centralized artifacts must already exist as an exact complete closure in the controller's OBD local repository or be supplied by the user; never download them automatically;
- every RPM-like artifact in either channel uses the same candidate order: exact target operating-system suffix, then EL8, then EL7, while preserving product/component/version/release/architecture;
- every fallback remains a candidate until its RPM requirements, loader, GLIBC, libraries/symbols, package-manager behavior, installation, and startup compatibility are proved on the target.

An EL8 or EL7 commercial candidate does not become a community artifact, and a public mirror miss is not evidence that an entitled commercial build does not exist.

## Expand Database Components First

For a controller-local or air-gapped repository, stage both the selected database package and its matching companion library package. For online resolution, prove both are available for the selected version, release family, architecture, and platform candidate even when OBD may skip downloading or installing the companion because the target host already satisfies `ldd`.

| Selected database component | Package closure |
|---|---|
| Community distributed OceanBase, normally `oceanbase-ce` | `oceanbase-ce` + matching `oceanbase-ce-libs` |
| Commercial distributed OceanBase, normally `oceanbase` | `oceanbase` + matching `oceanbase-libs` |

`*-utils` packages are not ordinary database-start prerequisites. Add `oceanbase-ce-utils` only when `install_utils` is selected, an OCP check/export workflow needs it, or the installed workflow explicitly declares it. Add `oceanbase-utils` or another commercial utility only when the selected commercial workflow or OCP software-catalog plan proves that exact requirement. Never invent a `-utils` package by analogy.

For ARM hosts without LSE support, select the documented `nonlse` OceanBase database variant when the chosen version requires it. OceanBase All-in-One does not supply that variant. Keep its companion closure and architecture consistent with the selected package.

## Distributed Database, Proxy, and Monitoring Sets

The following sets describe deployment payloads after the controller itself is available:

| Requested outcome | Required package set |
|---|---|
| Community OceanBase only | `oceanbase-ce`, `oceanbase-ce-libs` |
| Community OceanBase with ODP/OBProxy | Community database closure + `obproxy-ce` |
| OBD V4.6.0 documented default `demo`/`perf` component set | Community database closure + `obproxy-ce` + `obagent` + `prometheus` + `grafana` |
| Metrics collection without Grafana | Selected database closure + `obagent` + `prometheus` |
| Metrics collection with Grafana | Previous row + `grafana` |
| Commercial database with ODP | Selected commercial database closure + `obproxy` |

For component addition to an existing healthy deployment, acquire only the newly selected packages and their companion closure; prove the already deployed dependencies through registration and runtime evidence instead of downloading or redeploying them. Community ODP releases before the documented rename can use `obproxy` rather than `obproxy-ce`; preserve the exact installed-version package name instead of renaming it mechanically.

## Config Server Sets

| Requested outcome | Required package set |
|---|---|
| Config Server only | `ob-configserver` |
| Community OceanBase + ODP + Config Server | Community database closure + `obproxy-ce` + `ob-configserver` |

## OCP Sets

The official V4.6.0 workflow recommends the matching `ocp-all-in-one-*.tar.gz`. Its installer installs OBD, imports the bundle's RPMs into the controller-local repository, and disables remote repositories. Inventory the imported package identities and repository state after installation; the bundle name alone is not proof that the requested version, edition, architecture, or full catalog is present.

When individual artifacts are used, expand the runtime closure as follows:

| Requested outcome | Required package set |
|---|---|
| OCP Community Edition with an existing external MetaDB | `ocp-server-ce` + the exact `openjdk-jre` selected by its installed requirement map |
| Commercial OCP with an existing external MetaDB | `ocp-server` + the exact `openjdk-jre` selected by its installed requirement map |
| OCP CE with a same-deployment MetaDB and ODP | OCP CE runtime closure + community database closure + `obproxy-ce` |
| Commercial OCP with a same-deployment database and ODP | Commercial OCP runtime closure + the selected commercial database closure + `obproxy` |

The OCP server's own runtime closure is different from the software catalog OCP later uses to manage or deploy OceanBase. If that management capability is in scope, seed and verify the catalog separately:

- Community catalog candidates: `ocp-agent-ce` for every managed architecture, `oceanbase-ce`, `oceanbase-ce-libs`, `oceanbase-ce-utils`, and `obproxy-ce` for the versions OCP is expected to manage.
- Commercial catalog candidates: `ocp-agent`, `oceanbase`, `oceanbase-libs`, `oceanbase-utils`, and `obproxy`, limited to the approved products, versions, and architectures.

Catalog packages are conditional management content, not permission to deploy those products and not a reason to import every repository version. OCP takeover/export can also require `oceanbase-ce-utils` on the source Observer hosts; include that mutation and package identity in the operation plan.

## Controller-Side SQL Acceptance Tools

The official V4.6.0 command-line deployment workflow expects an OBClient-compatible SQL client for verification, and OceanBase All-in-One installs OBClient. Before the first deployment mutation, inventory the selected controller for a compatible SQL client whenever authenticated SQL is part of acceptance. If none exists, add and acquire the controller-side client closure before deployment rather than discovering the gap after startup. When OBD supplies that tool, the closure is `obclient` + matching `libobclient`; an already approved compatible SQL client can satisfy the need when its exact executable/version and target protocol are proved.

Do not treat OBD's private Python or an unverified `mysql.connector` import as the SQL client plan, and do not confuse this operator tool with a cluster component. If no compatible client or complete client closure can be obtained, report the acceptance prerequisite before mutating the cluster.

## Resolve and Acquire Every Closure Entry

Keep the package consumer explicit. Install only the verified `ob-deploy` controller RPM directly through the controller's operating-system package manager. Let OBD consume component RPMs: online mode resolves and fetches the proved remote winners through the owning OBD/repository workflow; local-package mode imports already-downloaded controller-local component RPMs with `obd mirror clone` and then runs that same OBD workflow. Install operating-system dependencies through the package manager on the machine that consumes them, and use the version-proved registration or installation path for non-RPM tools and images. Do not turn every downloaded RPM into a package-manager installation on every cluster node.

1. Freeze the requested topology or operation and list every selected YAML component, companion requirement, conditional package, test or diagnostic tool, current/target/rollback artifact, external prerequisite, and already-satisfied dependency.
2. For each RPM-like artifact in either edition/channel, preserve product form, component name, version, release, architecture, and hash. Apply the target-system suffix first, then EL8, then EL7 only when the preceding candidate does not exist and runtime compatibility is verified. Do not apply an EL suffix to an image/archive that does not use one.
3. Classify each candidate by distribution channel independently of step 2. For a public/community artifact, use the shared fixed source order: `mirrors.oceanbase.com`, then the direct package directory under `mirrors.aliyun.com/oceanbase`, with the defined three attempts per source before advancing. After normal OBD/repository fetching fails, vary those attempts with controller-local `curl`, `wget`, the package manager, or another applicable downloader; use the bounded artifact relay only after controller-local methods are exhausted. For a commercial (Enterprise Edition) database/component or standalone/centralized artifact, inspect only the selected controller's OBD local repository. If an exact required entry is absent, ask the user for that file or its existing path; do not query a network source or relay. The same EL8/EL7 fallback order identifies compatible candidates but never authorizes automatic download.
4. In **online mode**, prove a unique remote candidate and its effective artifact URL for every required public/community closure entry before the package-selecting operation. OBD may fetch only those public/community artifacts during the owning workflow when the effective URL follows the required source order; pre-downloading them into the local repository is not required. Commercial and standalone/centralized entries must already be local or user-supplied and must not remain remote winners. If one public mechanism fails, keep the current source while trying another applicable controller-local OBD/tool, `curl`, `wget`, or package-manager path. If an explicit public download or bounded checksummed relay obtains the artifact, transition the complete public closure to local-package mode rather than mixing local and unresolved remote winners.
5. In **local-package/offline mode**, acquire, verify, and import every required RPM closure entry on the selected remote controller before disabling participating remote repositories. Re-list the local repository inventory after import.
6. Treat an All-in-One bundle as a transport for a tested package set, not as evidence by name. Bundle contents vary by product series, and the V4.6.0 OceanBase All-in-One baseline does not include the ARM `nonlse` database variant. Inventory the actual bundle and add every missing selected artifact explicitly.
7. Before execution, compare the final closure manifest with the rendered component graph and the exact candidates OBD will use. A missing required entry is an incomplete package plan; an unrequested package in a bundle is inventory only and must not become a YAML component implicitly.
8. Restore any temporary remote-repository state after the final package-selecting stage unless persistent local-only behavior was explicitly requested.

Use a closure record with at least:

```text
purpose, yaml_component, artifact_name, requirement_class,
version_or_tag, release, os_suffix, architecture, hash_or_digest,
source, controller_or_node_location, resolution_state
```

On deployment output, reconcile OBD's displayed package table, subsequent companion-package resolution, and actual installed artifacts with this record. Some companion libraries are resolved only after target runtime inspection, so absence from the first displayed primary-component table does not prove they were unnecessary; verify the final runtime and package evidence.

## Evidence Basis

The package topology and bundle behavior above were established first from the official **OceanBase Installation and Deployment Tool V4.6.0** documentation for controller/All-in-One installation, distributed OceanBase deployment, OCP, Config Server, monitoring, and SQL acceptance tooling.

Where those documents do not enumerate an internal companion package, the closure is filled only from the declaration-oriented requirement maps and released examples in the pinned `ob-deploy` checkout described by the [source-evidence boundary](source-baselines.md#source-evidence-boundary): database `*-libs`, OCP `openjdk-jre`, OBClient `libobclient`, and the optional OCP software-catalog candidates. Those source observations do not map the checkout to an OBD RPM release. The installed plugin, package metadata, public help/schema, and selected repository remain runtime authority.
