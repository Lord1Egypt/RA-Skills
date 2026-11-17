# Clawpatch-aware malp work

Use this reference when a target project contains `.clawpatch/`, when the user asks a malp to treat clawpatch findings as a FOB, or when clawpatch findings need reachability/plausibility triage.

## Purpose

`.clawpatch/` is reconnaissance input, not an automatic work queue. A malp should use it as a conceptual FOB only when it helps the current operation.

The reusable workflow belongs here, not in each repo malp. Repo malps should record only local judgments, current finding IDs, reachability context, and decisions.

## Default stance

- Treat clawpatch findings as candidate defects.
- Preserve exact finding IDs, titles, statuses, and commands.
- Before recommending a DevOps item or PR, filter each finding through plausibility-to-recreate.
- Distinguish these cases explicitly:
  - ordinary browser/user workflow reachable
  - reachable only by direct route URL, synthetic request, or hidden/mounted surface
  - API/model defect with endpoint ownership unclear
  - real defect in likely dead or currently unmounted code
  - risk/semantic smell with no concrete reproduction yet
- Do not call a real defect `false-positive` merely because the current app does not expose it.
- Prefer `wont-fix` or `uncertain` when the key issue is reachability, not correctness.

## CLI use

Only use `clawpatch` when it exists and the target repo appears to be the correct cwd.

Useful commands:

```bash
clawpatch next
clawpatch show --finding <finding-id> --json
clawpatch triage --finding <finding-id> --status <status> --note "<note>"
```

Status choice is contextual. Common meanings in malp triage:

- `open` — keep in the fix queue.
- `uncertain` — technically plausible or valid, but reachability/impact needs confirmation.
- `wont-fix` — valid or plausible finding, but current evidence says it should not become active work now, often because the path is dead/unmounted/unjustifiable.
- `false-positive` — the tool is wrong about the defect itself, not merely unable to know reachability.

After triage, `clawpatch next` may return the next still-open finding. If a finding remains open, note that it can block ordinary `next` workflow.

## Review-pass operating notes

Treat clawpatch as a repo-local scout whose model of the codebase can lag behind active work. If a review result seems inconsistent with the visible diff or with files that were just added, refresh the map before trusting the result:

```bash
clawpatch map --source heuristic --skip-git-repo-check
```

Then rerun either a bounded review (`clawpatch review --limit <n>`) or targeted feature reviews. Targeted reviews are useful when the current question is scoped to one subsystem and a broad review pulls in unrelated areas:

```bash
clawpatch review --feature <feature-id>
```

Treat reports as cumulative/overlapping evidence, not a clean current-open list. A report may include older findings, fixed findings, uncertain findings, and duplicate/new wording for the same underlying defect after a remap. For current state, prefer `clawpatch status --plain` plus the finding records under `.clawpatch/findings/` or `clawpatch show --finding <id> --json`.

When a new finding overlaps an already-known gap, preserve the new finding ID, triage it explicitly, and say whether it is duplicate/superseding wording, newly actionable, or in-progress scaffold debt.

If the worktree contains unrelated dirty files, avoid using clawpatch fix as an automatic lander unless its clean-worktree preconditions are satisfied and the slice is clearly isolated. Manual fixes can still be made, tested, staged by exact path, and committed as a narrow slice.

## What to write into `.malp/`

When clawpatch is materially shaping the work, update `FOB.txt` with a terse tactical snapshot:

- `.clawpatch/` as the current conceptual FOB
- active finding IDs/titles
- the plausibility-to-recreate rule
- current reachability judgments
- next verification front

Use `NOTES.txt` for durable repo-specific lessons, open questions, or decisions. Avoid storing generic clawpatch CLI instructions there; link the local decision back to this skill behavior instead.

## Reachability triage checklist

For each finding, answer only as much as needed:

1. What exact code/file/symbol did clawpatch flag?
2. Is the defect technically valid in that local code?
3. Is there an ordinary user/browser path to exercise it?
4. If not, is there a direct route/API/synthetic path?
5. Is the backend endpoint or owner present in this repo snapshot?
6. Would a reproduction require unrealistic setup, stale routes, or dead code?
7. What status best communicates the gap between correctness and actionable work?

The best output is usually a concise recommendation plus the exact triage command, not a broad source tour.
