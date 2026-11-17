---
name: "mochi-daily-planner"
description: "Build priority-based time blocks with breaks and backlog, revise plans and export schedules. Use for Daily Planner and Review."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Daily Planner and Review

## Turn priorities into a realistic daily plan

Collect the calendar date, available minutes, task durations and priorities 1..3 (1 first). plan creates one plan per day. Preserve the user's estimates and separate proposed tasks from commitments. show reports remaining open work, completions and over-capacity minutes. complete marks a selected task done; rollover carries open tasks to a later day with source task IDs, so repeated rollover does not duplicate them.

## Amend work as the day changes

add-task appends a title, minutes and priority to an existing date. revise changes those fields on an open task selected by taskId. Keep the plan's existing task IDs and completed work; do not create a second plan for the same day.

## Calculate time blocks and export

schedule takes date, start HH:mm, optional breakMinutes 0..120 and optional availableMinutes for the current remaining window. It orders open tasks by priority, inserts breaks between included tasks, and keeps work that does not fit in backlog. Smaller later tasks may fit after a large task is left out. No block crosses midnight. Show the backlog instead of compressing estimates to make everything appear scheduled.

export uses the same scheduling inputs to save daily-plan.md and time-blocks.csv, including completed items in the Markdown review. The time blocks are a local plan, not calendar bookings or notifications. Use the host's calendar/scheduler tools separately if the user asks for those actions.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-daily-planner/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
