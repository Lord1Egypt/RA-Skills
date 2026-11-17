# Spaces, relations, type configuration

The lower-level surface that other resources are built on. You usually don't need this for everyday work — but you DO need it when you're:

- Setting up custom project / task / status types
- Wiring cross-resource relations
- Inspecting per-space permissions
- Doing structural migrations

---

## Decision: do I need this surface?

For 95% of work, the higher-level surfaces (`project`, `issue`, `card`, `document`) handle what you need. Reach for this surface only if:

- The user explicitly asks about **Space**, **SpaceType**, **Association**, **Relation**, or **Permission**.
- You need to create a **ProjectType**, **TaskType**, or **IssueStatus**.
- You're debugging a permission issue (`space permissions <ref>`).
- You need to wire something that the higher-level surfaces don't expose.

---

## Mental model: Spaces are the universal container

A **Space** (`core:class:Space`) is the abstract container primitive. Almost everything else is a sub-class:

| Higher-level surface | Class                         | Lives in space                                                                 |
| -------------------- | ----------------------------- | ------------------------------------------------------------------------------ |
| Tracker projects     | `tracker:class:Project`       | project domain (resolved via `client.getHierarchy().getDomain(CLASS.Project)`) |
| Chunter channels     | `chunter:class:Channel`       | `chunter:space:Chunter`                                                        |
| Chunter DMs          | `chunter:class:DirectMessage` | `chunter:space:Chunter`                                                        |
| Calendar calendars   | `calendar:class:Calendar`     | `core:space:Workspace`                                                         |
| Calendar events      | `calendar:class:Event`        | `calendar:space:Calendar`                                                      |
| Document teamspaces  | `document:class:Teamspace`    | `document:space:Default`                                                       |
| Documents            | `document:class:Document`     | teamspace's space                                                              |
| Cards                | `card:class:Card`             | card-space's space                                                             |
| MasterTags           | `card:class:MasterTag`        | card-space's space                                                             |

All share common fields: `name, description, private, archived, members, owners, type`.

When `huly space …` is useful: rare. Most operations work via the higher-level commands (`project`, `channel`, `calendar`, etc.).

---

## Space commands

```bash
huly space list --json
huly space list --type tracker:class:Project --json     # filter by SpaceType ref
huly space list --archived false --json                  # non-strict coercion
huly space list --private false --json

huly space get <ref> --json                              # by id
huly space update <ref> --name "…" --description "…" --private false --archived false

huly space permissions <ref> --json                      # role/permission matrix

huly space add-member    <ref> --members <emails...>     # --members REQUIRED, variadic
huly space remove-member <ref> --members <emails...>
huly space set-owners    <ref> --members <emails...>     # REPLACES owners array
```

**`add-member` de-duplicates** against existing members (no-op if all already present). **`remove-member`** does NOT pre-check (silent no-op on non-members via the SDK's `$pull` semantics). **`set-owners`** REPLACES the owners array unconditionally — there is no merge.

`--members` accepts:

- `me` or empty string → current user
- Full email (exact case-insensitive)
- Person UUID

The same `--members` flag is used on `space add-member`, `space remove-member`, `space set-owners`, AND on `channel add-member` / `channel remove-member`. The semantics differ (add vs remove vs replace).

---

## Space-type commands

```bash
huly space-type list --json
huly space-type get <ref> --json
```

Read-only. Lists `core:class:SpaceType` records. Use this to discover what SpaceTypes are available before creating a project with a custom type.

---

## Association vs Relation vs Issue.relations

Three different cross-resource link primitives. Pick the right one:

| Primitive                             | Class                    | Direction                  | Use                                                        |
| ------------------------------------- | ------------------------ | -------------------------- | ---------------------------------------------------------- |
| **Issue.relations / Issue.blockedBy** | (Issue-class fields)     | Issue ↔ Issue              | Ergonomic tracker relations; use `huly issue relation add` |
| **Association**                       | `core:class:Association` | Bi-directional, A ↔ B, N:N | Generic symmetric links between any two docs               |
| **Relation**                          | `core:class:Relation`    | Asymmetric A → B           | One-directional A→B link with a name                       |

For ergonomic issue-to-issue linking, ALWAYS prefer `huly issue relation`:

```bash
huly issue relation add  TSK-1 --type blocks       --target TSK-2
huly issue relation add  TSK-1 --type isBlockedBy  --target TSK-2
huly issue relation add  TSK-1 --type relatesTo    --target TSK-2
huly issue relation list TSK-1                       # merged view of blocks + isBlockedBy + relatesTo
```

The `huly association` and `huly relation` commands operate on the lower-level primitives and should be used only when:

- You need a non-Issue-to-Issue link (e.g. document ↔ document, or card ↔ issue)
- You're building a custom plugin
- You need N:N symmetric semantics

### Association

```bash
huly association list --json
huly association list --a <ref-A> --b <ref-B> --a-class <id> --b-class <id>
huly association create --a <ref-A> --b <ref-B> --a-class <id> --b-class <id>
huly association delete <ref>                # single
huly association delete <r1> <r2> --yes     # REQUIRED --yes for multiple
```

--a-class and --b-class default to `core:class:Doc`. The resulting `Association` is attached to `aDoc.space` under `aDoc` on the `associations` collection.

### Relation

```bash
huly relation list --source <ref> --target <ref> --source-class <id> --target-class <id>
huly relation create --source <ref> --target <ref> --name "dependency" --source-class <id> --target-class <id>
huly relation delete <ref>
huly relation delete <r1> <r2> --yes        # REQUIRED --yes for multiple
```

`--name` defaults to the literal string `'relation'`. Source's space is used to attach the relation.

---

## ProjectType, TaskType, IssueStatus

These configure the structure of tracker projects. Critical constraint:

**Custom space types and custom task types can ONLY be applied to NEW projects. You cannot migrate an existing project.**

If the user wants to change a project's type, the workflow is:

1. Read all issues from the old project.
2. Create a new project with the desired type.
3. Copy issues (and meta) to the new project.
4. Delete the original project.

See the bulk-migrate recipe in `references/tracker-projects.md`.

### project-type commands

```bash
huly project-type list --json
huly project-type get <ref> --json
```

**Read-only.** There is NO `huly project-type create`. ProjectTypes are created server-side as part of workspace bootstrap or plugin setup.

`ProjectType.classic = true` is the gating flag for the issue↔action cascade (see `references/issues-and-todos.md`).

### task-type commands

```bash
huly task-type list --project-type <ref> --json
huly task-type list --json
huly task-type create --project-type <ref> --label "Story" --description "User-facing story"
```

**`--project-type` is REQUIRED on create.** `--label` is REQUIRED (becomes `name`).

**Defaults:** `rank: '0|aaaaa:'`, `icon: 'task'`. **No `--icon` flag is exposed** despite the field existing.

The created TaskType is stored on `task:class:TaskType`, attached to the ProjectType in its `taskTypes` collection. Effect: only new projects picking up this TaskType use it (cannot migrate existing).

### issue-status commands

```bash
huly issue-status create \
  --project-type <ref> \
  --name "Blocked" \
  --category Active \
  --task-type <ref> \
  --description "waiting on external" \
  --rank "5|aaaaa:"
huly issue-statuses create ...     # alias
```

**Required on create:** `--project-type`, `--name`, `--category`. The `--category` enum is strict: `UnStarted | ToDo | Active | Won | Lost`.

**Optional:** `--task-type` (defaults to the ProjectType's first TaskType; throws `NotFound` if the ProjectType has zero TaskTypes), `--description`, `--rank` (defaults to `'0|aaaaa:'`).

After creating, verify it appears for the project:

```bash
huly project statuses --project TSK --json | jq -r '.[] | "\(.name) [\(.category)]"'
```

The `--category` determines cascade behavior. See `references/issues-and-todos.md` for the state machine mapping.

---

## Per-space permissions

Every space has a `Permission` matrix checked on every `TxCUD`. The CLI exposes ONE command for inspection: `huly space permissions <ref>`. There is NO `huly permission add`/`remove` — the matrix is managed by the server auto-middleware when members/owners change.

```bash
huly space permissions <ref> --json
# Returns array of {role, _id, ...} where role is resolved against core:class:Role.
# Empty → "(no permissions)".
```

If you need to programmatically check "can user X do operation Y in space Z?", use the SDK's `canPerform` method — the CLI doesn't expose it.

---

## Common task recipes

### Discover the project type and confirm it enables cascades

```bash
# Find the project-type ref
huly project get TSK --json | jq '.type'

# Inspect it
huly project-type get <type-ref> --json | jq '{name, classic, descriptor}'
# "classic": true → issue↔action cascade fires.
# "classic": false (Recruit/Lead) → no auto-todo creation/closure.
```

### Add an issue status with custom logic

```bash
# Find the project type
PT=$(huly project get TSK --json | jq -r '.type')
# Find the first task type for it
TT=$(huly task-type list --project-type "$PT" --json | jq -r '.[0]._id')

# Create a custom status
huly issue-status create \
  --project-type "$PT" \
  --task-type "$TT" \
  --name "In Review" \
  --category Active \
  --description "PR open, awaiting review"

# Verify
huly project statuses --project TSK --json | jq -r '.[] | select(.name == "In Review")'
```

### Find spaces a user has access to

```bash
huly space list --json \
  | jq -r --arg uid "<user-uuid>" \
    '.[] | select(.members[]? == $uid) | "\(.name)\t\(_id)"'
```

### Wire a document to a card via Association

```bash
# A = card, B = document (or reverse — order matters for storage location)
huly association create \
  --a <card-ref> --a-class card:class:Card \
  --b <doc-ref> --b-class document:class:Document
```

### Inspect the permission matrix on a project

```bash
huly project get TSK --json | jq -r '._id' \
  | xargs -I{} huly space permissions {} --json \
  | jq -r '.[] | "\(.role // "<unnamed>")\t\(_id)"'
```

---

## Gotchas

- **`huly space` covers generic spaces.** Most operations work via the higher-level surfaces (project, channel, calendar, etc.). Don't reach for `space` first.
- **ProjectTypes are not CLI-creatable.** The CLI only lists them. Bootstrap or migration must happen via raw RPC or web UI.
- **Custom types only apply to NEW projects.** Cannot migrate existing projects. Plan accordingly.
- **`--category` on issue-status is strict** (`UnStarted|ToDo|Active|Won|Lost`). Case-sensitive.
- **`task-type --project-type` and `--label` are REQUIRED** on create. `--icon` is NOT exposed despite the field existing.
- **Association order matters.** `--a` is the attached doc; the Association lives in `aDoc.space`. Pick the more "stable" side as A.
- **Relation is asymmetric A→B.** The CLI does NOT mirror to B's side. If you want bi-directional, use Association.
- **`Issue.relations`** is a special-case field on Issue itself, NOT the same as `core:class:Relation`. Don't confuse them.
- **`huly space permissions <ref>` is read-only.** No CLI command to add/remove permissions. The server manages this automatically on member changes.
- **Per-space permission checks happen on EVERY TxCUD** — there is no global role override. Granting rights is per-space.
- **Disabling RBAC** is a global, workspace-wide privilege escalation. The CLI does not expose the toggle (server-side only: Settings → General → disable RBAC for the whole workspace). Anyone with any account on the workspace gains full read/write access to every space, document, issue, and channel. **Never disable RBAC on a workspace that contains real customer data.** Re-enabling RBAC does not retroactively restore previous ACLs — access changes made while RBAC was off persist. There is no undo. Prefer per-space permission grants via the web UI instead. This is a one-way door.

---

## Where the cascade behaviors live

When a side effect fires (e.g. assigning an issue creates a ProjectToDo), the relevant `On…` mixin lives in the corresponding server plugin. The CLI role is just to know which command triggers which mixin:

| Mixin                                          | Triggered by CLI command(s)                      | Where           |
| ---------------------------------------------- | ------------------------------------------------ | --------------- |
| `OnProjectRemove`                              | `huly project delete`                            | tracker plugin  |
| `OnComponentRemove`                            | `huly component delete`                          | tracker plugin  |
| `OnIssueUpdate`                                | `huly issue update`, `huly time log`             | tracker plugin  |
| `OnToDoUpdate`                                 | `huly action update --title\|--visibility`       | time plugin     |
| `OnToDoRemove`                                 | `huly action delete`                             | time plugin     |
| `OnWorkSlotCreate`                             | `huly action schedule` (first slot)              | time plugin     |
| `OnWorkSlotUpdate`                             | `huly action update --visibility` mirrors        | time plugin     |
| `OnCardTag`                                    | server-side, on attribute add to one card        | card plugin     |
| `OnDocTitleChanged`, `OnDocHasBecomeEffective` | server-side, on ControlledDocument state changes | document plugin |

See `references/issues-and-todos.md` for the full cascade table.
