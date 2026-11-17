# OBD Controller Maintenance

Use this workflow to update, replace, pin, downgrade, or roll back OBD itself. This does not upgrade any managed component.

## Inventory and Compatibility Gate

1. Record the controller, user, exact executable, package owner and installation method, OBD version/build/revision, runtime, installation prefix, `OBD_HOME`, active OBD/Web tasks, and every registered deployment.
2. Record the installed plugins, workflows, schemas, local and remote repository configuration, and metadata format. Back up only the controller state required for recovery, using permissions that protect stored credentials; keep secrets out of the report.
3. Resolve the target artifact by exact version/build, OS, architecture, checksum, source, and installation method. Confirm compatibility with the existing metadata, plugins, repositories, and workflows needed by the registered deployments.
4. Read the installed `obd update --help` and determine how that build selects its update target. Enumerate every eligible local package and every enabled remote candidate before authorization, then prove which exact version, release, architecture, and hash the resolver will choose. Do not claim that `obd update` pins a requested version unless its actual command, implementation, and complete candidate set prove that. Use a reviewed package artifact when exact pinning or rollback is required.
5. Inspect the selected build's replacement order. In the inspected current source, `obd update` removes the installed `workflows`, `plugins`, `config_parser`, and `optimize` trees before copying the replacement; a copy/load failure can therefore leave a partially unusable controller. Record those exact trees, their package owner, and a version-compatible restoration artifact or protected snapshot before authorization. Do not describe this implementation as atomic.
6. Wait until no lifecycle command, Web/API task, repository mutation, tool installation, or test orchestration is active. Show the controller outage or command-availability impact and the complete rollback artifact before authorization.

Do not update OBD during an unresolved deployment failure merely to expose a command seen in newer source code.

## Official V4.6.0 Update Baselines

Keep the current installation method unless a separately reviewed migration is required. The V4.6.0 guide distinguishes these paths:

- For OBD installed through OceanBase All-in-One, use the version-compatible All-in-One upgrade workflow rather than replacing only the embedded OBD executable.
- For an RPM/repository installation that may track the enabled remote repository, review the repository source and candidate first, then use the installed `obd update` workflow and verify `obd --version`. This is not an exact-version lock unless the candidate set proves it.
- For an exact-version or offline RPM update, import the reviewed `ob-deploy` RPM into the local repository and disable remote repositories for the selection window. Re-enumerate all local `ob-deploy` packages: in the reviewed implementation the local mirror is always eligible and name-only resolution selects the highest matching package. Run `obd update` only after proving that this resolver selects the exact reviewed version, release, architecture, and hash. If a higher or otherwise competing winning candidate exists, do not use `obd update` as an exact-version mechanism; use a version-matched package-owned replacement or a separately authorized candidate-isolation procedure with a proved recovery path. Do not delete or alter unrelated local packages merely to force selection. Preserve the previous RPM and repository baseline for rollback, and verify the resulting build.

Do not transfer these V4.6.0 baselines to a source installation or another packaging layout without checking its version-matched upgrade procedure. Repository enable/disable changes and local artifact import are separate controller mutations and must follow the repository workflow.

## Change and Accept

Execute only the reviewed update or package-replacement method. Preserve package-manager output, artifact checksums, and any metadata migration record.

Afterward, verify:

- executable path, owner, version/build, runtime, plugin set, and metadata format;
- repository definitions and enabled state without changing package candidates;
- every registered configuration can be parsed and retains its identity;
- logical list/display inventory reports the expected deployments, allowing for ordinary controller-local CLI bookkeeping;
- the required command help exposes the options on which the planned workflow depends.
- each replaced workflow/plugin/parser/optimizer tree is present, owned by the expected package/build, and loadable; no mixture of old and new trees remains.

Do not start, stop, reload, or otherwise mutate a cluster just to test a controller update. Report controller compatibility separately from deployment runtime health.

If replacement fails after any old tree was removed, stop and treat OBD as potentially partially installed. Preserve the trace and exact tree inventory; do not rerun update or invoke managed-object commands through the damaged controller. Restore through the one pre-reviewed package-owned method or exact compatible snapshot, then repeat controller acceptance before any deployment operation.

## Rollback

Rollback requires both the recorded previous artifact and metadata/plugins compatible with it. If the new build rewrote state in a non-backward-compatible form, reinstalling the old executable alone is not a rollback. Determine whether restoring the protected metadata snapshot would discard controller changes made since the update; stop when that boundary is unclear.

Do not repeatedly alternate controller versions. Preserve the failed state and choose one version-matched recovery path.

## Sources

- Official OBD V4.6.0 OBD Upgrade Guide and Quick Start All-in-One upgrade sections.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `core.py` `update_obd` in the exact inspected checkout.
