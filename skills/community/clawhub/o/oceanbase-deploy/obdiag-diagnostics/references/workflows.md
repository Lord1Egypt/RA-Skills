# obdiag Diagnostic Workflows

Use this workflow for the installed OBD build's supported obdiag collection, analysis, check, scene, ASH, and RCA operations.

## 1. Identify the Installed Tool

Use the installed OBD build's normal inventory, `obd obdiag --help`, or version path to identify the available diagnostic command families. Some builds may install or update the dynamic obdiag tool while resolving the alias; record any resulting package change and verify the final tool identity before collection.

First record:

- controller host/user, exact OBD executable/build, `OBD_HOME`, and active tasks;
- OBD automatic-confirm, developer-mode, telemetry/network, and mirror enabled state relevant to discovery;
- `obd tool list` output or the installed build's equivalent core inventory;
- the selected repository candidate when an install or update is needed, including version, architecture, source, and install prefix;
- the resulting obdiag executable path and version.

If obdiag is absent, follow [the tool lifecycle](../../obd-administration/references/tool-lifecycle.md) through the supported install path, then verify the resulting package and executable before diagnostic use.

Tool installation or update does not authorize collection, inspection of a deployment, or access to diagnostic data. Establish that scope separately.

The available command families and options are determined by the resulting OBD/tool combination, not by examples from another release. Use its help to select the exact syntax and record the version used for the diagnostic result.

## 2. Define the Diagnostic Scope

Record the question to answer and choose the exact:

- registered deployment and independently verified target identity;
- nodes, components, tenant/database context when applicable;
- absolute start/end time and timezone;
- evidence type or named scene/check;
- output directory, expected size, free space, ownership, permissions, retention, and transfer boundary;
- CPU, I/O, pause, connection, and data-exposure impact.

Keep credentials out of command arguments when protected input is available. Diagnostic output can contain addresses, usernames, paths, SQL text, schema names, and business data; define redaction and access before collection.

Obtain diagnostic authorization for the target and evidence scope. Obtain an additional production-impact authorization immediately before stack capture, performance sampling, broad/all-module collection, or another mode that can materially load or pause a process. Do not infer this authorization from permission to install obdiag.

## 3. Select the Smallest Supported Mode

- Use a bounded **gather** only for evidence that is not already available, with explicit target and time limits.
- Use **analyze** on an existing artifact when new production collection is unnecessary.
- Use **check** for version-supported rule-based inspection and record the rule/package version.
- Use **RCA** only for a supported scene and treat its output as a hypothesis.
- List scenes before selecting one. Updating scene definitions changes diagnostic behavior and package state; do it only when explicitly requested and after reviewing source, checksum, compatibility, and rollback.
- Generate ASH or other database-derived reports only after verifying the required tenant/account, time range, privileges, and expected query load.

Do not replace a narrow request with an all-module gather for convenience.

## 4. Execute and Verify Artifacts

Before execution, preserve the redacted command, OBD and obdiag versions, selected options, configuration checksum, target identity, time range, and output destination. Run one reviewed diagnostic task and retain its trace/task identifier.

Verify:

- the task reached a terminal state rather than merely starting;
- expected files exist under the approved canonical output directory;
- file sizes, timestamps, permissions, and checksums are plausible for the requested scope;
- every requested node/module/time range is represented and unexpected targets are absent;
- partial, truncated, or failed modules are reported explicitly;
- no unrelated service or listener changed.

Do not automatically upload or delete output. Keep it until the user-defined retention or disposition step.

## 5. Interpret and Corroborate

Separate raw evidence, obdiag findings, and inference. Record the rule/scene/tool version and the evidence location supporting each finding. Corroborate a suspected cause with independent runtime, SQL/API, configuration, or system evidence and check that the timing matches the incident.

Report “suggested cause” or “not confirmed” when corroboration is missing. A successful collection proves artifact production, not root cause; a clean check does not prove the incident did not occur outside its rule or time coverage.

## 6. Failure and Retry

On failure or timeout, preserve the trace/task state, partial output, free-space state, tool/config versions, and per-module results. Determine whether the collector is still running and whether retry would duplicate data, increase load, or overwrite evidence.

Do not reinstall the tool, update scenes, broaden the gather, delete partial artifacts, or repeat a high-overhead capture as generic recovery. Choose the narrowest observed-state recovery and obtain new authorization when its target, data access, or production impact changes.
