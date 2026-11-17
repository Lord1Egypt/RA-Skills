# Acceptance evidence

Use synthetic data, an isolated namespace/state directory and an independent
archive. Run local/template tests before consuming a GPU. Keep exact generated
bytes, commands and logs so the result can be reproduced.

1. Prove identity, supported authentication reuse and scheduler observation.
   A failed scheduler query must remain unknown, not become an empty queue.
   For a desktop wrapper, check literal shell syntax, spaces, Unicode, a quoted
   comma-containing argument, `run`'s `--` marker, exit status and a staged script
   larger than the desktop argument limit. Verify bytes through the actual route.
2. Submit one stable allocation request; replay it concurrently and after a
   connection interruption. Prove one Slurm job with matching owner/comment.
   Changed parameters and unrelated existing jobs must refuse another submission.
3. On a granted node, prove restore/verification, initial autosave readiness,
   current-writer health and persistent archive placement. Check a login-node
   observer cannot obtain the compute writer's lease.
   Prove the selected tmux namespace, actual disk mount/cache locations and
   application readiness through its launcher. A normal backup doctor does not
   check framework imports, CUDA compilation or worker environment inheritance.
4. Write/change/delete synthetic files, save and restore. Exercise corruption
   fallback, interrupted publication and retention with isolated fixture packs.
   Confirm `.venv` and large cache exclusions without using research checkpoints.
5. Finish the first owned probe, get a fresh local path in a second allocation,
   and prove automatic restoration. Inspect the pre-deadline save and actual
   Slurm terminal state separately from forced-timer unit checks.
6. Ask a fresh agent with no task history to use the skill and raw site evidence
   to produce a valid profile and staged bundle. Review its artifacts and decisions.
   Never count a fixture scheduler as a real GPU lifecycle test.

Use the lowest-cost eligible GPU with an available slot. If allocation is delayed
or policy denies the partition, preserve that result and mark the GPU check
pending; a successful CPU filesystem probe proves only its tested storage/lock
behavior. Do not automatically cancel or replace a research allocation.

Before adopting an existing archive, verify its chain and inspect its size/quota.
Keep the legacy bytes until a verified new generation has been published. Rehearse
the migration on an independent copy if the archive is valuable or unfamiliar;
fixture migration tests alone do not establish that a particular research archive
is usable. Report completed tests, installed hashes and remaining limits separately.
