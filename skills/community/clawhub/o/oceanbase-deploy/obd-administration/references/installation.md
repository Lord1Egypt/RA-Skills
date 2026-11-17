# Install OBD on a Controller

Use this workflow for a new OBD installation. Use [controller-maintenance.md](controller-maintenance.md) when an executable or package already owns the intended controller state.

Do not apply a controller-wide root or sudo eligibility gate. An existing OBD may be inspected and used under its owning login-session user for every operation that user can perform. Evaluate privilege only when the selected new-install transaction reaches a command that actually requires it; inability to elevate blocks that installation step, not unrelated OBD operations or the whole Skill. If the required OBD installation transaction cannot run because the current controller login user lacks sudo privilege, tell the user plainly, in the user's language: **the current controller user lacks sudo privilege; switch the controller login to a sudo-capable user, or grant sudo privilege to the current user**. Do not silently switch users or modify sudoers.

## Resolve the Installation

Controller bootstrap precedes the installed-build capability gate. If inventory proves there is no OBD executable, no existing OBD metadata owner, and no installation to take over, route directly through this installation workflow; do not require help output from a nonexistent CLI. Establish the OBD/plugin/schema capability record only after installation acceptance. Before then, deployment material is planning-only and commercial artifacts/repositories remain unresolved.

The controller RPM is `ob-deploy`. It is the same public OBD package for Community and Commercial OceanBase deployments, and its first and normal download location is `https://mirrors.oceanbase.com/community/`. Never look for a separate commercial OBD build, let the target database edition change its source, or route it through the commercial database/component acquisition workflow.

For a cluster deployment, select the installation target through the shared [default controller, SSH, and cluster discovery rule](../../references/operation-contract.md#default-controller-ssh-and-cluster-discovery). Inspect every supplied cluster host first. Reuse the target host that owns the intended registration or another unambiguous usable target-host OBD installation. Only after all targets are reachable and all are confirmed to have no OBD executable, package ownership, controller metadata, or registration, install OBD on the first supplied cluster host without asking the user to choose. This applies to every deployment mode and package-acquisition mode. A user-explicit separate controller overrides the default; an unreachable target does not count as empty.

A failed download or repository request does not justify installing OBD on the automation runner or moving the controller. Follow the [fixed artifact-source order and acquisition fallback](mirror-and-repositories.md#fixed-online-package-source-order). On a clean controller with no verified local OBD RPM, begin under `https://mirrors.oceanbase.com/community/`, default to resolving and downloading the exact `ob-deploy` RPM there with controller-local `curl` or `wget`, and install that local RPM through the operating-system package manager. Do not add a persistent OceanBase `.repo` merely as the default bootstrap path. If one mechanism fails, remain on the current effective source and use another applicable controller-local mechanism through the required source/suffix attempts. If no controller-local method works, use another reachable host only as a checksummed artifact relay, transfer the exact package to the controller, verify it again, and install it there. Ask only after the relay also fails, or before using an unlisted source or different controller.

1. Resolve the intended controller host and login user through inspection rather than asking for facts that can be observed. Use the user-supplied login account, or `root` when no login user was supplied; use passwordless SSH when no authentication material was supplied. After login, keep that login-session user for OBD installation and execution, controller-owned files, `OBD_HOME`, and controller-to-node SSH; do not derive or switch to another OBD execution user. Inventory every existing `obd` executable on `PATH`, package-manager record, profile entry, installation prefix, `OBD_HOME`, registered deployment, active OBD process, and shared automation that invokes OBD.
2. Select an installation method supported for the target operating system, architecture, and artifact: an exact released RPM/package, an approved All-in-One distribution, or a source/development build. Do not mix methods without an explicit ownership and rollback plan.
3. Resolve the exact OBD version/build, operating system, architecture, runtime requirements, source, checksum/signature, installation prefix, executable path, and expected plugin/repository content. Do not use an unpinned “latest” command when reproducibility matters.
4. Review the network source, destination path, privilege escalation, package dependencies, and files the installer can create or replace. A request to execute an OBD-dependent deployment when the selected controller is proved clean authorizes the controller-local artifact acquisition, first package installation, necessary profile changes, and package-manager non-interactive acceptance intrinsic to that selected method; record them but do not ask for separate confirmation before the install command. An explicit standalone OBD-install request grants the same authority. Overwriting another owner, replacing/upgrading/downgrading an existing OBD installation, or changing the installation/controller identity remains out of scope.
5. If existing OBD metadata is present, stop and classify the request as maintenance. A new binary with a fresh `OBD_HOME` can hide registered deployments; a new binary pointed at old metadata can migrate it.

Source builds are development artifacts unless an approved release process says otherwise. Record the revision and build inputs; do not present source `HEAD` as a released version.

Build the installation decision from target evidence rather than a remembered platform label:

| Decision | Required evidence | Stop condition |
|---|---|---|
| Operating platform | Distribution and version, kernel, architecture, package manager, container boundary, and available OBD package suffixes | No same-version, same-release, same-architecture candidate remains after the shared exact-suffix, EL8, then EL7 order, or neither fallback is runtime-compatible |
| Runtime compatibility | Dynamic loader, GLIBC and other required libraries/symbols, executable format, and disk/inode capacity for the exact OBD artifact | A required loader/library/symbol is absent; do not transfer an OBServer component requirement to the OBD controller package or vice versa |
| Ownership and privilege | Intended controller user, package/prefix/profile owners, the exact write/elevation requirements of the selected installer, umask, and shared automation | The exact installation transaction cannot complete under the current access path, or the method would overwrite another owner |
| Connectivity | Online/offline boundary, approved repositories, proxy/TLS trust, artifact transfer route, and checksum/signature verification | The only available path requires an unreviewed network source, credential exposure, or unpinned package |
| Existing state | Every executable, `OBD_HOME`, registration, active task, package record, profile entry, and rollback artifact | Existing state has no proved owner or safe maintenance/migration path |

For an RPM-based Linux controller, apply the shared [package-source and platform-fallback policy](../../references/product-and-capability-resolution.md#fixed-package-sources-and-platform-fallback): first the suffix matching the observed OS major version, then same-version/same-release/same-architecture EL8, then EL7. Verify the selected fallback package's loader, GLIBC/library dependencies, package-manager compatibility, and installed executable on the controller. This is the same suffix order used for every OBD-managed component; each component still requires its own runtime and dependency proof.

For the V4.6.0 official baseline, distinguish the supported methods rather than mixing their ownership:

- **All-in-One:** preferred when a tested compatible component set or offline installation is required; inspect its installer, bundled RPM closure, profile changes, mirror import, and remote-mirror state.
- **Released RPM/repository:** use controller-local `curl`, `wget`, or the operating-system package manager—not `obd mirror`—for any explicit remote download. Resolve and install the exact selected `ob-deploy` RPM and record package-manager/profile ownership; do not use an unpinned latest package when the required version is fixed.
- **Source:** development-only unless the user's release process explicitly approves it; validate the built revision and generated plugin/example content separately.

These are the three installation methods. An offline All-in-One archive does not create a fourth standalone TAR method: extraction only stages the All-in-One distribution whose reviewed `bin/install.sh` owns installation.

For the released-RPM path, choose the effective artifact source before the acquisition mechanism. Use controller-local `curl`, `wget`, or a package-manager path whose final package URL has been proved—not `obd mirror`—following the fixed source order `https://mirrors.oceanbase.com/community/` then the direct package directories under `https://mirrors.aliyun.com/oceanbase`, with three failed attempts per source before switching. A downloaded `.repo` file is only configuration and does not count as an OBD package attempt; inspect its resolved `baseurl` and candidate location before using it. If neither source yields a package matching the controller OS major version, use the shared EL8-then-EL7 fallback with the same source order.

Rocky BaseOS/AppStream and other operating-system repositories are dependency channels, not OceanBase artifact sources. If one is unavailable, handle it as a separate verified stage and restore temporary repository changes. Do not count that work as an OceanBase source attempt or combine an operating-system repository rewrite, OceanBase repository registration, and OBD installation in one output-suppressed compound command.

Installing a controller-local RPM can still make `yum` or `dnf` refresh every enabled operating-system repository. Before installation, inspect the exact `ob-deploy` RPM requirements with the available RPM or package-manager query surface and prove which installed providers or prepared local dependency RPMs satisfy them. If an unrelated enabled repository is unavailable but the full installation dependency closure is already installed, or every missing dependency RPM is verified locally and supplied in the same transaction, use the installed package manager's all-repositories-disabled form for those exact absolute paths. If any dependency remains unresolved, do not use that bypass: repair only the required operating-system dependency channel or acquire and verify the missing dependency RPMs. Do not rewrite all operating-system repository files merely to install OBD, and do not suppress repository or dependency output while deciding which case applies.

## Version-Matched Command Skeletons

Use these only after substituting reviewed absolute paths and confirming them against the selected V4.6.0 artifact/instructions:

- **Offline All-in-One:** verify the exact `oceanbase-all-in-one-*.tar.gz` checksum, extract it into a new empty staging directory, inspect the extracted `bin/install.sh`, then execute that script from the All-in-One tree. Do not call this a standalone TAR installation and do not execute an unrelated `install_obd.sh` or guessed installer name.
- **Local RPM:** install the exact reviewed `ob-deploy` RPM through the target OS package manager with its ordinary non-interactive acceptance option, for example `yum install -y <absolute_reviewed_ob_deploy_rpm>`. A proved enabled repository may instead use `yum install -y ob-deploy`, although the default clean-controller bootstrap remains direct download of the exact RPM. When the complete dependency closure is already proved and unrelated enabled repositories are the only blocker, use `yum --disablerepo='*' install -y <absolute_reviewed_ob_deploy_rpm> <absolute_reviewed_dependency_rpm> ...`, or its installed-help equivalent. Run the transaction as the established controller login user and apply an already available narrowly scoped elevation mechanism only if that exact command requires it. If sudo is unavailable, stop only the installation step and give the privilege notice above. Do not ask the user to approve these reviewed first-install commands. Package-manager `-y` is a scoped first-install exception, not permission to enable controller-wide automatic confirmation or accept OBD lifecycle, destructive, replacement, upgrade, or downgrade prompts. Do not use the all-repositories-disabled form with unresolved dependencies, a glob, or an unproved remote candidate.
- **Source:** check out the approved release revision, verify the V4.6.0 build prerequisites and scripts, then run the release's documented `rpm/build.sh` target. Record the resulting executable and generated content as a development/source-owned installation.

The V4.6.0 guide also documents a remote All-in-One bootstrap script, but do not pipe it from the network into a shell without separately reviewing and pinning its content. Prefer a downloaded, checksummed artifact when reproducibility or supply-chain control matters.

## Install

Use the selected method's version-matched instructions and the reviewed controller-local absolute artifact path. Install only on the controller, execute the proved first-install command without a separate permission prompt, and verify its result before continuing. Do not copy the OBD package to every managed host merely because OBD will later connect to them, and do not install it on the runner merely because the controller needed an approved artifact relay.

Keep privilege scope narrow. Do not pipe an unreviewed remote installer into a shell, overwrite another package owner's files, or create a second implicit `OBD_HOME`. Preserve existing shell and service configuration unless the chosen method requires a reviewed change.

## Accept

Verify independently:

- the executable path, owner, package/build identity, version, runtime, and installation prefix;
- the intended user resolves that executable in a fresh shell;
- `OBD_HOME` and its permissions are the intended ones;
- shipped plugins and repository definitions can be read without an unintended network update;
- any pre-existing registered deployments remain visible and parseable through logical list/display inventory, allowing for ordinary controller-local CLI bookkeeping;
- no managed component process, listener, configuration, or target-host path changed during controller installation.

On failure, preserve installer output and the before/after executable and metadata inventory. Do not delete `OBD_HOME`, reinstall through a second method, or remove profile/package files until ownership and the completed installation stage are known.

## Sources

- Official OBD V4.6.0 Quick Start section 1: All-in-One, RPM, and source installation.
- Exact package metadata, installer content, or source revision selected for the target controller.
