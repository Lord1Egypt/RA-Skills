# Operating lessons from the reference sites

Read this when adapting a desktop transport or preparing and observing real
work. These lessons come from the maintained MSI/PSC installation; site-specific
versions, quotas and paths must still be established for the new site.

## Connection identity and tmux routing

Shared home does not imply shared processes, sockets or temporary directories.
Pin the login node when it owns a transport or allocation tmux. Record the host
alongside the socket/session; a service found in shared home may belong to a
different login node. Verify actual remote identity after authentication.

On PSC, a separate SSH connection to the same compute hostname can see a
different `/tmp` namespace and miss the allocation's tmux socket. Use the existing
allocation bridge for commands, window inspection and snapshots. For another
site, prove its compute route within the allocated context before choosing
`direct-ssh`. Always bind dispatch to the intended job and verify its identity;
do not select the first visible GPU when several jobs exist.

The outer tmux owns allocation; compute tmux owns tasks. Keep setup/autosave
windows protected. The generated configuration uses `Ctrl-b` outside and
`Ctrl-a` inside. A reconnect must preserve the existing hierarchy, task IDs and
logs. Repeated bootstrap must not replace an existing session.

## Desktop arguments and file transport

Treat command arguments literally. Expand variables, globs, pipes and redirects
only in an explicitly requested remote shell, such as `bash -c '...'`. Never
evaluate remote syntax in the desktop shell. In PowerShell, quote a whole
comma-containing argument such as `'--format=JobID,State,ExitCode'`. A `.ps1`
wrapper may consume `--`; the native run wrappers restore it after the explicit
window name. This behavior must be implemented and tested in a new wrapper.

Preserve UTF-8 script bytes and binary file bytes; use stdin or the existing
`exec`/`push` bridge for large scripts rather than Windows command arguments.
The bridge is a deployment transport, not a complete desktop command wrapper.
Some login nodes disable SFTP/SCP while SSH exec works: probe the actual transfer
route and use a supported data-transfer node for large files when site policy
requires it. Verify staged bytes before execution or atomic replacement.

Login banners and module warnings can precede structured output. For these
helpers, parse the final JSON record and validate its schema/site/job identity;
also preserve the process exit status and diagnostic lines. Do not parse all
stdout as one JSON document or accept a JSON-looking warning as success. If a
PowerShell wrapper is edited, run its AST syntax check before using the route.

## Repository launchers and compute readiness

`nvidia-smi` establishes driver/GPU visibility, not an installed CUDA compiler.
Probe the workload's actual Python environment, CUDA frontend and host compiler
on compute. A CUDA runtime wheel or `ptxas` alone does not establish `nvcc`.
Use a small import/build/GPU smoke check through the repository's launcher.

The launcher owns locked environment recreation, framework variables and
compiler modules. Set `VIRTUAL_ENV` and prepend its `.venv/bin` to `PATH` so
Ray/JIT subprocesses can also find tools such as `ninja`. Avoid loading a compiler
module into every task unless that site deliberately requires it: a changed
`libstdc++` can affect unrelated repositories. Preserve a toolkit setup failure
as a workload limitation; allocation/snapshot READY is not application readiness.

For private sources, reuse the configured credential mechanism. Noninteractive
Git steps should fail promptly with `GIT_TERMINAL_PROMPT=0`; missing credentials
must not leave a controller waiting for invisible input. Record actual revisions
and submodule revisions. After interruption, inspect local edits before replacing
or force-updating a checkout. A restored workspace may be the only surviving
source copy; preserve it before synchronizing with upstream.

Before a long run, validate its configuration/imports through the same launcher.
Warm up JIT-dependent benchmarks before timing; keep startup compilation logs
separate from measured results. Do not submit another GPU to fix an application
startup error while its original allocation remains available.

## Scratch, caches and storage budgets

Inspect the allocated path with `findmnt -T PATH` or the site's equivalent.
`/tmp` can be a job-specific disk mount; a path name alone does not prove disk
or RAM backing. Conversely, unrequested temporary space can count against memory.
Verify job isolation, mount, writability, capacity and inodes on compute.

Keep environment and uv cache on the same local filesystem when using hardlinks.
Also place model/dataset and compilation caches there through explicit repository
configuration: `HF_HOME`, `HF_HUB_CACHE`, `HF_DATASETS_CACHE`, `TORCHINDUCTOR_CACHE_DIR`,
`TRITON_CACHE_DIR`, `CUDA_CACHE_PATH` and `TMPDIR` as applicable. The generic direct
boot sets the workspace and uv cache; it does not configure every framework.
Confirm cache exclusions and actual output paths rather than relying on defaults.

Persistent storage can enforce project-wide byte and inode quotas. Budget for
the live local tree, staging pack, retained backup families and any extracted
mirror. A configured results path does not rewrite an application's checkpoint
option. Pass persistent output paths explicitly and verify a complete checkpoint
before calling it resumable. Capacity/quota probing is part of site acceptance;
the current automatic home-budget check is MSI-specific, not a universal quota
provider. Do not make the MSI budget or site quota a default for other clusters.

## Observe the requested job through completion

Record requested and granted resources separately. Queue RUNNING, bootstrap
READY, current backup health, application startup and experiment completion are
different observations. `squeue` absence is not a terminal outcome: reconcile
with the exact job's `sacct` record, owner and exit status. Delayed/unavailable
accounting leaves the result unknown; preserve the request and task evidence.

For an allocation-only watch, observe that job and stop when the requested state
is reached or it terminates. Use a quiet, site-appropriate cadence; the source
workflow uses five minutes for queue watches. Notify on a meaningful transition,
failure or required action. Inspecting experiments, resubmitting, authentication
and cancellation require their own task scope. A user stop revokes that watch;
old authorization must not restart it.

## Local capabilities not yet exported

The reference installation also has a PSC browsable snapshot mirror and an
opt-in recipe controller that waits, deploys and starts experiments while the
desktop is offline. Neither helper is distributed in the public kit today.
The generated PSC profile explicitly disables the mirror. Do not advertise or
invoke `SITE mirror` or `SITE launch` as public commands.

A future mirror must read a pinned, verified committed generation, remain
separate from restore authority, exclude rebuildable caches and enforce both
capacity and ownership boundaries. An optional mirror failure must not tear
down an otherwise healthy allocation. A recipe controller must use the existing
request/task identity and dispatch paths, retain failures, fail before expensive
work when possible, and avoid automatic allocation/training retries.
