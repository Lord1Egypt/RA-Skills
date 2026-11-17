# Dynamic Tool Lifecycle

Use this workflow for `obd tool list`, installation, update, and uninstall. A top-level alias can exist even when its backing tool is not installed.

## Inventory Before Alias Invocation

Start with the core tool inventory, local and already known remote repository candidates, installed tool paths, executable entry points, versions, package hashes, and consumers. Do not invoke a dynamic alias or alias-specific `--help` as an inventory probe: alias resolution can refresh metadata, download a package, enter an installation prompt, or attempt an update even when the tool is already installed. Automatic-confirm settings can turn that probe into an installation or replacement.

Read the installed core `obd tool --help` and selected core subcommand help. Inspect version-matched dispatch behavior before the first alias invocation and treat any unsuppressible update check as a potential mutation. Inventory is separate from execution of the tool itself.

## Install or Update

1. Identify the requested capability and prove that the selected tool/version provides it.
2. Resolve one package by tool/component name, version, release, architecture, hash, source, install prefix, and entry point. Do not default to latest.
3. Review network access, download/cache/install paths, dependency changes, privileges, conflicts with other tools, and the rollback artifact.
4. For an update, inspect the installed implementation's replacement order. Verified 4.7-era code removes the existing tool tree before copying the replacement and can remove the tool configuration when installation fails. Treat that behavior as a non-atomic uninstall-plus-install and a tool-availability mutation. Record every active consumer, the old config and path, and an exact locally available old package/hash with a version-proven restoration procedure; a metadata copy alone is not a rollback.
5. Obtain authorization for the exact download and installation. When the update is non-atomic, the authorization must also name deletion of the existing installation, the unavailable interval, and the possible tool-absent failure state. This does not authorize running the installed tool against a deployment or diagnostic target.
6. Do not add automatic-yes or force options by default. A conflict must be resolved from observed ownership and dependency state.

After installation or update, verify the OBD tool inventory, actual executable path and version, package hash, ownership, and one minimal non-mutating command that cannot trigger a second installation or update. Confirm unrelated tools did not change. On a failed non-atomic update, preserve the missing/partial state and restore the recorded old artifact only when the observed paths and installed workflow make that safe; do not blindly repeat update or create an empty config directory.

## Uninstall

Before uninstall, identify the exact installed version, active process, scheduled job, plugin, alias, and workflow that depends on it. Show whether cached packages, shared dependencies, configuration, or output data will remain. Obtain authorization for the selected tool only.

After uninstall, verify the inventory entry and entry point are absent while unrelated tools and shared directories remain intact. Do not force-remove a shared tool directory or broadly clean repositories.

On any partial result, inspect inventory and files before retrying. Tool installation success and successful use of the tool are separate completion results.

## Sources

- Official OBD V4.6.0 Command Guide tool command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `core.py` tool install/update/uninstall functions and dynamic alias dispatch in the exact inspected checkout.
