# Project Template Workflows

Reusable project templates are blueprints stored in a space's template library. Use the `project_templates` namespace to create, edit, and instantiate templates. Template content is **not** live work — use live namespaces when collaborating on active projects, goals, or spaces.

See also: [Project Workflows](project-workflows.md) for live projects, [Docs & Files](docs-and-files.md) for live hub commands, [Collaboration Patterns](collaboration-patterns.md) for live vs template comments.

## When to Use Templates vs Live Commands

| Intent | Use | Example |
| --- | --- | --- |
| Edit a reusable blueprint | `project_templates …` | `operately project_templates update_task …` |
| Collaborate on an active project | `projects …`, `tasks …`, `comments …` | `operately comments create --entity-type project_task …` |
| Comment on blueprint content | `project_templates create_comment …` | `--parent-type discussion` |
| Comment on live check-ins, tasks, docs | `comments create …` | `--entity-type project_check_in` |
| Staff a template blueprint | `project_templates create_person …` | roles, access, task assignments |
| Add people to a live project | `projects create_contributor …` | `--permissions edit_access` |
| Template Docs & Files | `project_templates create_document …` | materializes when a project is created |
| Live Docs & Files | `documents create_document …` | `--space-id`, `--project-id`, or `--goal-id` |

## Feature Availability

Templates are feature-gated per space. Enable them without overwriting unrelated tool settings:

```bash
operately spaces update_tools \
  --space-id s1 \
  --tools.templates-enabled true
```

Check whether templates are enabled on a space via `operately spaces get --id s1` (`templates_enabled` field).

**Archived templates** can be listed and restored, but cannot be used with `create_project`.

## Library and Lifecycle

### List and Get

```bash
operately project_templates list --space-id s1
operately project_templates get --id pt1
```

### Create Empty Template

```bash
operately project_templates create \
  --space-id s1 \
  --name "Product Launch Blueprint" \
  --description "# Launch template\n\nStandard launch workflow."
```

### Save Template from Existing Project

Returns `schedule_issues` when the source project has dates before its start date:

```bash
operately project_templates create_from_project \
  --project-id p1 \
  --name "Launch Template from Q2 Project" \
  --include-people-and-assignments true \
  --include-discussions true \
  --include-docs-and-files true
```

Review `schedule_issues` in the response and adjust relative offsets if needed.

### Create Live Project from Template

```bash
operately project_templates create_project \
  --template-id pt1 \
  --space-id s1 \
  --start-date 2026-09-01 \
  --name "Q4 Product Launch" \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70
```

Optional: `--goal-id g1` to link the new project to a goal.

### Duplicate, Update, Archive, Restore, Delete

```bash
operately project_templates duplicate --id pt1 --name "Copy of Launch Blueprint"
operately project_templates update --id pt1 --name "Updated Launch Blueprint"
operately project_templates archive --id pt1
operately project_templates restore --id pt1
operately project_templates delete --id pt1
```

## Relative Scheduling

Template milestones and tasks use **due offsets** (days from project start), not absolute calendar dates. When `create_project` runs, offsets are converted using `--start-date`.

```bash
operately project_templates create_milestone \
  --template-id pt1 \
  --title "Beta Launch" \
  --due-offset-days 30

operately project_templates update_milestone \
  --template-id pt1 \
  --milestone-id tm1 \
  --title "Public Launch" \
  --due-offset-days 45
```

Update the template's project duration with `operately project_templates update --id pt1 --duration-days 90`.

## Plan Structure

### Milestones

```bash
operately project_templates create_milestone \
  --template-id pt1 \
  --title "Design Phase" \
  --due-offset-days 14

operately project_templates update_milestone \
  --template-id pt1 \
  --milestone-id tm1 \
  --title "Design & Research" \
  --due-offset-days 21

operately project_templates delete_milestone \
  --template-id pt1 \
  --milestone-id tm1
```

### Tasks

```bash
operately project_templates create_task \
  --template-id pt1 \
  --milestone-id tm1 \
  --name "Create wireframes" \
  --due-offset-days 7

operately project_templates update_task \
  --template-id pt1 \
  --task-id tt1 \
  --name "Create high-fidelity mockups" \
  --due-offset-days 10

operately project_templates delete_task \
  --template-id pt1 \
  --task-id tt1
```

Clear a template task due offset with `--due-offset-days null` when no offset is intended.

### Move Tasks (Zero-Based Index)

```bash
operately project_templates update_milestone_and_ordering \
  --template-id pt1 \
  --task-id tt1 \
  --milestone-id tm2 \
  --index 0
```

`--index` is zero-based within the target milestone.

### Task Assignees

```bash
operately project_templates update_task_assignees \
  --template-id pt1 \
  --task-id tt1 \
  --assignee-ids u1 \
  --assignee-ids u2
```

## Template Contributors (People)

Template contributors define blueprint staffing. They are **not** live project contributors.

```bash
operately project_templates create_person \
  --template-id pt1 \
  --person-id u1 \
  --role reviewer \
  --responsibility "Product Lead" \
  --access-level 70

operately project_templates update_person \
  --template-id pt1 \
  --template-person-id tp1 \
  --responsibility "Lead PM" \
  --access-level 70

operately project_templates delete_person \
  --template-id pt1 \
  --template-person-id tp1
```

## Discussions and Comments

### Discussions

```bash
operately project_templates create_discussion \
  --template-id pt1 \
  --title "Launch checklist" \
  --body "# Pre-launch\n\nReview before each launch."

operately project_templates get_discussion \
  --template-id pt1 \
  --discussion-id td1

operately project_templates update_discussion \
  --template-id pt1 \
  --discussion-id td1 \
  --title "Updated launch checklist" \
  --body-file ./launch-checklist.md
```

### Template Comments (Not Live Comments)

Use `project_templates` comment commands for blueprint content only:

```bash
operately project_templates list_comments \
  --template-id pt1 \
  --parent-type discussion \
  --parent-id td1

operately project_templates create_comment \
  --template-id pt1 \
  --parent-type discussion \
  --parent-id td1 \
  --content "Add security review step."

operately project_templates update_comment \
  --template-id pt1 \
  --comment-id tc1 \
  --content "Add security and compliance review."

operately project_templates delete_comment \
  --template-id pt1 \
  --comment-id tc1
```

Valid `--parent-type` values: `discussion`, `document`, `file`, `link`.

For comments on **live** resources, use `operately comments create/update/delete` instead.

## Template Docs & Files

Template resources are separate from live `documents/*` commands. They copy into the project hub when `create_project` runs.

### Folders

```bash
operately project_templates create_folder \
  --template-id pt1 \
  --name "Specs"

operately project_templates update_folder \
  --template-id pt1 \
  --folder-id tf1 \
  --name "Technical Specs"
```

### Documents

```bash
operately project_templates create_document \
  --template-id pt1 \
  --name "Launch Runbook" \
  --content "# Runbook\n\nSteps for launch day."

operately project_templates update_document \
  --template-id pt1 \
  --document-id td1 \
  --name "Launch Runbook v2" \
  --content-file ./runbook.md
```

### Links

```bash
operately project_templates create_link \
  --template-id pt1 \
  --name "Design System" \
  --url "https://design.example.com" \
  --type other
```

### File Upload

Upload a local file into the template (handles blob upload internally):

```bash
operately project_templates create_file \
  --template-id pt1 \
  --file ./launch-checklist.pdf

operately project_templates create_file \
  --template-id pt1 \
  --parent-folder-id tf1 \
  --file ./spec.pdf \
  --name "Product Spec" \
  --description-file ./spec-notes.md
```

### Update, Move, Delete Resources

```bash
operately project_templates update_file \
  --template-id pt1 \
  --file-id tf1 \
  --name "Updated Spec"

operately project_templates move_resource \
  --template-id pt1 \
  --node-id tr1 \
  --parent-folder-id tf2

operately project_templates delete_resource \
  --template-id pt1 \
  --node-id tr1
```

## Include Toggles on create_from_project

When saving a project as a template, control what is copied:

| Flag | Default | Copies |
| --- | --- | --- |
| `--include-people-and-assignments` | `false` | Contributors and task assignees |
| `--include-discussions` | `true` | Template discussions |
| `--include-docs-and-files` | `true` | Folders, documents, links, files |
| `--include-comments` | `false` | Comments on included resources |

## Gotchas

### Wrong Namespace

If a command returns `not_found` for a template parent, confirm you are not using live `comments/*` or `documents/*` on template IDs (or vice versa).

### Archived Templates

`list` may include archived templates. Restore with `restore` before `create_project`.

### Live Task Routing

Edit tasks on active projects with `tasks/*`. Edit blueprint tasks with `project_templates create_task`, `update_task`, etc.

### CLI Version

Project templates, scoped search, and document history require Operately CLI **1.9.0** or newer. Run `operately --version` before template workflows.
