# Offline Repository Preparation

Use this workflow to prepare and validate all artifacts required for an OBD operation in an air-gapped or no-egress environment.

## Build the Closure Outside the Offline Operation

1. Resolve the exact OBD build and the requested product form, topology, components, versions, releases, architectures, plugins, and package dependencies.
2. Include the OBD installation artifact separately from component artifacts when the controller is not yet installed. For commercial (Enterprise Edition) and standalone/centralized artifacts, first inspect the controller's OBD local repository; if any required entry is absent, require user-provided files or an existing accessible path. Do not download them automatically, and never replace missing items with community packages.
3. Record provenance, checksums/signatures, sizes, licenses/access boundaries, and the expected repository identity of every file. A directory containing similarly named packages is not a dependency closure.
4. Inspect the transfer destination, free space, ownership, permissions, mount boundaries, and symlinks. Use a manifest with an exact file count and checksum for transfer verification.

Do not download during the offline deployment workflow. Network access and the staging host are separate scopes requiring their own approval.

## Import Without Changing Selection Accidentally

Capture the controller's mirror enabled state and local repository inventory. Import only the reviewed artifacts using the current OBD build's supported local-repository workflow. Do not use force, wildcards over an unreviewed directory, or broad repository cleanup.

Disabling remote mirrors is a controller-wide policy change, not a required side effect of every offline import. Do it only when the offline policy or resolution test requires it, record every affected section, and state whether the change is temporary or persistent.

After import, verify each expected component/version/release/architecture/hash appears exactly once in the local repository and that no unexpected candidate was added.

## Prove Offline Resolution

Before a real deployment or upgrade:

1. use a version-supported non-deploying resolution or preflight path when available;
2. verify every selected artifact and plugin resolves locally by exact identity;
3. verify the operation does not depend on remote metadata refresh, dynamic tool installation, package-manager download, or another unapproved runtime dependency or egress path;
4. exercise the resolution under the intended network policy when that can be done without mutating the target.

If any dependency remains unresolved, stop and update the manifest outside the offline operation. Do not enable a remote mirror temporarily, choose a different release, or proceed with a partial set without a new reviewed plan.

Retain imported artifacts according to the recovery plan. Removing them later is a separate repository-cleanup operation; never delete all local packages merely to restore an earlier mirror view.
