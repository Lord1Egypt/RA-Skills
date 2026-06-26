---
name: pf-clone-gitlab
description: Batch clone GitLab group projects with branch checkout and Excel indexing. Use when user needs to clone all projects from a GitLab group, organize by group structure, checkout multiple branches (master/default + latest + release/prod), and generate an Excel index file with project metadata and branch information.
---

# Clone GitLab Skill

Batch clone all projects from GitLab group(s), maintain folder hierarchy, checkout key branches, and generate an Excel index.

## When to Use

- User wants to batch clone all projects from one or more GitLab top-level groups
- Need to maintain original group/subgroup folder hierarchy locally
- Need to checkout multiple branches (default + latest active + release/prod)
- Need an Excel index file (`01.Index.xlsx`) with per-group sheets

## Requirements

Before starting, collect from user:

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| GitLab URL | ✅ | — | e.g. `https://gitlab.company.com` |
| Personal Access Token | ✅ | — | Needs `read_api` + `read_repository` scopes |
| Target Group(s) | ✅ | — | Group/sub-group/project paths, comma-separated. Supports: top-level group (`myGroup`), sub-group path (`myGroup/mySubGroup`), or direct project path (`myGroup/mySubGroup/my-project`) |
| Local Storage Path | ❌ | `~/Desktop/Code` | Where repos are stored |
| Auth Method | ❌ | HTTPS+Token | Or SSH if key is configured |
| Mode | ❌ | clone | `clone` (default), `update` (pull only), or `sync` (clone+pull+cleanup stale Excel rows) |
| Workers | ❌ | 4 | Parallel clone workers (`GITLAB_WORKERS`) |
| Total Timeout | ❌ | 0 (none) | Global timeout in seconds (`GITLAB_TOTAL_TIMEOUT`). 0=no limit |

## Workflow

### Step 1: Collect Input

Ask user for the 4 parameters above. Pass them as environment variables to the script:

```
GITLAB_URL, GITLAB_TOKEN, GITLAB_GROUPS (comma-separated), GITLAB_BASE_DIR
```

### Step 2: Run the Script

```bash
cd <skill-dir>/scripts
python3 clone_and_index.py
```

The script handles everything:
1. Resolves each input path — auto-detects if it's a top-level group, sub-group, or direct project
2. For top-level groups: fetches all subgroups recursively (skips if access denied)
3. For sub-group paths (e.g. `myGroup/mySubGroup`): directly resolves and syncs that sub-group and its descendants only
4. For direct project paths: syncs only that specific project
5. Clones new projects / pulls existing ones (with 5-min timeout per project)
6. Uses multiprocessing for parallel clone/pull (process-group kill on timeout to prevent orphan git processes)
7. Checks out branches: default + latest active + release/prod
8. **Incrementally** updates `01.Index.xlsx` every 50 projects (so partial results survive crashes)
9. On SIGTERM/SIGINT, emergency-flushes pending results to Excel before exit
10. Prints per-group project counts during discovery and real-time progress with elapsed time
11. In `sync` mode, the final Excel write removes rows for deleted/archived projects and handles cross-group migrations

### Step 3: Report Results

After the script finishes, report:
- Total projects cloned/updated
- Any failed/timed-out projects (the script prints a summary table)

## Modes

### Update Only

If projects already exist and user just wants to update:

```bash
GITLAB_MODE=update python3 clone_and_index.py
```

This skips clone, only does `git fetch --all && git pull` on existing repos, re-checkouts branches, and refreshes the Excel.

### Sync (Full Sync with Cleanup)

For a complete sync that also cleans up stale data in the Excel:

```bash
GITLAB_MODE=sync python3 clone_and_index.py
```

This behaves like `clone` mode (new repos are cloned, existing ones are pulled), but additionally:
- Removes Excel rows for projects that no longer exist on GitLab (deleted/archived)
- Handles projects that moved between groups (updates path, removes old row)
- Only cleans up sheets belonging to the groups specified in `GITLAB_GROUPS` (won't touch other groups' data)

## Excel Specification

**File:** `01.Index.xlsx` inside `<local-path>/` (e.g. `~/Desktop/Code/01.Index.xlsx`)

**Sheets:** One sheet per top-level group (sheet name = group name, e.g. "myGroup")

**Columns:**

| Col | Field | Content |
|-----|-------|---------|
| A | 主Group名称 | Top-level group (e.g. myGroup) |
| B | 子Group路径 | Full group path without project name |
| C | Project路径 | Full path (e.g. myGroup/mySubGroup/myProject) |
| D | Project名称 | Project name |
| E | Project描述 | GitLab description |
| F | 已checkout分支 | All local branches, one per line |
| G | 分支最新提交时间 | Corresponding commit times, one per line |
| H | SSH Git链接 | ssh_url_to_repo |
| I | 下载时间 | Clone/update timestamp |
| J | Project ID | GitLab project ID (hidden column, used for matching) |

**Sort:** A (asc) → B (asc) → D (asc)

**Formatting:** Frozen header row, thin borders on all cells, F/G columns left-aligned with wrap, other columns center-aligned, UTF-8 encoding.

## Security

- Token is passed via environment variable, never logged
- After clone, remote URL is reset to remove embedded token
- If clone times out or crashes, a cleanup step removes token from `.git/config`

## Output Structure

```
~/Desktop/Code/
├── 01.Index.xlsx
├── myGroup/
│   ├── SubGroup1/
│   │   ├── project-a/
│   │   └── project-b/
│   └── SubGroup2/
│       └── project-c/
└── AnotherGroup/
    └── ...
```
