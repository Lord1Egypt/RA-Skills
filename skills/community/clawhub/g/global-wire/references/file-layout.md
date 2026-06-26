# File Layout

GlobalWire should work as a zero-configuration public skill.

## Public default layout

Save under a relative project folder:

```text
./global-wire/
  briefs/
    2026-03-24.md
  alerts/
    2026-03-24-us-iran-escalation.md
  timelines/
    us-iran-conflict.md
  snapshots/
    2026-03-24/
```

## Naming rules

- Brief files: `YYYY-MM-DD.md`
- Alert files: `YYYY-MM-DD-event-slug.md`
- Timeline files: `event-slug.md`
- Snapshot folders: `YYYY-MM-DD/`

## Adaptation rule

If the current workspace already has a stronger editorial structure, keep the public folder semantics and map them to the nearest compatible relative path. Do not require a user-specific absolute path.

## Saving rules

1. Prefer markdown.
2. Preserve the visible section headers from the rendered output.
3. Keep one file per brief run and one rolling file per continuing timeline.
4. Do not overwrite a timeline destructively; append or refresh carefully.
5. If the user does not ask to save, saving is still appropriate when the workflow is clearly archival or repeatable.
