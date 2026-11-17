# Mirrors and Repositories

Use this workflow to inspect or change OBD mirror sections, local repository artifacts, remote repository definitions, and package candidates.

When acquisition serves a deployment, component addition, upgrade, or reinstall, first build the full [deployment package closure](../../references/deployment-package-sets.md). Apply mirror and operating-system candidate resolution to every required closure entry; do not begin with one obvious component and discover its companion libraries, JRE, client library, or node-local image only after deployment has started.

## Keep the Layers Distinct

- An **effective artifact source** is the base URL or final candidate URL that serves the package bytes.
- A package-manager **repository definition** such as an `OceanBase.repo` file is configuration containing fields such as `baseurl`, `mirrorlist`, enabled state, and trust settings. The host serving that small configuration file is not necessarily the effective artifact source.
- An **acquisition mechanism** is the path used to resolve or transfer an artifact, such as an installed OBD/tool workflow, `curl`, `wget`, or the operating-system package manager. Mechanism choice never changes source priority.
- An OBD **mirror section** describes a local or remote source and its enabled/available state.
- The **local repository** contains artifacts OBD can select, identified by component, version, release, architecture, hash, tags, and source.
- A **compatible package set** is a reviewed selection for one product form and workflow. Mirror visibility or repository presence alone does not prove compatibility.
- An **operating-system dependency repository** such as Rocky BaseOS or AppStream is separate from the OceanBase artifact sources. Changing or probing it does not count as an OceanBase source attempt and does not change the order below.

Always choose and prove the effective artifact source before choosing the acquisition mechanism. Do not use “repository” as shorthand for both concepts.

Read the installed `obd mirror` and `obd repo` help before constructing commands; available subcommands and argument forms vary by OBD build.

## OBD Controller Package Is Edition-Neutral

`ob-deploy` does not have separate community and commercial editions. Community and commercial distributed deployments use the same public OBD controller package. Always classify `ob-deploy` as a public controller artifact and use `https://mirrors.oceanbase.com/community/` as its first and normal download location. If that source is exhausted, retain the public-package fallback order below; never switch `ob-deploy` to the commercial acquisition workflow or ask the user for a commercial OBD package merely because the target database is commercial.

## Commercial Package Acquisition

OceanBase community repositories do not provide commercial (Enterprise Edition) database or component artifacts. The Skill must not automatically download commercial distributed or standalone/centralized artifacts from a portal, software center, support channel, private repository, community mirror, or another network source. This boundary does not include the edition-neutral public `ob-deploy` controller package.

First inspect the selected controller's OBD local repository for the exact complete commercial package closure. Use it only when every required component, companion package, version, release, operating-system suffix, architecture, and reviewed hash is present and compatible. If any entry is missing, stop before a package-selecting or deployment command and ask the user to provide the exact missing files or an existing accessible path. Do not sign in to a portal, contact support, search another host, or download on the user's behalf.

Use the same RPM platform-candidate order to identify what the user must provide: exact target-system suffix, then EL8, then EL7, while preserving component/version/release/architecture and proving runtime compatibility. Suffix fallback never authorizes automatic acquisition, a switch to a community repository, or a different product form. After the user supplies the files, verify provenance, access/license boundary, product form, version, release, architecture, operating-system compatibility, checksum, and dependency closure; transfer them to the selected controller when necessary, verify them again there, and import/register them through the version-supported local path.

The same no-automatic-download boundary applies when reviewing a standalone/centralized request. It does not make an otherwise unsupported product workflow executable.

## Fixed Online Package Source Order

For every public/community package carried by the OceanBase public repositories, use these mirror sources in exactly this order:

1. `https://mirrors.oceanbase.com`
2. the direct package directories under `https://mirrors.aliyun.com/oceanbase`

For `ob-deploy`, source 1 resolves under `https://mirrors.oceanbase.com/community/` regardless of whether the database deployment is community or commercial. Preserve its exact version, release, architecture, and operating-system suffix while resolving the package beneath that tree.

The second source means its actual `community/stable`, `development-kit`, or other proved package directory. Merely downloading or registering `https://mirrors.aliyun.com/oceanbase/OceanBase.repo` is not a package acquisition attempt and does not prove use of source 2. Inspect the definition and the package manager's resolved candidate location: if its effective `baseurl` or final package URL points to `mirrors.oceanbase.com`, the package still comes from source 1. Record the effective artifact URL, not the repository-definition download host.

Build operating-system candidates in the shared exact-suffix, EL8, then EL7 order. For each candidate suffix, walk the two mirror sources above in order. One attempt is one complete source-specific pass to resolve and acquire the same exact component/version/release/suffix/architecture, including source metadata and the exact package object when resolved; individual HTTP subrequests are not separate attempts. The first OceanBase package network action must be an actual attempt against source 1. A ping, generic public-Internet test, unrelated website request, DNS-only check, proxy inspection, operating-system repository change, or `.repo`-definition download does not count and cannot gate that first attempt. Across attempts on one source, do not blindly repeat only the same failed mechanism: while keeping the effective package URL on that source, vary applicable controller-local mechanisms among direct `curl` or `wget`, a package-manager resolve/fetch with proved effective URL, and an installed OBD/tool acquisition path when one exists.

Keep the same mirror source until that exact acquisition has failed three times, recording attempts 1, 2, and 3. After the third failure, move to the next mirror source. After source 2 has also failed three times, move to the next compatible suffix. Stop immediately when the artifact is acquired and its identity and checksum are verified. If every compatible suffix, both mirror sources, and all applicable controller-local download methods are exhausted, use another reachable host only as a bounded artifact relay for the same exact package from the same ordered sources. Verify the artifact on the relay, transfer it to the existing controller, and verify it again there; do not install or run OBD on the relay or change controller identity. Ask the user only if the relay also cannot acquire or transfer the exact artifact, an unlisted source is required, or artifact identity or compatibility remains unresolved.

### OBD Bootstrap Emphasis

The OBD controller RPM is `ob-deploy`. Community and Commercial OceanBase deployments use the same OBD package from the public `community` tree; do not search a commercial software channel for a different OBD build merely because the target database package is Commercial. On a clean controller with no verified local OBD RPM, the first package request must begin under `https://mirrors.oceanbase.com/community/`. Default to resolving and downloading the exact RPM there with controller-local `curl` or `wget`, then install that local RPM through the operating-system package manager. A repository definition is an allowed mechanism only when its effective package URL is proved to follow the current source order; do not add a persistent OceanBase `.repo` merely as the default bootstrap method.

### How OBD-Managed Component Packages Are Consumed

Treat `ob-deploy` differently from the packages it manages. Install the verified `ob-deploy` RPM directly on the selected controller. For Observer, companion libraries, OBProxy, monitoring, Config Server, and other OBD-consumed component RPMs:

- in online mode, let the installed OBD/repository workflow resolve and fetch the exact proved remote winner, then let the owning OBD command distribute and install it on the target hosts;
- after an explicit controller-local download or bounded relay succeeds, verify and import every RPM in the complete closure with `obd mirror clone <path>`, isolate local resolution as described below, and run the same owning OBD workflow;
- do not install component RPMs independently with the target operating-system package manager unless the installed component/plugin explicitly defines that as its consumer path.

Operating-system runtime dependencies remain a separate channel and are installed on the machine that actually consumes them. Non-RPM tools, archives, and images use only their version-proved local registration, extraction, image-load, or installation path; `mirror clone` is not a universal importer.

### Release-Suffix Fallback Without Hidden Repository Edits

When a remote repository definition substitutes the controller's current `$releasever` and that suffix has no candidate, keep the shared target-suffix, EL8, then EL7 order but do not rewrite `$releasever` inside `OBD_HOME`, edit files under `OBD_HOME/mirror/remote`, or fabricate a local file/directory URL for `obd mirror add-repo`. Directly resolve and download the exact fallback-suffix RPM closure from the fixed sources to the selected controller, verify every artifact and runtime dependency, import each OBD-consumed RPM into the local repository, disable participating remote sections for the local-selection window, and run the owning OBD workflow against the proved local winners. This changes package-resolution mode, not controller identity or target operating-system identity.

### Remote Download Command Boundary

After selecting the current effective artifact source, use an applicable controller-local mechanism to fetch the proved exact package. If one mechanism fails, keep the same source and try another applicable mechanism before changing sources or acquisition hosts. Do not pass a URL to `obd mirror clone`, invent an `obd mirror pull/download` command, or otherwise use `obd mirror` as a network downloader.

`obd mirror clone <path>` starts only after the complete RPM already exists at that controller-local path and has passed identity and checksum verification; it imports the local file into OBD's local repository. `obd mirror update` refreshes repository metadata, and `obd mirror add-repo` downloads and registers a remote `.repo` definition URL; `add-repo` is not a local RPM, local file, local directory, or release-suffix override path. Neither command downloads the requested package file. A repository definition tells a resolver where it may look later; registering one is not proof that the requested package exists, that its effective URL belongs to the intended source, or that any package bytes were downloaded. For a non-RPM artifact, use only its version-proved local registration, image-load, extraction, or installation path. During a clean OBD bootstrap, install the verified controller-local OBD artifact directly because no working OBD exists to import it. In online mode, a package-selecting workflow may resolve and fetch through an enabled remote repository only after its effective artifact URL and winning candidate are proved.

The V4.6.0 command surface preserves these ordinary operation shapes:

```bash
obd mirror list [mirror_repo_name]
obd mirror update
obd mirror clone <reviewed_rpm_path>
obd mirror create --name=<component_name> --path=<reviewed_install_tree> --version=<component_version> [--tag=<reviewed_tags>]
obd mirror disable <mirror_repo_name>
obd mirror enable <mirror_repo_name>
obd mirror add-repo <reviewed_repository_definition_url>
```

Confirm each form with the installed help. `list` is inventory; `update`, `clone`, `create`, `disable`, `enable`, and `add-repo` mutate controller state or future candidate resolution and require the matching gates below. The available `--force` options are intentionally omitted from reusable examples; do not add them automatically.

## Baseline and Selection

1. Record the controller identity, `OBD_HOME`, existing mirror definitions and enabled state, metadata timestamps, local repository inventory, active repository mutation, and package candidates relevant to the request.
2. For every artifact, record component, version, release, architecture, checksum/hash, size, source mirror, and provenance. Select one reviewed artifact per component; do not let version-only or “latest” matching choose among multiple releases.
3. Resolve dependency and compatibility edges separately. A repository can contain individually valid packages that cannot be used together.

Listing the mirror and listing the local repository answer different questions. Preserve both views when diagnosing why resolution changed.

## Keep Acquisition on the Selected Controller

In a remote workflow, `local repository`, `local package`, and `download locally` refer to the selected OBD controller, not the automation runner. Keep package discovery, candidate selection, download, checksum verification, import, and OBD execution on that controller by default.

Before the first OceanBase package network request, use controller-local inventory to confirm remote-repository enabled state, effective base URLs, metadata state, the target suffix, and the exact requested package identity. This local preparation must not be replaced by a generic Internet-connectivity test. Then make the first actual package request against source 1. After a source attempt fails, inspect DNS, route, proxy, TLS trust, HTTP response or redirect, metadata refresh, package-manager resolution, authentication, or local capacity as needed to explain that failure and prepare a different applicable download mechanism on the same source. Such diagnostics are not a mirror source, do not increment the three-attempt count, and cannot justify skipping to the next source or changing machines.

Treat operating-system repositories separately. If an unavailable BaseOS/AppStream or equivalent repository prevents dependency resolution, diagnose and repair only that dependency channel, preserve its baseline, and restore temporary changes. That work does not count as an OceanBase source attempt and does not authorize replacing or skipping the selected OceanBase source. Do not combine an operating-system repository rewrite, OceanBase repository registration, and package installation in one output-suppressed compound command; execute and verify each stage independently. Necessary in-scope persistent proxy, trust, repository, or host changes follow the shared default-consent rule: record and verify the exact change without asking again solely because it persists; do not add unrelated changes.

Record the mirror-source priority, effective base URL, component/version/release/suffix/architecture, download mechanism, attempt number from 1 through 3, exact package URL when known, relevant proxy/repository state, timestamps, and result. Restore any authorized temporary state. After the full controller-local suffix-by-source-and-mechanism matrix is exhausted, use another reachable host as the bounded artifact relay described above without changing controller identity. The relay may download and transfer the exact artifact but must not install or run OBD or the requested workflow. Ask the user only after that relay path also fails or when proceeding requires an unlisted source, a different controller, or an unresolved artifact choice.

## Repository Availability Probe

Do not classify a package, platform, or component as unsupported merely because the currently enabled remote sections return no candidate or the repository substituted the target system's current `$releasever`. Before an `UNSUPPORTED` verdict:

1. Record the target `/etc/os-release` identity and major version, architecture, package manager, OBD's resolved `$releasever`, and the fully substituted URL of every relevant repository section.
2. List all remote sections, including disabled ones, with enabled/available state, base URL, metadata age, refresh errors, and relevant local candidates.
3. For each required component and dependency, preserve product form, version, release, and architecture while probing the target-system suffix, EL8, and EL7 in that order. Do not stop after only the current `$releasever` returns no package.
4. For each suffix, probe `https://mirrors.oceanbase.com` first and the direct package directories under `https://mirrors.aliyun.com/oceanbase` second. Do not pre-filter either source through a generic reachability verdict. A source is exhausted only after three failed complete acquisition attempts for that exact candidate.
5. For each source and suffix, establish three independent layers: repository metadata/index presence and freshness; effective base, metadata, and candidate-object URL behavior including TLS/redirects; and an exact package filename or NEVRA candidate for the required component plus its dependency closure. Confirm that the effective base URL still belongs to the mirror source being counted.

If a trusted relevant section is disabled, temporarily enable that exact section when required by the requested package-resolution or compatibility probe. The request authorizes this bounded controller-wide state change under the shared persistent-change default; do not ask again. Capture its original state, refresh and inspect the candidate set, and restore the exact state after the probe unless the selected online workflow still needs it enabled through final package selection. Verify restoration; do not infer package absence or switch machines to avoid the probe.

Only a conclusive negative result at the metadata, URL, and exact-package layers after three failed attempts on each fixed mirror source for every required suffix supports an `UNSUPPORTED` package verdict. A generic connectivity result, timeout, authentication failure, certificate failure, stale metadata, skipped source or suffix, disabled untested source, or omitted attempt does not. In a test report, omitting a required in-scope source or attempt is an incomplete or failed test execution, not a blocked product capability.

## Choose Online or Local-Package Resolution

Choose one resolution mode before a deployment or other package-selecting workflow:

- **Online mode:** keep the reviewed remote repository enabled and prove the exact remote source and winning component/version/release/suffix/architecture/hash. Let the package-selecting workflow resolve and fetch through that repository; do not invoke `obd mirror` as a downloader. Online mode does not require downloading or importing the package into the local repository first.
- **Local-package mode:** explicitly download each required RPM on the controller with `curl`, `wget`, or the operating-system package manager, verify it, then import the already-local file with `obd mirror clone`. Prove that the exact selected artifacts and complete dependency closure exist in the local repository. Capture the enabled-state baseline, use the installed public command to disable every remote section that can participate in resolution—commonly the section named `remote`—and immediately re-list mirror state and eligible candidates. Do not execute the package-selecting workflow unless remote resolution is absent and the expected local hashes are the only proved winners.
- **Online-to-local fallback:** when normal online resolution or fetch fails but an explicit controller-local download or bounded artifact relay obtains the exact artifact, transition the whole package-selecting operation to local-package mode. Acquire and import the complete required closure, apply the remote-disable isolation window, then retry the original workflow against the proved local winners. Do not import one package and leave unresolved remote candidates competing for the rest.

Disabling participating remote sections is intrinsic to an explicitly selected local-package workflow and is covered by the shared persistent-change default; record it but do not request another confirmation. Keep remote resolution disabled through the final package-selecting stage. Unless the user requested a persistent local-only controller policy, restore every temporarily disabled section to its exact prior state afterward and verify the candidate-set baseline. Do not use an unresolved hybrid mode; acquire the remaining closure locally or choose online mode explicitly.

## Register or Update a Remote Source

Before `mirror add-repo` or an equivalent supported command:

- resolve the repository definition or URL to the exact reviewed input;
- verify its name does not collide with an existing section;
- review transport, certificate validation, authentication source, OS/architecture scope, component scope, ownership, and permissions;
- reject embedded clear-text credentials, unapproved redirects, disabled certificate verification, and unexpected symlinks;
- explain that registration or metadata update changes future package candidates but does not itself select or install a package.

Update only the intended source. Afterward, compare mirror state and candidate inventory with the baseline. Stop if an existing deployment workflow could now resolve to a different artifact without an explicit hash or other unambiguous constraint.

## Import or Create Local Artifacts

Treat `mirror clone`, `mirror create`, and comparable operations as repository mutations. `mirror clone` takes a controller-local RPM path; it is not a remote fetch operation and must never receive a URL. Inspect the source artifact or build directory, metadata, checksum, ownership, and destination behavior first. Do not use force automatically; overwriting an existing artifact or tag can change future resolution.

For `mirror clone`, record both the incoming RPM MD5 and its package filename. Independently inventory (a) any local-repository record with the same MD5 and its current path and (b) any record or file that uses the destination filename. In the inspected implementation, the overwrite prompt and `--force` gate are keyed by the incoming MD5, while the copy target is keyed by package filename. These are different collision identities: the same MD5 can replace/move its recorded file, while a different MD5 with the same filename can overwrite the bytes beneath an older MD5 record. `--force` only bypasses the same-MD5 prompt; it does not make a filename collision safe.

Before any authorized forced clone, show the exact old/new MD5, package metadata, source and destination paths, affected repository records/tags, active consumers, and candidate-resolution delta. Retain the exact prior RPM and its checksum plus a version-supported re-import plan; do not promise rollback by editing hidden repository metadata. Afterward verify the destination bytes, every affected MD5 record/path, tags, and selected candidates. Stop if a stale record or supported restoration path cannot be ruled out.

For `mirror create`, first identify the selected installed component plugin and its required file list, then prove the build/install tree contains every required path with the expected file type, executable bit, symlink target, architecture, and version metadata. The V4.6.0 guide's source-build example runs the build system's staged install before `mirror create`; OBD collecting files from a directory is not proof that the directory is complete. If the installed plugin file list or any required object cannot be established, do not invoke `mirror create`. Treat `--force` as replacement of an existing image or tag and authorize that exact repository object separately.

After import, verify the local repository shows the expected exact artifact and that no unrelated entry changed. For `mirror create`, verify the main repository's real hash/file list and every requested tag independently: inspected code can create the main repository, fail one or more tag operations, print errors, and still leave a partial result. A successful exit is not proof that all tags point to the intended hash. Repository registration is not installation acceptance.

## Enable, Disable, and Clean

Changing a mirror's enabled state is controller-wide and can affect every later resolution. Capture the original state and active tasks, change only the named section, then verify the candidate-set delta. The local-package isolation window above is conditional on choosing local packages; it is not a requirement to pre-download packages for an online deployment.

Repository or mirror cleaning is destructive. The V4.6.0 guide documents that `obd mirror clean` without filters removes all currently unused component files while retaining only a version-sorted latest RPM per component; that is still a broad deletion, not maintenance discovery. Do not invoke the clean command to obtain a preview: inspected code can continue from its listing directly into deletion, and a controller-wide automatic-confirm setting can suppress the prompt.

Handle a `mirror clean` confirmation through [non-interactive automation execution](../../references/automation-execution.md). If the installed command needs an interactive answer, use a real PTY rather than an ordinary pipe, display the exact expanded hash/path selection before confirmation, and confirm only that reviewed selection.

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before producing the repository deletion set. Deployment, component, tenant, test, or controller-maintenance authorization never implies mirror, cache, downloaded-package, or tag cleanup.

The installed V4.6.0 command supports filters such as `--components=<names>`, `--type=<rpm|repository>`, and `--hash=<exact_hash>`, plus `--confirm`. These options select or confirm deletion; none is a dry-run. Do not emit an executable clean command until the exact selected objects have been independently enumerated and authorized.

Build the preview from read-only mirror/repository inventory and exact filesystem identities. Record automatic-confirm state, active tasks, deployment and rollback references, then enumerate the precise hashes and paths proposed for deletion. Prefer an exact supported `--hash` filter. A component/type filter still selects a set and must be expanded before authorization. Never run an unfiltered clean unless the user explicitly requested that complete enumerated set after seeing its impact. If automatic confirmation is enabled, stop or separately authorize a temporary controller setting change and restore its exact prior state before any other task.

Rollback restores the original repository definition and enabled state, refreshes only the affected metadata, and proves that the candidate set matches the recorded baseline. Do not delete unrelated cache, credentials, or mirror files.
