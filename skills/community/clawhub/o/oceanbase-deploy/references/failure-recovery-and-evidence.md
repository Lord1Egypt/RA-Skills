# Failure Recovery and Evidence

Read this reference after a failure, timeout, interruption, or mixed result and before retrying, cleaning, or changing the plan.

Any proposed cleanup must also pass [cleanup and ownership boundaries](cleanup-boundaries.md). Failure recovery does not expand the original authorization or transfer ownership of residual objects.

## Freeze the Observed State

Do not assume a non-zero exit means nothing changed or that a timeout means the task stopped. Preserve:

- OBD executable/build and plugin identities;
- exact redacted command or API request and input configuration checksum;
- trace or task ID, timestamps, terminal output, task phase, and logs;
- deployment/component/tenant state before and after;
- target processes, listeners, paths, mounts, resources, and relevant component logs;
- package/repository candidates and actual installed artifact identity.

Collect only evidence needed for the failure. Route high-overhead production collection to the obdiag skill.

## Classify the Actual State

Use observed evidence to classify the target, for example:

- configured but not deployed;
- deployed but not running;
- partially running;
- running but unhealthy;
- healthy at control plane but unavailable at data plane;
- product topology changed while OBD registration remains stale or contradictory;
- timeout with server-side state unknown;
- destroyed or dropped with residual objects;
- asynchronous task accepted, running, failed, or recoverable.

Do not choose a recovery command until the state and completed stage are known.

<a id="reconcile-caller-timeouts-and-asynchronous-tasks"></a>

## Reconcile Caller Timeouts and Asynchronous Tasks

A caller timeout, lost terminal, or interrupted SSH session does not cancel an OBD or server-side task. Before retrying, use the same controller identity and resolved `OBD_HOME` to identify the original local OBD process and children, correlate its trace/task ID and time window, and query the narrowest public control-plane and domain state available. Corroborate that state with runtime and data-plane evidence such as the exact deployment/component/tenant object, processes/listeners, authenticated SQL, task rows, or storage artifacts.

Define a bounded observation deadline and classify the original invocation as exactly one of:

- **succeeded:** the intended terminal control-plane state and every required acceptance layer are present;
- **failed:** the task reached a proved failed terminal state, with partial objects inventoried;
- **still running:** the original process or task is active and remains the only authorized invocation;
- **unknown:** evidence is unavailable, contradictory, or cannot distinguish a live task from a partial result.

When the caller timed out but the exact task and target subsequently satisfy acceptance, continue from that successful state; do not report failure or submit a duplicate. When it is still running, continue bounded observation rather than launching another invocation. For failed or unknown states, freeze retries until idempotence, residual ownership, and the narrowest next action are proved. Trace text alone never supplies the terminal classification.

Treat duplicate-object, conflict, `already exists`, or `already submitted` responses after an earlier mutation as the same kind of ambiguous completion signal. They can mean that the original request succeeded, is still running, partially created the target, or collided with a pre-existing object. Correlate object identity, task ID, timestamps, ownership, and requested values; then apply the same four-state classification above. If one matching object already satisfies the complete acceptance criteria, converge on that successful state instead of retrying. If the object is stale, conflicting, or only partially complete, preserve it and define a separate recovery action; never delete or overwrite it merely to make the original command retryable.

## Choose the Narrowest Recovery

For the classified state, decide whether the safe action is to continue the original task, repair one failed target, use a documented recover operation, restore a saved configuration/artifact, roll back, or stop for operator input.

The following are never generic recovery steps:

- `redeploy` or a second deploy;
- `destroy`, tenant drop, or metadata deletion;
- `--force` or ignore-safety options;
- mirror/repository clean or broad cache deletion;
- clearing OBD environment state, locks, or stored credentials;
- editing hidden `.obd` metadata or installed plugins;
- changing unrelated network, path, resource, or kernel parameters.

If recovery would introduce a new destructive, availability, persistent-host, repository, or credential mutation, present it as a new operation and obtain its own authorization.

<a id="failed-initial-start-and-storage-topology"></a>

### Failed Initial Start and Storage Topology

When a new deployment's precheck or first start fails, separate host-environment findings from storage initialization. If the failure is limited to a reported kernel value or deployment-user limit, keep the registered configuration and initialized paths unchanged, apply only the owning public OBD host/user initializer or its exact documented fallback, verify persistence and a fresh deployment-user login, then repeat the public precheck before considering a start retry.

For `OB_NO_SUCH_FILE_OR_DIRECTORY`, a missing storage object, or contradictory path evidence, first inventory the deploy-time and current registered values for `home_path`, `data_dir`, and `redo_dir`; the deploy trace and configuration checksum; the canonical `home_path/store`, data, `sstable`, `clog`, and `slog` paths; symlink targets; owners, modes, mount identities, and contents on every server. Do not remove custom storage values, delete an empty-looking initialized directory, replace a symlink, manually create `store/{clog,slog,sstable}`, edit hidden OBD metadata, or rerun deploy merely because one of those actions can make a fresh empty instance start.

Do not infer from observer starting with `-d <home_path>/store` that the installed OBD/plugin ignores `data_dir` or no longer supports a schema-accepted `redo_dir`. That path can be the canonical entry backed by OBD-created links. Compare the version-matched initializer with the actual path graph: when custom data is configured, determine whether `<home_path>/store` resolves to `data_dir`; determine where the data-side `clog` path resolves; and verify the expected redo-side directory and `slog` placement. If `data_dir` or `redo_dir` was placed below `<home_path>/store`, report a reserved-path collision rather than a removed split-redo capability; validate direct equality separately as the possible plugin-supported direct data/single-root case. Do not retry an unchanged start or collapse data and redo onto one filesystem as diagnosis-by-workaround.

If only the registered configuration changed after a successful deploy initialization and the original initialized topology remains intact, restore the exact deploy-time path values through the installed supported configuration workflow, verify the topology, and then evaluate a start retry. If initialization itself is partial or contradictory, a newly created, uniquely owned, never-bootstrapped, data-free test deployment may be destroyed and recreated only under authorization for that exact removal set. Any existing data, bootstrap ambiguity, unknown ownership, or inability to prove the original topology requires stopping with the preserved evidence rather than reconstructing Observer storage by hand.

## Retry Rules

Before retrying:

1. resolve whether the previous operation is still active;
2. determine whether the operation is idempotent for the observed stage;
3. identify partial objects and whether the command resumes, duplicates, overwrites, or rejects them;
4. confirm inputs and repository resolution have not changed;
5. define a stop condition that prevents repeated blind attempts.

One unexplained repeated failure is enough to stop automated retries when another attempt can expand damage or ambiguity. Online package acquisition from the fixed OceanBase public mirror sources is a narrower non-mutating exception: it follows the explicit three-attempt-per-source rule below.

### Network and Artifact-Acquisition Failures

A DNS, connection, proxy, TLS, HTTP, metadata, or download failure establishes only one failed package-source attempt and observation window; it does not by itself prove that the controller has no usable network path. For every OceanBase public package, keep the selected controller and follow the [fixed artifact-source order](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order): three meaningful acquisition attempts on source 1 before source 2, then three on source 2 before advancing to another compatible suffix. Select the effective package source before varying applicable controller-local OBD/tool, `curl`, `wget`, or package-manager mechanisms. A `.repo`-definition download, operating-system repository change, or generic connectivity probe neither counts as an OceanBase package attempt nor permits a source to be skipped.

For a commercial (Enterprise Edition) database/component or standalone/centralized artifact, do not treat a community-mirror miss as an acquisition failure and do not run the public-source retry matrix. Return to the [commercial package-acquisition workflow](../obd-administration/references/mirror-and-repositories.md#commercial-package-acquisition), inspect the controller's OBD local repository, and ask the user for every exact missing file or its existing path. Do not retry through a portal, software center, support channel, relay, or other automatic download route.

After all applicable controller-local mechanisms, required source attempts, and compatible suffixes are exhausted, use another reachable host only as a bounded artifact relay for the same exact package from the same ordered sources. Verify it on the relay and again on the controller before local import/install. Do not install or run OBD on the relay, introduce a third source, or select another controller as recovery. Ask the user only when the relay also fails, an unlisted source is needed, or the exact artifact remains ambiguous.

## Report the Outcome

Separate confirmed facts, tool suggestions, and inference. State:

- which stage completed and which did not;
- current availability and data-safety status;
- residual objects or active tasks;
- evidence supporting the suspected cause;
- the narrowest safe next action and whether it needs new authorization.

An obdiag rule, log pattern, or RCA suggestion is not a confirmed root cause until it agrees with independent runtime, SQL/API, or system evidence.
