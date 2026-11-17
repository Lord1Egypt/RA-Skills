# Uninstall OBD or Its Owning Distribution

Use this workflow only when the user explicitly requests controller removal. First read the shared operation, cleanup, failure, and completion contracts. Uninstalling OBD is not deployment cleanup, and destroying a deployment does not authorize uninstalling OBD.

## Resolve the Installation Owner

Record the controller user, every `obd` executable, package-manager record, installation prefix, All-in-One root, source-build manifest, shell-profile entries, `OBD_HOME`, registered deployments, plugins/tools, active OBD/Web/API/automation processes, and rollback artifact. Determine exactly one owner:

- an OceanBase All-in-One distribution;
- an `ob-deploy` RPM/repository package;
- an approved source/development installation;
- unresolved or mixed ownership.

Stop on unresolved or mixed ownership. Do not remove one executable while leaving a profile entry that selects another, and do not use recursive deletion as discovery.

## Select the Owner's Uninstall Path

### OceanBase All-in-One

The V4.6.0 guide uninstalls the **All-in-One distribution**, not a standalone TAR installation and not necessarily only OBD. Inspect the exact owned All-in-One root and its `bin/uninstall.sh`, enumerate every bundled product/file/profile object it will affect, and obtain authorization for that complete set. Then run only the reviewed script from that exact tree:

```bash
bash <absolute_all_in_one_root>/bin/uninstall.sh
```

Removal of an exact `source .../.oceanbase-all-in-one/bin/env.sh` line from the owning user's profile is a separate reviewed edit. Preserve unrelated profile content and require a fresh shell or a separately approved reload to validate PATH changes.

### RPM or Repository Package

Use the package manager record for the exact installed `ob-deploy` package and the target OS's version-matched removal workflow. Preview the package-owned removal set and dependency impact first. Do not guess a package name, remove repository/component RPMs merely because OBD referenced them, or clean local/remote mirrors as part of controller uninstall.

### Source or Development Installation

Use the approved build/install manifest or release-owned uninstall procedure. If no exact ownership manifest exists, stop and report that safe automatic uninstall cannot be proved. Do not reconstruct the file set from path-name patterns or broad prefixes.

## Preserve Controller Data by Default

Before uninstalling, explicitly ask whether the user wants to remove only the OBD executable or owning distribution, or also delete the resolved controller data directory. Resolve that directory for the actual controller user; it is commonly `~/.obd`, but do not treat the literal shorthand as a proved path. If the user does not explicitly choose deletion, preserve it.

Keep `OBD_HOME`, registered deployment metadata, traces, repositories, cached artifacts, stored credentials, tool state, and managed hosts/components unless each exact object is separately requested, enumerated, and authorized. Deleting the resolved controller data directory requires showing its exact path and summarizing the deployments, traces, repositories, cached artifacts, credentials, and tool state it contains before obtaining authorization. Warn that preserving encrypted credentials also preserves sensitive controller state; protect permissions and hand the retained path to its owner.

An uninstall that removes the executable while deployments continue running does not transfer their ownership or prove they are healthy. Record how they will be administered afterward before removing the last working controller.

## Accept or Recover

Verify that only the authorized executable/package/profile objects are absent, the fresh-shell PATH no longer resolves the removed installation, retained controller data is intact and protected, managed processes/listeners were not changed, and unrelated packages/profile entries remain. Report any retained `OBD_HOME`, registration, repository, or runtime state explicitly.

On script/package failure, preserve output and re-inventory the exact installed/removed objects. Do not retry with recursive deletion, a second installation method, or a broader package removal. Restore only through the pre-reviewed owner-specific artifact and then reassess.

## Sources

- Official OBD V4.6.0 Quick Start section 1.2, “Uninstall OceanBase All-in-One.”
- Package-manager or source-install ownership records for the exact installed controller; the V4.6.0 All-in-One script does not define a universal RPM/source uninstall procedure.
