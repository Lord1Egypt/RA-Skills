# Project Access

Users may have multiple projects.

The skill must support:
- list projects
- inspect one project summary
- continue an existing project
- create a new project
- get a workspace link

## Default behavior

If the user says "continue" or references prior work:
- check for a suitable existing project first
- do not create a new project by default

If the user asks to "start a new one":
- create a project
- return the new project id and workspace link

## Required handoff fields

For project-mode responses, prefer returning:
- `projectId`
- `projectName`
- `workspaceUrl`
- `stateSummary`
- `lastRunStatus`

## Web access rule

When the user asks to open or inspect the project on web:
- provide the workspace link
- do not require local-only state as the canonical source
