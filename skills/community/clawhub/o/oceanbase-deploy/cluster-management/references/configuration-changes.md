# Configuration Changes

Use this workflow only for `edit-config`, `reload`, `chst` configuration-style conversion, and classifying how configuration fields become effective. Lifecycle operations, component changes, upgrade/reinstall, tenant operations, and deployment rebuilds belong to their dedicated workflows. A text edit, a successful reload, and an effective runtime change are distinct outcomes.

A deployed component's server-set change is a topology operation, not an ordinary configuration edit. Adding or removing Observer servers from a registered deployment is unsupported. Do not use `edit-config`, its complete-YAML standard-input path, a generated-file editor, SQL, obshell, component operations, process control, or metadata edits to perform or reconcile that transition. Generic access to a `servers` field is not evidence of support.

## Select an Existing or New Registered Configuration

Resolve the exact controller, OBD executable, `OBD_HOME`, and `deploy_name`, then determine whether that name is already registered. Do not assume that `edit-config` requires an existing deployment: the official V4.6.0 command guide and inspected current implementation support creating a registered deployment configuration when the name does not exist.

For an absent name:

1. Recheck immediately before the command that the name is still unused on the selected controller. Review one complete candidate deployment YAML, including product/component identities, versions, servers, paths, ports, resources, repositories, and secret handling.
2. Treat creation as a controller-local configuration registration and obtain authorization for that exact name and complete YAML. It does not authorize package installation, target-host changes, deployment, start, or tenant creation.
3. With a controlled TTY, `obd cluster edit-config <deploy_name>` can prompt to create the missing deployment and then open the editor. Do not use non-TTY standard input as the default creation path. Only an exact installed build already runtime-proved to accept one complete non-empty YAML document may use that version-specific path; a development source branch or another RPM is not proof. Obtain authorization before invocation rather than relying on either prompt behavior.
4. Accept success only when the registered deployment exists with state `configured`, its stored YAML parses, and its semantic content and checksum match the reviewed candidate. Confirm that no component was deployed or started and do not run `reload`. Route a later deployment request through the [configuration deployment workflow](config-deployment.md), revalidate the stored configuration, and treat `obd cluster deploy <deploy_name>` as a separate mutation. Route a later start request through the [lifecycle workflow](lifecycle.md) only after deployment succeeds and the registered and installed state has been verified.

If the name appears concurrently, the stored content differs, or any target-host/runtime side effect is observed, stop and preserve the controller trace and configuration evidence.

## Build the Change Set

1. For an existing deployment, record the OBD build, deployment identity and state, selected component/plugin versions, registered configuration checksum, and effective database/component values.
2. Read the installed command help and plugin parameter schema/workflows. Classify every field as:
   - dynamically applicable;
   - accepted by OBD but requiring a component restart;
   - immutable or unsupported after deployment;
   - requiring a supported upgrade, reinstall, component transition, or destructive rebuild path.
3. Show the semantic before/after values, target servers/components, generated-file impact, availability effect, persistence boundary, and rollback value.
4. Save a protected, redacted-for-display snapshot outside deployment-owned paths. Preserve the unredacted source only with permissions appropriate for its credentials.

If the installed plugin cannot establish the apply class, stop. Do not assume `reload` makes every accepted field dynamic.

<a id="serialized-effective-and-runtime-values"></a>

### Serialized, Effective, and Runtime Values

Classify a configuration change at three separate layers:

1. the serialized YAML diff, including whether a key moved between `global` and a server section;
2. the effective value calculated for every server after defaults and scope inheritance;
3. the value actually used by the running component.

A scope-only move or duplication can change the serialized YAML while leaving every effective and runtime value unchanged. Conversely, an installed OBD parser or plugin can still classify that textual change as an immutable port, path, or topology mutation and require redeploy. Compute and record all three layers before editing; do not infer impact from the textual diff alone.

If OBD rejects a scope-only normalization with an immutable or redeploy-required error, including an `OBD-1026`-class result, do not bypass the guard, edit hidden metadata, reload blindly, or perform a destructive redeploy solely to normalize the document. Prefer a corrected controller/workflow, or render the required scope before the first deployment. If neither is available for the existing deployment, preserve the current effective runtime state and report that the requested representation has no supported non-destructive transition.

## Auditable Editing

`obd cluster edit-config <deploy_name>` can open an editor. The default automation path is a real, controllable PTY plus a version-proven editor integration. Tested frozen builds have returned `Input is empty` or `Empty configuration` under non-TTY automation instead of accepting a replacement or opening the editor. Do not first try an empty pipe, redirected stdin, here-document, or a non-PTY session and then improvise around that failure.

An inspected development implementation contains a branch that reads non-empty standard input as the complete candidate deployment YAML instead of opening an editor. Treat that as source-only evidence. Use non-TTY whole-document replacement only when the exact installed build has already been runtime-proved to implement it; otherwise use the PTY/editor path. Even where proved, submit exactly one complete protected YAML, preserve its checksum, and require the resulting semantic diff to match the approved change set. It is never a field-patch interface: do not send a fragment, omit unchanged secret-bearing fields, or invent a `--set` option.

For automation, first inspect how the installed OBD build selects and invokes its editor. If it honors a command-local editor variable, use a narrowly scoped wrapper that:

- accepts only the exact generated configuration path supplied by OBD;
- verifies the expected pre-edit checksum;
- changes only the reviewed keys;
- records the file device and inode, rewrites and truncates that same file in place, and verifies that its device and inode remain unchanged;
- rejects a missing, symlinked, or unexpected path;
- writes no secret into terminal output;
- returns failure unless the post-edit YAML parses and the semantic diff matches the approved change set.

Do not use `sed -i`, temporary-file replacement, rename-based atomic writing, or an editor that swaps the generated file's inode in this path. In the tested build, such a replacement made OBD report `config unchange`; an in-place rewrite under a controlled editor and PTY was observed correctly. This is an editor-path compatibility requirement, not permission to edit hidden OBD metadata.

For an existing deployment, the bundled [`obd-edit-config-pty.py`](../scripts/obd-edit-config-pty.py) implements this transport boundary. Run it on the selected OBD controller, under the established controller user, with an already reviewed complete replacement YAML stored in a task-owned `0600` file. If the Skill files are not present on that controller, copy only this helper into a task-owned `0700` directory, verify its checksum, and remove that copy under the normal task cleanup boundary. Resolve and verify the absolute Python interpreter and canonical non-symlink OBD executable first; record the OBD SHA-256 and do not rely on `PATH` for either executable. Use the shape, replacing both `/absolute/...` placeholders with those verified paths:

```bash
/absolute/path/to/verified-python3 /absolute/path/to/obd-edit-config-pty.py \
  --deployment <exact_existing_deploy_name> \
  --replacement <protected_complete_yaml> \
  --replacement-sha256 <reviewed_sha256> \
  --obd /absolute/path/to/verified-obd \
  --obd-sha256 <reviewed_obd_sha256> \
  --transcript <protected_unique_transcript>
```

The helper sends no response to OBD. It rejects PATH lookup, relative paths, symlinked executables, untrusted writable executable paths, and an OBD hash mismatch before fork; it revalidates the executable identity immediately before execution. The OBD child receives the fixed system PATH `/usr/bin:/bin`, and Python, dynamic-loader, and shell startup injection variables are removed. This permits a reviewed OBD wrapper that uses a system interpreter without allowing the caller's PATH to select it; a wrapper that depends on a non-system interpreter is outside this helper's boundary and must not be used here. The helper fails closed on every confirmation prompt, validates the candidate checksum, rejects a symlink or broadly readable candidate, rewrites and truncates the OBD-generated temporary YAML through its existing file descriptor, and verifies that device/inode did not change. The protected transcript can still contain OBD-rendered configuration or errors; never print or attach it without redaction. After success, independently verify the registered configuration checksum, semantic diff, config status, effective values, and absence of unrelated changes. The helper is transport and editor plumbing, not authorization, semantic review, `reload`, or permission to accept a redeploy-required change.

Do not invent a `--set` option, leave a persistent global editor override, or edit hidden `.obd` files directly. If no safe PTY/editor path or deliberate complete-YAML standard-input path is supported, stop.

## Apply and Verify

Use only the installed syntax, commonly:

```bash
obd cluster edit-config <deploy_name>
obd cluster reload <deploy_name>
```

Before reload, inspect the recorded diff and refresh component health. Obtain availability authorization if the installed workflow can restart any target. Current inspected OBD HEAD exposes no component/server selector for reload and applies it across the deployment; on a stopped or unhealthy deployment it may first start the whole deployment. Display and authorize that full scope and implicit start, or stop when the requested scope is narrower. Preserve the trace ID.

For a field already proved dynamically applicable by the installed plugin, capture Observer PIDs and start times and run a bounded authenticated SQL continuity probe before, throughout, and after reload. The tested dynamic-parameter path changed the effective value without restarting Observer and kept SQL continuously available. Treat that as the expected no-restart acceptance result only for fields classified dynamic in the selected build; do not generalize it to restart-required or unresolved fields. Any PID/start-time change or SQL interruption disproves a no-restart claim even when final health recovers, and inability to observe the reload interval means uninterrupted availability was not established.

Afterward compare:

- registered configuration and generated per-server files;
- component command line or local configuration where relevant;
- database/API-side effective values;
- selected process PIDs/start times and service health;
- SQL continuity across the reload interval when a dynamic no-restart result is expected;
- unselected fields and targets.

Report values that remain pending restart. Never report a field as applied solely because `reload` exited successfully.

## Configuration Style Conversion

Use `obd cluster chst` only when the installed help and selected plugins expose the requested style. Treat it as a configuration mutation, not display formatting.

Before conversion, save the registered configuration and metadata checksums, enumerate supported styles and field mappings, and produce a semantic preview covering components, servers, zones, paths, ports, resources, dependencies, secrets references, and artifact constraints. Use the exact version-supported syntax; do not assume a style name or option from another release.

After conversion, prove semantic equivalence and that OBD can parse/display the deployment. Do not reload or restart merely because conversion succeeded. If a field was lost or changed meaning, stop and restore only from the validated snapshot.

## Failure Boundary

If `edit-config` fails while loading the unchanged generated YAML, before an approved semantic edit has occurred, classify the editor path as unavailable for that exact OBD build and registered configuration. Preserve the unchanged checksum, temporary-YAML parsing error, trace, registered configuration, and runtime state, then stop. Do not automatically switch editors, submit the whole document through standard input, or edit hidden metadata to bypass the failing parser.

On any edit, reload, or conversion failure, preserve both configurations, trace, generated files, real process state, and effective runtime values. Do not apply a second edit, restart all components, or redeploy until the observed state identifies the narrow recovery action.

## Sources

- Official OBD V4.6.0 Command Guide cluster configuration command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `_cmd.py` `ClusterEditConfigCommand`; `core.py` `edit_deploy_config` in the exact inspected checkout.
