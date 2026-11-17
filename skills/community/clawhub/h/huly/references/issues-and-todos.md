# Issues & actions (todos) — the state machine

This is the most important reference in this skill. Issues and `huly action` (the CLI's name for Planner ToDos; there is no `huly todo`) are tightly coupled via server-side mixins. Most surprise-cascades happen here.

---

## Before you touch this surface: confirm the issue/project exists

```bash
# Resolve the issue ref the user gave you (or discover one)
huly issue get TSK-1 --json                  # ref form
huly issue get 1                             # if HULY_PROJECT is set
huly issue list --project TSK --json | jq '.[0]'   # discover
```

ALWAYS `--json` for any read that leads to a write. Tables hide fields you'll need.

---

## Decision: where to put new work?

| User says…                                                  | Use                              |
| ----------------------------------------------------------- | -------------------------------- |
| "create a bug", "track this", "file an issue", "bug report" | `huly issue create`              |
| "remind me to…", "task to…", "todo:", "follow up on…"       | `huly action create`             |
| "log time on…"                                              | `huly time log`                  |
| "add a comment to TSK-1"                                    | `huly comment add --issue TSK-1` |

If the user says "task" without specifying, ASK whether they mean a tracker issue (`huly issue create`) or a Planner action (`huly action create`). These are different objects. Conflating them is the most common agent mistake on this surface.

---

## Issue commands — cheatsheet

### Discover

```bash
huly issue list --project TSK --json
huly issue list --project TSK --status "In progress" --json
huly issue list --project TSK --status-category Active --json    # Active | ToDo | Won | Lost | UnStarted
huly issue list --project TSK --assignee alice@example.com --json
huly issue list --project TSK --label bug --label auth --json     # repeatable, AND'd
huly issue list --project TSK --description-search "deploy" --json # MongoDB regex, case-insensitive
huly issue list --project TSK --parent null --json                # top-level only
huly issue list --project TSK --limit 100 --offset 200 --json     # in-memory slice
huly issue get TSK-1 --json
huly issue get TSK-1 --markdown        # body as Markdown
```

### Create

```bash
huly issue create \
  --project TSK \
  --title "Set up CI pipeline" \
  --description "Migrate from Jenkins" \
  --body "## Acceptance criteria\n- Runs in <5min\n- Slack on failure" \
  --priority High \
  --assignee alice@example.com \
  --label backend --label infra \
  --due 2026-09-30T17:00:00Z \
  --parent TSK-42                # or 'parent:null' or just omit for top-level
```

Defaults the CLI silently applies (use `--minimal` or `HULY_OPINIONATED=0` to skip the opinionated ones):

| Default                     | What gets set                                                                                                                                                                                                                                                         | How to skip                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `status`                    | lowest-rank IssueStatus in category `ToDo` (usually `To do`) — NOT `Backlog`                                                                                                                                                                                          | `--status "Backlog"`, `--status "Done"`, etc.                                               |
| `priority`                  | `Medium` (alias `Normal`) or first available. **Auto-seed:** if the workspace has zero `TypeIssuePriority` records (e.g. self-hosted with `INIT_REPO_DIR=/no-init-scripts`), the 5 platform priorities are seeded into `core:space:Model` before resolution (HULY-7). | `--priority High` to override; `--minimal` / `HULY_OPINIONATED=0` to suppress the auto-seed |
| `task-type`                 | first available TaskType for the project; if none, falls back to `tracker:taskTypes:Issue` (NOT `tracker:issue:default` — that ref is invalid and the create errors)                                                                                                  | `--task-type "Story"`                                                                       |
| `parent`                    | `null` (top-level)                                                                                                                                                                                                                                                    | `--parent TSK-42`                                                                           |
| `members` (on project)      | current user added                                                                                                                                                                                                                                                    | cannot skip on `project create`                                                             |
| `description`               | `''`                                                                                                                                                                                                                                                                  | `--body "…"`                                                                                |
| `assignee`                  | **current user's email** (resolved from `getAccount().fullSocialIds`)                                                                                                                                                                                                 | `--assignee <other-email>` to override; `--assignee ''` to leave unassigned                 |
| issue number                | `$inc` the project's `sequence` field, before create                                                                                                                                                                                                                  | n/a (automatic)                                                                             |
| `--body` vs `--description` | both stored; `--body` is the rich Markdown                                                                                                                                                                                                                            | pass one or the other                                                                       |

**Opinionated defaults master switch:** the new opinionated defaults (`status` = `ToDo` category, `assignee` = current user's email) AND the pre-existing `--minimal`-gated fields (`parent: null` and `space: project._id` on `issue create`, plus `description` omission on `project create`) are all disabled by `HULY_OPINIONATED=0` (or `false` / `no` / `off`) or by passing `--minimal`. With opinionated defaults OFF, `status` reverts to the workspace's lowest-rank status overall (usually `Backlog`), `assignee` is unset (unless you pass `--assignee <email>` or `--assignee ''`), `parent` and `space` are omitted entirely from the issue payload, and `description` is omitted from `project create`. The auto-seed of `TypeIssuePriority` records (HULY-7) is also suppressed under `HULY_OPINIONATED=0` / `--minimal` — explicit `--priority X` against an empty enum then throws CLI-13 with the workspace's actual state, instead of silently fixing the model. Implicit `--priority` resolves to `Medium` when available, else the first available priority; when the enum is empty AND opinionated defaults are OFF (or `--dry-run` is set), the field is omitted from the issue entirely rather than auto-seeded. The remaining defaults that are NOT gated by `HULY_OPINIONATED` continue to apply: `task-type` resolves to the first available TaskType; the issue number is always `$inc`'d; `body`/`description` storage and the `--body` vs `--description` precedence are unaffected.

**Critical:** creating an issue with `--assignee` (or with the opinionated default assignee) while status category is `ToDo` or `Active` triggers the server-side auto-creation of a `ProjectToDo` (classic projects only). With the opinionated default ON, this fires on every `issue create` that doesn't pass `--assignee ''` because the status lands in `ToDo` AND the assignee resolves to you — see the state machine below.

**Idempotency:** if `huly issue create` returns `duplicate` / `exists` / `already`, the CLI re-fetches and returns the existing `_id`. But the issue number is NOT rolled back on that path — the next new issue still gets the next number.

### Update

```bash
huly issue update TSK-1 --status Done
huly issue update TSK-1 --assignee bob@example.com     # fires assignee cascade
huly issue update TSK-1 --title "New title"            # propagates parentTitle to children
huly issue update TSK-1 --priority Urgent
huly issue update TSK-1 --due 2026-12-31T23:59:59Z
huly issue update TSK-1 --description "…"
huly issue update TSK-1 --set customField="value"      # auto-coerced; reserved keys stripped
```

Multiple flags per call. Empty call → `nothing to update`.

### Move (set parent)

```bash
huly issue move TSK-1 --parent TSK-42
huly issue move TSK-1 --parent null                   # drop parent (top-level)
huly issue move TSK-1 --parent -                      # same as null
```

`huly issue move` does NOT change the project — issues cannot be moved across projects via the CLI (the SDK has no method for this). To "move" between projects, see the bulk-migrate recipe at the bottom of SKILL.md.

### Labels

```bash
huly issue label TSK-1 add bug
huly issue label TSK-1 add auth
huly issue label TSK-1 remove bug
```

Adding a label that doesn't exist yet auto-creates a `TagElement` in `tags:space:Tag` (don't be surprised).

### Relations

```bash
huly issue relation add    TSK-1 --type blocks       --target TSK-2
huly issue relation add    TSK-1 --type isBlockedBy  --target TSK-2
huly issue relation add    TSK-1 --type relatesTo    --target TSK-2
huly issue relation remove TSK-1 --type blocks       --target TSK-2
huly issue relation list   TSK-1                       # shows blocks + isBlockedBy + relatesTo
```

`--type` and `--target` are both required. Types are exactly `blocks | isBlockedBy | relatesTo` (case-sensitive on parse). `add` does NOT dedupe — duplicates will both be stored.

### Document linking

```bash
huly issue link-document TSK-1 <doc-ref-or-title>
huly issue unlink-document TSK-1 <doc-ref>
```

Documents and issue-relations both live in the issue's `relations` array; distinguished by `_class`. Link only once; `link-document` warns and no-ops on duplicate.

### Preview / delete

```bash
huly issue preview-delete TSK-1        # show subIssues / comments count / relations
huly issue preview-delete TSK-1 TSK-2  # multiple
huly issue delete TSK-1 --yes          # single, no prompt
huly issue delete TSK-1 TSK-2 --yes    # multiple, REQUIRES --yes
```

`preview-delete` is your friend. ALWAYS run it before bulk delete. The cascade (comments, sub-issues deletion) happens server-side — no undo.

---

## Comments (issue comments are ChatMessages on the issue)

```bash
huly comment list --issue TSK-1 --json
huly comment add --issue TSK-1 --body "Looking into this" --json
huly comment add --issue TSK-1 --body-file ./note.md
huly comment update <comment-ref> --body "Edited text"
huly comment delete <comment-ref>...    # --yes for ≥2
```

Side effects on `comment add` (server-side, not the CLI):

- Author auto-added as `Collaborator` on the issue
- Every `@mention` in body parsed → inbox notification per collaborator + per mention
- An `ActivityMessage` is emitted, appears in `huly activity list`

---

## Time tracking

```bash
huly time list --issue TSK-1 --json
huly time list --start 2026-06-01 --end 2026-06-30 --json
huly time log --issue TSK-1 --minutes 30 --description "wired up CI"
huly time log --issue TSK-1 --hours 2 --description "pair prog"
huly time report TSK-1                    # alias for `time list --issue <ref>`, per-issue only
huly time delete <entry-ref>... --yes
```

**Critical side effect:**

- The CLI stores time as **man-hours** (`value = minutes / 60`).
- `time log` updates `reportedTime` and recomputes `remainingTime` on the issue.
- **If the issue has a parent issue, the recompute walks UP the parent chain.** No opt-out.
- `time report <ref>` is per-issue only — there is no workspace rollup command. For aggregates, use `time list --start … --end … --json` and jq:

```bash
huly time list --start "$(date -u +%Y-%m-%dT00:00:00Z)" --json --limit 1000 \
  | jq --arg since "2026-06-01" '[.[] | select(.date >= ($since | fromdateiso8601 * 1000))]'
```

**Gotcha:** passing both `--minutes` and `--hours` throws `Validation: pass only one of --minutes or --hours` (`resources/time.ts:86-88`). Pick one.

---

## Actions (`huly action` — the only name; NOT `huly todo`)

There is NO `huly todo` command in the current build. The CLI exposes Planner todos under `huly action`. The `todo.ts` source file is named that way for historical reasons.

### Discover

```bash
huly action list --owner alice@example.com --json
huly action list --issue TSK-1 --json
huly action list --title "deploy" --json              # MongoDB regex
huly action list --priority High --json
huly action list --visibility public --json           # public | busy | private
huly action list --due-from 2026-07-01 --due-to 2026-07-31 --json
huly action list --completed false --json              # false | true | all
huly action list --completed all --json               # both
huly action get <ref> --json
huly action get <ref> --markdown                      # body
```

### Create

```bash
huly action create --title "Send weekly report" --due 2026-07-05T17:00:00Z
huly action create --title "Fix login bug" --owner alice@example.com --priority High
huly action create --title "Plan sprint" --body "…"
huly action create --title "…" --attached-to TSK-1 --attached-to-class tracker:class:Issue
```

Strict enums on write:

- `--priority` ∈ `Urgent | High | Medium | Low | NoPriority` (case-SENSITIVE — `NoPriority` is one word)
- `--visibility` ∈ `public | busy | private` (case-SENSITIVE)

If you pass an invalid value: `Validation` error.

### Update / complete / reopen

```bash
huly action update <ref> --title "…" --priority Urgent
huly action complete <ref>                              # sets doneOn=now
huly action reopen <ref>                                # clears doneOn
```

`reopen` does NOT restore removed WorkSlots. If the issue's status was auto-advanced by `IssueToDoDone`, the user must `huly issue update --status <previous>` to roll back manually.

### Schedule / unschedule

```bash
huly action schedule <ref> --start 2026-07-05T14:00:00Z --duration 60
huly action schedule <ref> --start 2026-07-05T14:00:00Z --duration 60 --all-day
huly action unschedule <ref>                            # remove ALL slots
huly action unschedule <ref> --slot-id <slot-id>        # remove ONE
```

**Destructive guard:** `unschedule` with multiple slots and no `--yes` throws `Validation`. Single slot via `--slot-id` is allowed without `--yes`.

### Delete

```bash
huly action delete <ref> --yes
```

`OnToDoRemove` cascade: if this was the LAST open todo on its attached issue, the issue's status rolls back to the previous un-started state (classic projects only).

---

## The Issue ↔ Action state machine (read this section carefully)

ALL of the following happen server-side via mixins on classic projects (`ProjectType.classic = true`, the Tracker default; Recruit and Lead projects are NOT classic). There's no client-side CLI toggle.

### Creates

| Your command                                                                      | Server does                                                                                       |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `huly issue create --assignee <email>` when status is `ToDo` or `Active` category | Auto-creates `ProjectToDo` for the assignee + sends inbox notification.                           |
| Same, but status is `Backlog`, `Done`, or `Canceled`                              | Nothing. **Category matters, not literal name.**                                                  |
| `huly issue update --assignee <new>` while issue has open todos                   | Closes existing assignee's open todos (`doneOn=now`), creates new `ProjectToDo` for new assignee. |
| `huly issue update --status Done\|Canceled`                                       | All open todos on this issue get `doneOn=now`.                                                    |
| `huly issue update --status ToDo\|Active` on a todo-less assigned issue           | Creates the FIRST `ProjectToDo`.                                                                  |

### Action → Issue

| Your command                                                                  | Server does                                                                                                     |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `huly action complete <ref>` (last open todo on its issue)                    | Auto-advances issue status past the last `Active` state, via `IssueToDoDone` mixin.                             |
| `huly action schedule <ref>` (first WorkSlot, issue status = Backlog or Todo) | Auto-advances issue status to the next `Active` state, via `OnWorkSlotCreate`.                                  |
| Subsequent WorkSlots on the same action                                       | None (already in Active state).                                                                                 |
| `huly action unschedule <ref>`                                                | Removes WorkSlots. **Does NOT roll back status.** Only `OnToDoRemove` (i.e. `action delete`) triggers rollback. |
| `huly action reopen <ref>` after IssueToDoDone advanced the status            | Status stays advanced. User must `huly issue update --status <previous>` manually.                              |
| `huly action delete <ref>` (was the last open todo on the issue)              | Auto-rolls back issue status to the previous un-started state.                                                  |
| `huly action update --title\|--description\|--visibility`                     | Mirrors to all WorkSlots of that todo (`OnToDoUpdate` → `OnWorkSlotUpdate`).                                    |
| `huly action update --priority` or `--due`                                    | NOT mirrored to WorkSlots.                                                                                      |

### Issue → everything

| Your command                                               | Side effect                                                     |
| ---------------------------------------------------------- | --------------------------------------------------------------- |
| `huly issue update --title "New"` on issue with sub-issues | Propagates new title into each sub-issue's `parentTitle` field. |
| `huly time log --issue <ref>` on issue with parent         | Walks parent chain recompute (`OnIssueUpdate`). **No opt-out.** |

### Status categories

`UnStarted | ToDo | Active | Won | Lost`

- `ToDo` and `Active` cause `ProjectToDo` creation (combined with `--assignee`).
- `Won` (typically `Done`) and `Lost` (typically `Canceled`) cause open todos to close.
- `UnStarted` (typically `Backlog`) does neither.

**Opinionated default:** `huly issue create` without an explicit `--status` lands the new issue in the lowest-rank status of category `ToDo` (usually `To do` / `Todo`). Pin to `Backlog` with `--status Backlog`. Disable with `--minimal` or `HULY_OPINIONATED=0`. This is intentional — combined with the opinionated default `--assignee <current-user-email>`, it means a bare `huly issue create --project X --title "…"` fires the full ProjectToDo cascade. To suppress that, pass `--assignee ''` (explicit empty string) — empty is treated as "no assignee", distinct from "not specified".

Filter with `--status <label>` (case-insensitive exact on label/name) or `--status-category <UnStarted|ToDo|Active|Won|Lost>` (the accepted-value list is case-sensitive, but matching against stored categories is case-insensitive).

### Verify what cascaded

After any state change, the right way to confirm:

```bash
huly issue get TSK-1 --json                         # status, assignee, etc.
huly action list --issue TSK-1 --completed false --json   # open todos
huly action list --issue TSK-1 --completed true --json    # closed todos
```

---

## The dual-parent trap (read before creating `huly action` on an issue)

Server-auto-created `ProjectToDo`s (e.g. those from `--assignee` cascades) use `createTxCollectionCUD` and live under **both** the issue's `todos` collection AND the assignee's `time:space:ToDos` personal index. **CLI-created actions are single-parent** — the true dual-parent shape is not reproducible in one CLI call.

| Shape                   | Lives in                                                              | Created by                                                                                                                                |
| ----------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Dual-parent             | issue's `todos` collection AND assignee's personal `time:space:ToDos` | Server mixin (`createTxCollectionCUD`) — not CLI-reproducible                                                                             |
| Single-parent on issue  | issue's `todos` collection only                                       | `huly action create --attached-to TSK-1 --attached-to-class tracker:class:Issue`                                                          |
| Single-parent on Person | assignee's personal `time:space:ToDos` only                           | `huly action create` with no `--attached-to` (defaults to current user's `account.uuid`, or resolved Person `_id` if `--owner` is passed) |

To make a CLI-created action appear in the assignee's personal todo list, omit `--attached-to` entirely so the todo attaches to the Person doc. To get the action under BOTH the issue's `todos` and the assignee's personal list (the server's dual-parent shape), you need to create two separate actions.

**Practical:** if you `huly action create --attached-to TSK-1 --attached-to-class tracker:class:Issue` without `--owner`, the assignee's inbox gets NO notification and the action does NOT show in their personal todo list. Add `--owner alice@example.com` to a second call to attach a personal-list copy, or omit `--attached-to` to attach to the current user instead of the assignee.

---

## Common task recipes

### Create an issue and assign to a person in one shot

```bash
# Find the assignee
huly user find alice@example.com --json
# {"personUuid": "<alice-id>", "source": "account"}

# Create + assign (in classic projects, this auto-creates the first ProjectToDo)
huly issue create --project TSK --title "Migrate to k8s" \
                  --priority High --assignee alice@example.com
```

After this, verify the cascade:

```bash
huly action list --issue TSK-<new> --json | jq length  # should be 1 in classic projects
```

### "Move to Done" workflow

```bash
# First, see what's open on it
huly issue get TSK-1 --json | jq '{title, status, assignee}'
huly action list --issue TSK-1 --completed false --json

# Confirm with the user — moving to Done closes all open todos
huly issue update TSK-1 --status Done

# Verify
huly action list --issue TSK-1 --completed false --json  # should be []
```

### Bulk-archive done issues via reparent (reversible)

```bash
huly issue list --status-category Won --limit 1000 --json \
  | jq -r '.[]._id' \
  | xargs -I{} huly issue move {} --parent null
```

Note: `huly issue move` accepts only `--parent`; it does NOT accept `--yes` (the flag is silently ignored if passed).

### Find orphan sub-issues (issue with deleted parent)

```bash
# Issues whose parent's title doesn't resolve
huly issue list --json \
  | jq -r '.[] | select(.parent != null) | "\(._id) parent=\(.parent)"'
# then for each, check parents[] chain manually
```

### Audit trail for an issue

```bash
huly ws findAll '["core:class:Tx",{"objectId":"<issue-id>","modifiedOn":{"$gte":<start-ms>,"$lte":<end-ms>}}]' \
  --json \
  | jq '[.[] | {by: .modifiedBy, on: .modifiedOn, ops: .attributes, _class}]'
```

---

## Gotchas (don't do this)

- **Don't** try `huly todo …` — that command doesn't exist. Use `huly action …`.
- **Don't** assign with `--assignee bob` when there's both `Bob Anderson` and `Bob Bishop`. The substring fallback picks the first match in `findAll()` result order (not alphabetical). Pass full email.
- **Don't** `--owner bob` and expect substring fallback. `--owner` is exact-match only. Pass full name or email.
- **Don't** mix `--priority` strict enums between issue and action. Issue priority is loose (`Urgent | High | Medium | Low | NoPriority`, with `--priority Normal` and `--priority None` accepted as aliases); action priority is strict (and `NoPriority` is one word).
- **Don't** delete the last open todo without expecting the issue to roll back. Verify with `huly action list --issue <ref> --completed false`.
- **Don't** pass `--rrule` to time tracking — there's no recurrence; `--due` is one-shot.
- **Don't** expect `huly issue move` to change the project's `space` (project). It only changes `parent`. Cross-project moves require copy+delete.
- **Don't** try `action --set` — actions don't accept `--set key=value`. Use the typed flags (`--priority`, `--visibility`, `--owner`, `--title`, `--description`, `--body`, `--due`).
- **Don't** assume the project's project-type is classic. Run `huly project-type get <ref>` if you need to confirm; Recruit/Lead projects disable cascades.
- **Don't** pass `--body` AND `--body-file`. Mutually exclusive (`Validation: ambiguous body input`).
- **Newlines in `--body` / `--description` are auto-stripped.** The CLI's `normalizeMarkupInput` strips newlines (and adjacent whitespace) before the prosemirror parser runs, so `<h1>Title</h1>\n<p>Body</p>` round-trips cleanly into one heading and one paragraph with no phantom empty paragraphs. (Earlier versions warned against embedded `\n`; that restriction is now lifted.)
- **Nested HTML must be properly nested, not flat.** A nested list needs `<li>...<ul><li>...</li></ul></li>`, not `<li>...</li><ul><li>...</li></ul>`. The prosemirror parser validates structure and silently drops malformed siblings — same applies to blockquotes in lists, code blocks in table cells, etc.
- **`--status` errors if the status doesn't exist.** `huly issue create --status "Bogus"` throws with the list of available statuses. Same for `--priority` and `--task-type`.
- **`--status-category` (UnStarted | ToDo | Active | Won | Lost)** picks the lowest-ranked status in that category from the project's IssueStatus records. Available on `issue list`, `issue create`, and `issue update`.
- **`--kind <ref>`** overrides the default TaskType. Default is the project's first available TaskType (or `tracker:taskTypes:Issue` as final fallback, validated via `findOne`).
- **`--raw-markup` is read-only.** Use it on `issue get` / `document get` / `card get` / `document snapshot` to dump raw prosemirror-JSON. Using it on `issue create` / `issue update` returns `unknown option`.
