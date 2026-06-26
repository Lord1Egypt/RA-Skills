---
name: plane-flow
description: Operate a local/self-hosted Plane workspace for product and project flow management. Use when the user wants to read or update Plane projects, issues, states, labels, members, or issue metadata; create requirements/tasks from notes; move issue status; assign owners; or summarize project progress. Trigger on requests involving Plane, backlog, issue management, PM workflow, project status, task assignment, or turning meeting notes / feedback into Plane issues.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"],
        "env": ["PLANE_BASE_URL", "PLANE_API_TOKEN", "PLANE_WORKSPACE_ID"],
        "pythonPackages": ["requests"]
      }
    },
    "planeFlow": {
      "optionalEnv": ["PLANE_CONFIG_FILE"],
      "optionalPythonPackages": ["PyYAML", "markdown"],
      "adminSetup": true,
      "businessUserFacing": true,
      "network": {
        "purpose": "Connect to a trusted self-hosted Plane instance configured by the administrator.",
        "destination": "PLANE_BASE_URL"
      },
      "filesystem": {
        "reads": [
          "local files explicitly chosen for issue attachment uploads",
          "optional local config file referenced by PLANE_CONFIG_FILE"
        ],
        "writes": [
          "~/.plane_config.yaml only when an administrator intentionally runs scripts/init_config.py"
        ]
      },
      "credentials": {
        "primary": "PLANE_API_TOKEN",
        "related": ["PLANE_BASE_URL", "PLANE_WORKSPACE_ID"]
      }
    }
  }
---

# Plane Flow

## Overview

Use this skill to work with a locally integrated Plane instance through the bundled scripts in `scripts/`. It supports safe PM operations first, then controlled writes: read projects/issues, summarize a project, create issues, update descriptions, move states, assign owners, set priority, and set labels.

## Operating model

This skill is designed around two roles:

### 1. Administrator / technical owner
The administrator configures the Plane connection for the environment.
That setup includes:
- `PLANE_BASE_URL`
- `PLANE_API_TOKEN`
- `PLANE_WORKSPACE_ID`
- optional `PLANE_CONFIG_FILE`

The administrator may also use bundled helper scripts in `scripts/` for local setup or debugging.

### 2. Business user
Once the environment has been configured, business users should be able to use this skill conversationally for backlog, issue, sprint, and project workflow tasks.
They should not need to deal with environment variables or CLI commands.

## Runtime expectations

- Requires `python3`
- Requires Python package: `requests`
- Optional Python packages:
  - `PyYAML` (only if using `PLANE_CONFIG_FILE`)
  - `markdown` (used for markdown-to-HTML rendering)
- Requires administrator-provided environment variables:
  - `PLANE_BASE_URL`
  - `PLANE_API_TOKEN`
  - `PLANE_WORKSPACE_ID`
- Optional environment variable:
  - `PLANE_CONFIG_FILE`

## Security / behavior notes

- This skill makes network requests only to the Plane instance configured through `PLANE_BASE_URL`.
- It uses `PLANE_API_TOKEN` to authenticate against that Plane instance.
- Attachment upload features can read local files that the operator explicitly chooses to upload.
- The optional init helper can write `~/.plane_config.yaml`, but only when an administrator intentionally runs `scripts/init_config.py`.
- If the Plane connection has not been configured yet, prefer user-facing guidance that asks for administrator setup rather than exposing raw missing-env errors to business users.

## Core Capabilities

### 1. Read Plane workspace data

Use this skill when the user wants to:
- list Plane projects
- inspect project issues
- read a specific issue
- list states, labels, or members
- summarize a project's current status

Prefer these commands:
- `python3 scripts/plane_cli.py projects list`
- `python3 scripts/plane_cli.py issues list --project <project>`
- `python3 scripts/plane_cli.py issues get --project <project> --id <issue_id>`
- `python3 scripts/plane_cli.py projects summary --project <project>`
- `python3 scripts/plane_cli.py states list --project <project>`
- `python3 scripts/plane_cli.py labels list --project <project>`
- `python3 scripts/plane_cli.py members list`

### 2. Create and enrich issues

Use this skill when the user wants to:
- create a requirement, task, or bug in Plane
- turn meeting notes into one or more Plane issues
- add more context to an existing issue
- attach images to issue descriptions or comments

Prefer this flow:
1. Resolve the target project
2. If needed, inspect states / labels / members first
3. Create the issue
4. Optionally enrich it with description, labels, priority, assignee, or state

Prefer these commands:
- `python3 scripts/plane_cli.py issues create --project <project> --title <title> --desc <desc>`
- `python3 scripts/plane_cli.py issues update-desc --project <project> --id <issue_id> --desc <desc>`
- `python3 scripts/plane_cli.py issues set-priority --project <project> --id <issue_id> --priority <priority>`
- `python3 scripts/plane_cli.py issues set-labels --project <project> --id <issue_id> --labels <comma-separated-labels>`
- `python3 scripts/plane_cli.py issues assign --project <project> --id <issue_id> --assignee <member>`
- `python3 scripts/plane_cli.py issues move --project <project> --id <issue_id> --state <state>`

### 2b. Inline images in issue descriptions and comments

This skill supports uploading images and embedding them directly in issue descriptions or comments.
Images are uploaded as Plane issue attachments, then embedded using Plane's native image-component nodes with alignment control.

#### Directive syntax (in `--desc` for issue descriptions)

Place `[image: /path/to/image.png, <align>]` anywhere in the description text:

```
[image: ./screenshot.png, center]   – centred block
[image: ./screenshot.png, left]     – left-aligned block
[image: ./screenshot.png, right]    – right-aligned block
```

Available alignments: `center` (default), `left`, `right`.

Examples:

```bash
# Create issue with a centred image in description
python3 scripts/plane_cli.py issues create \
  --project <project> \
  --title "Requirement with screenshot" \
  --desc "See diagram below:\n\n[image: ./diagram.png, center]"

# Create issue with left and right images
python3 scripts/plane_cli.py issues create \
  --project <project> \
  --title "Comparison" \
  --desc "Before:\n[image: ./before.png, left]\n\nAfter:\n[image: ./after.png, right]"
```

#### CLI flag syntax (for issue descriptions and comments)

Use `--image <path>` to attach images, with `--image-align` to set alignment:

```bash
# Issue with images (all same alignment)
python3 scripts/plane_cli.py issues create \
  --project <project> \
  --title "Report" \
  --desc "See attachments" \
  --image ./fig1.png \
  --image ./fig2.png \
  --image-align center

# Comment with a right-aligned image
python3 scripts/plane_cli.py comments create \
  --project <project> \
  --issue-id <issue_id> \
  --content "Screenshot:" \
  --image ./screen.png \
  --image-align right
```

Alignment applies to all `--image` flags in the same command. For mixed alignments in a single call, use the directive syntax inside `--desc`.

#### Behavior notes

- Images are uploaded as issue attachments in Plane, then embedded in `description_html` or `comment_html` using Plane's native `<image-component>` nodes.
- Alignment uses Plane's built-in `alignment` attribute (`left`, `center`, `right`).
- True text wrapping around floating images is not supported by Plane's editor — images are always block-level elements.
- If image embedding fails (e.g., no asset URL returned), the image is still saved as an attachment and a text note is added to the description/comment.

### 3. Turn PM inputs into structured Plane changes

Use this skill when the user provides:
- meeting notes
- feedback summaries
- requirement drafts
- PM action items
- triage instructions

Recommended approach:
1. Extract candidate issues from the source text
2. Group or deduplicate obvious overlaps
3. Draft issue titles and descriptions
4. Ask for confirmation only when needed for destructive or ambiguous writes
5. Create issues and enrich metadata

### 4. Summarize project flow

Use this skill when the user asks for:
- backlog overview
- project progress
- blocked/high-priority work
- issue status distribution
- PM-style progress summaries

Start with:
- `python3 scripts/plane_cli.py projects summary --project <project>`
- `python3 scripts/plane_cli.py issues list --project <project>`

Then transform the raw output into a concise PM summary.

## Working Rules

- Always prefer the bundled Plane integration in `scripts/` over inventing raw API calls unless debugging is required.
- For issue detail and issue updates, always include `--project <project>`; this Plane instance uses project-scoped issue detail/update routes.
- If a write fails, inspect current states / labels / members before retrying.
- Prefer single-issue updates over bulk mutation unless the user explicitly asks for batch changes.
- For ambiguous project names, resolve by listing projects first.
- For ambiguous assignees, resolve by listing members first.
- For ambiguous labels or states, resolve by listing labels/states first.
- When a description or comment includes images, prefer uploading them as issue attachments and embedding them inline using the `[image: path, align]` directive or `--image` / `--image-align` flags rather than linking to external URLs.

## When to Inspect Raw Output

Use `--raw` when:
- debugging field mappings
- checking unfamiliar Plane response structures
- validating a new endpoint behavior
- confirming what IDs correspond to states, labels, or other metadata

## References

- Read `references/cli-usage.md` for a compact command cookbook and practical examples.
