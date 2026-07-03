---
name: huly-cli
description: Drive a self-hosted Huly workspace through the `huly` CLI — issues, projects, cards, documents, calendars, channels, DMs, actions/todos, time tracking, notifications, and approvals. Use this skill for ANY Huly mutation or read that should not require a browser.
---

# huly-cli skill

This skill teaches you how to drive a self-hosted Huly workspace through the `huly` CLI instead of a browser. The CLI wraps the Huly SDK over WebSocket RPC. Most platform behaviors (cascade side effects, auto-creations, mixin triggers) fire whether the action came from you or the web UI — so this skill is mostly about **knowing which side effect will fire, and choosing the right command to get the result you want**.

---

## The 7 rules. Read these first.

1. **Verify before you mutate.** Run `huly whoami` to confirm the workspace, and `huly <surface> list --json | jq` to discover refs when they aren't given to you explicitly. NEVER guess a ref, person, or status name.

2. **Use `--json` for every programmatic read.** Tables are for humans. If you're piping, branching, or capturing an `_id`, use `--json` (or equivalently `--ci`). The CLI also auto-enables JSON when `CI=1`.

3. **Prefer Cards over Documents for new knowledge content.** When the user says "create a doc", "write down...", "save this...", default to `huly card create` — UNLESS they explicitly ask for nested hierarchy, versioned snapshots, controlled-document/e-signature workflow, or training. See `references/cards.md` vs `references/documents.md`.

4. **The Issue ↔ Action state machine is one machine.** Changing an issue's status or assignee auto-creates/closes `ProjectToDo` records. Completing/scheduling/deleting an `action` (todo) can auto-advance or auto-rollback the parent issue's status. This is the most common silent cascade you will hit. See the diagram below.

5. **Don't use destructive verbs without checking first.** Run `huly <surface> get <ref> --json` or the surface's `preview-` verb if it has one, then ask the user before proceeding. Bulk deletes (`<ref...>` with 2+ refs) require `--yes`.

6. **Ask, don't guess, when context is missing.** Workspace name, project identifier, person email, exact ISO timestamp — none of these can be inferred. If the user gave you one but not the others, ask.

7. **Reach for `huly ws` only when the CLI falls short.** The CLI covers ~95% of use. Use `huly ws <method>` for raw RPC when a flag is missing, when you need fulltext search, or when you need to query the tx audit log.

---

## Decision: which surface?

When the user asks you to do something, pick the right top-level command first. The order below is "from most likely to be correct":

| User intent | Surface | Reference |
|---|---|---|
| create / list / update / comment on a tracker item | `huly issue …` | `references/issues-and-todos.md` |
| create / list / update a Planner task / todo | `huly action …` (NOT `huly todo` — that doesn't exist) | `references/issues-and-todos.md` |
| log time on an issue | `huly time …` | `references/issues-and-todos.md` |
| create a project / tracker bucket | `huly project …` | `references/tracker-projects.md` |
| create / update a component, milestone, or issue template | `huly {component,milestone,issue-template} …` | `references/tracker-projects.md` |
| post in a channel; send a DM | `huly {channel,dm} …` | `references/chat-and-collaboration.md` |
| reply to a message thread | `huly thread …` | `references/chat-and-collaboration.md` |
| react, pin, save, view mentions | `huly activity …` | `references/chat-and-collaboration.md` |
| create a CARD (default for "doc"/"page"/"note") | `huly card …` | `references/cards.md` |
| create a DOCUMENT (nested wiki, snapshots, controlled) | `huly document …` | `references/documents.md` |
| create a calendar event (one-off or recurring) | `huly calendar …` | `references/calendar-and-schedule.md` |
| create an owner-availability schedule | `huly schedule …` | `references/calendar-and-schedule.md` |
| create / inspect a workspace, project type, task type, status | `huly {workspace,project-type,task-type,issue-status} …` | `references/spaces-types-and-relations.md` and `references/workspace-and-user.md` |
| create / inspect / reply to an approval request | `huly approval …` | `references/notifications-and-approvals.md` |
| read / mark / subscribe to inbox notifications | `huly notification …` | `references/notifications-and-approvals.md` |
| log in / check identity / look up a user by email | `huly {login,whoami,user} …` | `references/auth-and-setup.md` and `references/workspace-and-user.md` |
| something the CLI doesn't expose | `huly ws …` or `huly api …` | `references/escape-hatches-and-internals.md` |

---

## Connection & authentication (the 5-second version)

Every `huly` invocation is a fresh WebSocket connection — there is NO connection pooling and NO auto-reconnect.

```bash
# Confirm what's logged in
huly whoami --json

# Headless login (CI / agent)
HULY_URL=https://huly.example.com \
HULY_EMAIL=alice@example.com \
HULY_PASSWORD=… \
huly whoami

# Or use a pre-issued JWT (preferred for service accounts / agents)
HULY_URL=https://huly.example.com \
HULY_TOKEN=eyJ0eXAiOiJKV1Q… \
huly --workspace production issue list

# Force a specific workspace for a single command
huly --workspace production issue list --json
```

There is **no `huly logout` command**. To clear credentials:

```bash
rm -f ~/.config/huly/credentials.json \
      ~/.config/huly/active-workspace \
      ~/.config/huly/active-account
unset HULY_TOKEN HULY_EMAIL HULY_PASSWORD HULY_WORKSPACE
```

All three files are mode 0600. This is intentional — see `references/auth-and-setup.md` for why.

Full env var cheat sheet and the auth-state machine: `references/auth-and-setup.md`.

---

## Output modes — when to use which

| You want to… | Use | Returns |
|---|---|---|
| Read interactively (human) | default (table) | Auto-sized columns, hidden boring fields |
| Pipe to `jq` / `xargs`, capture an `_id`, branch on data | `--json` (or `--ci`) | Raw arrays / objects |
| Read the body of a doc/comment/message as markdown | `--markdown` | Raw string. Has a 5s timeout fallback. |
| See exactly what a write would do before committing | `--dry-run` | Prints the would-be tx JSON, no side effects |
| Skip smart defaults (no auto-teamspace, no auto-issueStatus seeding) | `--minimal` | Lean writes |

`--ci` is an alias for `--json` today, but signals intent — use it in scripts so future maintainers know you meant "no prompts".

---

## Ref resolution — the 6-step order (read once)

When you pass a positional `<ref>` (e.g. `huly issue get TSK-1`), the CLI tries these in order (`transport/ref-resolver.ts:106-140`):

1. Looks like a raw `_id`? — either matches `^[a-z0-9]+:[a-z0-9]+:[A-Za-z0-9_-]+$` (e.g. `tracker:class:Issue`) **or** is a 16+ char opaque token → use as-is.
2. Index lookup (cached per `PlatformClient` via `WeakMap`).
3. Prefixed form `^[A-Z][A-Z0-9]+-\d+$` like `TSK-12` (requires 2+ chars before the dash) → look up by composite key.
4. Bare digits with `HULY_PROJECT` set → composes `${HULY_PROJECT}-${N}`.
5. Lowercased-title lookup.
6. Throw `NotFound` with the first 10 candidates as a hint.

**Critical:** the cache is invalidated after every write to the same class. Cross-class writes in the same process may see stale refs — restart the process, or run any write to the changed class to force refresh.

For ref-accepting FLAGS (`--assignee`, `--owner`, `--person`), there's a separate algorithm with one critical asymmetry: **`--assignee` has a substring fallback. `--owner` does NOT.** Always pass the full email or full name to `--owner`. (`--calendar` has its own resolver — see `references/escape-hatches-and-internals.md`.)

Full algorithm and edge cases: `references/escape-hatches-and-internals.md`.

---

## The Issue ↔ Action state machine (the most important thing in this skill)

This is the cascade everyone hits and nobody expects. ALL of these run server-side via mixins on `tracker:class:Issue` (only when `ProjectType.classic = true` — the default for new projects; Recruit and Lead projects are NOT classic):

| You do this | Server does this | What's affected |
|---|---|---|
| `huly issue create --assignee <email>` while status category is `ToDo` or `Active` | Auto-creates `ProjectToDo` for the assignee | Assignee gets an inbox notification; todo is schedulable |
| `huly issue create --assignee <email>` while status is `Backlog`, `Done`, or `Canceled` | Nothing | No todo. Status category matters, not literal name. |
| `huly issue update --assignee <new>` | Closes all open todos on the issue (`doneOn = now`), creates a new todo for the new assignee | The previous assignee's todos are preserved as historical records with `doneOn` set |
| `huly issue update --status Done\|Canceled` | Closes all open todos on the issue | Todos survive with `doneOn` set |
| `huly issue update --status ToDo\|Active` on a todo-less assigned issue | Creates the first `ProjectToDo` | First cascade creation |
| `huly action schedule <ref>` (first WorkSlot on an issue-attached todo) | Auto-advances issue status to next `Active` state | Only if issue is currently Backlog/Todo |
| `huly action complete <ref>` (completes the LAST open todo) | Auto-advances issue status past the last `Active` state | Classic projects only |
| `huly action delete <ref>` (deletes the LAST open todo on an issue) | Auto-rolls back the issue status to the previous un-started state | Classic projects only |
| `huly action unschedule <ref>` | Removes WorkSlots but does NOT roll back status | Only `OnToDoRemove` (i.e. `action delete`) triggers rollback |
| `huly action update --title\|--description\|--visibility` | Mirrors to all WorkSlots of that todo (`OnToDoUpdate` → `OnWorkSlotUpdate`) | Same change on the calendar event |
| `huly time log --issue <ref>` on an issue with a parent | Walks up the parent chain and recomputes `reportedTime` / `remainingTime` | No opt-out |

**WorkSlot visibility mirror goes the other way too:** changing a WorkSlot's visibility mirrors back to the todo via `OnWorkSlotUpdate`.

### Status categories

`UnStarted | ToDo | Active | Won | Lost`. Use `--status-category` to filter, or `--status <name>` to filter by exact label. `--status` matching is case-insensitive on the label/name; `--status-category` accepts the literal enum values listed above (case-sensitive on parse), but matching against stored categories is case-insensitive.

### The dual-parent trap

When the server auto-creates a `ProjectToDo` (e.g. via issue update), it uses `createTxCollectionCUD` and the todo lives under **both** the issue's `todos` collection and the assignee's `time:space:ToDos` index. A CLI-created todo via `huly action create --attached-to <issueRef> --attached-to-class tracker:class:Issue` is a **single-parent** `addCollection` — it appears under the issue but NOT in the assignee's personal list unless you also pass `--owner <email>`.

The server's true dual-parent shape is **not reproducible in a single CLI call**. To make a CLI-created action appear in the assignee's personal todo list, omit `--attached-to` entirely. The CLI then sets `attachedTo` to the current user's `account.uuid` (when `--owner` is also omitted) or the resolved Person's `_id` (when `--owner` is passed), with `attachedToClass: contact:class:Person`. The result is single-parent on the Person — it puts the todo in the user's personal list and links it into the `time:space:ToDos` index, but does NOT add it to the issue's `todos` collection. To get it under the issue as well, create two actions: one with `--attached-to <issueRef> --attached-to-class tracker:class:Issue` and one with `--attached-to <personRef> --attached-to-class contact:class:Person`.

---

## Default behaviors the CLI silently applies

The CLI is opinionated. When you don't specify, it does:

| Trigger | What happens |
|---|---|
| First `huly document create` in a workspace with zero teamspaces | Auto-creates a `General` teamspace |
| First `huly issue create` in a workspace with zero issue statuses | Auto-seeds 5 defaults (Backlog / To do / In progress / Done / Canceled) into `core:space:Model`. Best-effort; re-run if it silently fails. |
| `huly issue create --assignee …` in `ToDo`/`Active` category | Auto-creates the first `ProjectToDo` (see state machine above) |
| `huly dm send --person <email>` | Always creates a new `DirectMessage` doc (no get-or-create; duplicates possible — call `huly dm list --json` first if you care) |
| `huly channel message send` (server-side) | Sender is added to channel `members` if not already a member. The CLI does NOT do this client-side; if the platform doesn't either, the send will fail for non-members. |
| `@<name>` in any message/comment body | Server parses via `extractReferences`, auto-adds mentioned person as `Collaborator`, emits inbox notification |
| `huly project create` | Adds current user as `members[0]` (required by `SpaceSecurityMiddleware` — cannot be skipped) |
| `huly issue create` body is empty | Stores as raw empty string |
| Any auto-retry on duplicate | `huly issue create` and `huly project create` retry on `duplicate`/`already`/`exists` and return the existing record's `_id` |
| `huly action create` without `--attached-to` | Sets `attachedTo` to the resolved Person's `_id` when `--owner <email>` is passed, OR the current user's `account.uuid` when `--owner` is omitted; `attachedToClass` is always `contact:class:Person`. So the todo appears under "my tasks" (or the named owner's personal list), but it is single-parent on the Person — not dual-parent on the issue's `todos` collection (see "The dual-parent trap" above). |
| `huly calendar create` | Always creates a new `Calendar` doc — no "get-or-create" |
| `huly card create` without `--card-space` | Defaults to `card:space:Default` literal — **this usually does not exist**; create one first |

### Reserved keys you cannot use in `--set key=value`

The reserved set differs between `create` and `update`:

- **`create`:** `json, ci, markdown, dryRun, minimal, yes, workspace, url, space`
- **`update`:** `set, unset, json, ci, markdown, dryRun, minimal, yes, workspace, url, defaultProjectIdentifier`

These are silently stripped. `defaultProjectIdentifier` is an internal helper option (used by `--project TSK-5` ref resolution), not a user-facing CLI flag.

### `--yes` is required for

- `workspace create`
- `workspace delete` (and `--force` if deleting the active workspace)
- Any `<resource> delete <ref...>` with ≥2 refs

Single-ref deletes proceed without confirmation. `dm create --person`, `dm send --person`, and `action unschedule --slot-id <single>` are non-destructive in the sense that they don't prompt.

---

## Common task recipes (copy-paste-ready)

### Discover what's in the workspace before doing anything

```bash
huly whoami --json
huly project list --json | jq -r '.[] | "\(.identifier)\t\(.name)\t\(_id)"'
huly action list --owner me --completed false --json | jq -r '.[] | "[\(.priority)] \(.title)"'
```

### Create a project, then a first issue, then assign it

```bash
# 1. Create the project (the CLI help text claims --yes is required; the code does NOT
#    actually enforce it, so it's optional today — included here for forward-compat).
huly project create --name "Q3 Initiative" --identifier Q3I --description "Q3 goals" --yes

# 2. Verify what default statuses were seeded
huly project statuses --project Q3I --json | jq -r '.[] | .name'

# 3. Create the first issue (note: --status defaults to the lowest-rank status, usually Backlog)
huly issue create --project Q3I \
                   --title "Set up CI pipeline" \
                   --priority High \
                   --assignee alice@example.com \
                   --label backend --label infra

# 4. Verify the assignment actually fired the cascade:
huly action list --issue Q3I-1 --json | jq 'length'
# If > 0, a ProjectToDo was created (classic projects only).
```

### Move an issue to Done (and watch the cascade)

```bash
# Preview first — show what the issue looks like and what its open todos are
huly issue get Q3I-1 --json
huly action list --issue Q3I-1 --completed false --json

# Move it
huly issue update Q3I-1 --status Done

# Cascade effect: all open todos on this issue are now doneOn=now.
huly action list --issue Q3I-1 --completed false --json   # should be []
```

### Find everything Alice owns

```bash
# Two paths — try both:
huly user find alice@example.com --json
huly action list --owner alice@example.com --completed false --json | jq -r '.[] | "\(._id)\t\(.title)"'

# To get issues assigned to Alice (NOT the same thing — she's the assignee, not the owner):
huly issue list --assignee alice@example.com --json | jq -r '.[] | "\(.identifier)\t\(.title)"'
```

### Log time and watch it walk the parent chain

```bash
huly time log --issue Q3I-1 --minutes 30 --description "wired up buildkite"
# Then check the issue's totals:
huly issue get Q3I-1 --json | jq '{reportedTime, remainingTime}'
# If Q3I-1 has a parent issue, those numbers will have been recomputed there too.
# There is no opt-out — script accordingly.
```

### Bulk-archive old issues safely

```bash
# NEVER pipe `huly issue delete` to xargs without first previewing what you'll lose.
huly issue list --status-category Won --limit 1000 --json \
  | jq -r '.[]._id' \
  | tee /tmp/to-archive.txt

# Then either delete or move-to-no-parent (move is reversible, delete is NOT):
# `issue move` takes only --parent (no --yes), `issue delete` REQUIRES --yes for ≥2 refs.
cat /tmp/to-archive.txt | xargs -I{} huly issue move {} --parent null
# OR (destructive, cascade-deletes comments/etc):
# cat /tmp/to-archive.txt | xargs -I{} huly issue delete {} --yes
```

### Audit trail — who changed what

```bash
huly ws findAll '["core:class:Tx",{"objectId":"<doc-id>"}]' --json \
  | jq '[.[] | {by: .modifiedBy, on: .modifiedOn, ops: .attributes}]'
```

---

## When the CLI falls short: escape hatches

Two escape hatches handle the ~5% the CLI doesn't cover. Use them only when you have to — the CLI handles auth, ref resolution, output formatting, and error mapping for you.

```bash
# REST escape hatch
huly api GET /api/v1/version
huly api POST /api/v1/foo --body '{"key":"value"}'

# Raw WebSocket RPC (method names mirror the SDK's PlatformClient interface).
# `huly ws` takes ONE positional [params] arg that must be a JSON-encoded ARRAY —
# multi-positional SDK signatures have to be wrapped, e.g. findAll(classId, query, options).
huly ws findAll '["tracker:class:Issue", {"_class":"tracker:class:Issue"}, {}]'
# Space for a project is resolved via getHierarchy().getDomain(CLASS.Project);
# use `huly ws getHierarchy` first if you need the literal id.
huly ws createDoc '["tracker:class:Project", "<project-space>", {"identifier":"NEW","name":"New"}]'
```

Full list of methods, timeouts, and chunks handling: `references/escape-hatches-and-internals.md`.

---

## Which reference to load

If the task is about a specific surface, load the matching reference file **before** running commands. The references contain the gotchas and exact flag semantics that the CLI help text doesn't show.

- Auth, signup, env vars → `references/auth-and-setup.md`
- Workspace / user lookup → `references/workspace-and-user.md`
- Issues, actions/todos, comments, time, the state machine → `references/issues-and-todos.md`
- Projects, components, milestones, issue templates → `references/tracker-projects.md`
- Channels, DMs, threads, activity (reactions/pins/saved) → `references/chat-and-collaboration.md`
- Cards (preferred for new content) → `references/cards.md`
- Documents (only when nested/snapshots/controlled needed) → `references/documents.md`
- Calendar events, recurring events, schedules → `references/calendar-and-schedule.md`
- Spaces, relations, project types, task types, statuses → `references/spaces-types-and-relations.md`
- Notifications inbox, approval requests → `references/notifications-and-approvals.md`
- `huly ws` / `huly api` escape hatches, ref resolver internals, error codes, caches → `references/escape-hatches-and-internals.md`

---

## Quick command reference (the verbs the CLI exposes)

```
workspace    list | current | use <name> | create | delete | info
             members | member add | rename | guests | access-link | regions

user         get | find <email> | update

project      list | get | create | update | delete | statuses
             target-preferences | target-preference upsert

issue        list | get | create | update | delete | preview-delete
             label add <ref> | label remove <ref>
             relation add <ref> | relation remove <ref> | relation list <ref>
             link-document | unlink-document | move
             related-targets | related-target set

component    list | get | create | update | delete
milestone    list | get | create | update | delete
issue-template  list | get | create | update | delete | add-child | remove-child
comment      list | add | update | delete

channel      list | get | create | update | delete | archive | unarchive
             members | join | leave | add-member | remove-member
             message list/send/update/delete
dm           list | create | message list/send
thread       list | add | update | delete

activity     list | get | pin | react | reply list/add/update/delete
             saved list/save/unsave | mentions

card         list | get | create | update | delete
card-space   list | get | create | delete
master-tag   list          # read-only on CLI

document     list | get | create | update | delete
             snapshots | snapshot | inline-comments
teamspace    list | get | create | update | delete

calendar     calendars | create-calendar | delete-calendar
             list | get | create | update | delete
             recurring | recurring-instances <ref>
schedule     list | get | create | update | delete

time         list | log | report | delete
action       list | get | create | update | complete | reopen
             schedule | unschedule | delete

space        list | get | update | permissions
             add-member | remove-member | set-owners
space-type   list | get
association  list | create | delete
relation     list | create | delete
project-type list | get
task-type    list | create
issue-status create

notification list | get | mark-read | mark-unread | mark-all-read
             archive | unarchive | archive-all | delete | unread-count
             providers | types
             contexts list/get/pin/hide
             subscribe | unsubscribe
             settings list/update

approval     list | get | request | comment | approve | reject | cancel | delete

api          <METHOD> <path> [--body] [--query] [--header]
ws           <method> [params] [--no-ping]
```
